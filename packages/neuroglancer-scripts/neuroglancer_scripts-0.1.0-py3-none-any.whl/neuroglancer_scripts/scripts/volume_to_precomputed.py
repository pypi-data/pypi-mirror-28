#! /usr/bin/env python3
#
# Copyright (c) 2016, 2017, Forschungszentrum Juelich GmbH
# Author: Yann Leprince <y.leprince@fz-juelich.de>
#
# This software is made available under the MIT licence, see LICENCE.txt.

import json
import logging
import os
import os.path
import sys

import numpy as np
import nibabel
import nibabel.orientations
from tqdm import tqdm

import neuroglancer_scripts.accessor
from neuroglancer_scripts.accessor import convert_file_url_to_pathname
import neuroglancer_scripts.chunk_encoding
import neuroglancer_scripts.pyramid_io


logging.basicConfig(format='%(message)s', level=logging.INFO)


# TODO import from library
NG_DATA_TYPES = ("uint8", "uint16", "uint32", "uint64", "float32")


def nifti_to_neuroglancer_transform(nifti_transformation_matrix, voxel_size):
    """Compensate the half-voxel shift introduced by Neuroglancer for Nifti data

    Nifti specifies that the transformation matrix (legacy, qform, or sform)
    gives the spatial coordinates of the *centre* of a voxel, while the
    Neuroglancer "transform" matrix specifies the *corner* of voxels.

    This function compensates the resulting half-voxel shift by adjusting the
    translation parameters accordingly.
    """
    ret = np.copy(nifti_transformation_matrix)
    ret[:3, 3] -= np.dot(ret[:3, :3], 0.5 * np.asarray(voxel_size))
    return ret


def volume_to_raw_chunks(pyramid_writer, volume, chunk_transformer=None):
    info = pyramid_writer.info
    assert len(info["scales"][0]["chunk_sizes"]) == 1  # more not implemented
    chunk_size = info["scales"][0]["chunk_sizes"][0]  # in order x, y, z
    size = info["scales"][0]["size"]  # in order x, y, z
    dtype = np.dtype(info["data_type"]).newbyteorder("<")
    num_channels = info["num_channels"]

    # Volumes given by nibabel are using Fortran indexing (X, Y, Z, T)
    assert volume.shape[:3] == tuple(size)
    if len(volume.shape) > 3:
        assert volume.shape[3] == num_channels

    progress_bar = tqdm(
        total=(((size[0] - 1) // chunk_size[0] + 1)
               * ((size[1] - 1) // chunk_size[1] + 1)
               * ((size[2] - 1) // chunk_size[2] + 1)),
        desc="writing", unit="chunks", leave=True)
    for z_chunk_idx in range((size[2] - 1) // chunk_size[2] + 1):
        z_slicing = np.s_[chunk_size[2] * z_chunk_idx:
                          min(chunk_size[2] * (z_chunk_idx + 1), size[2])]
        for y_chunk_idx in range((size[1] - 1) // chunk_size[1] + 1):
            y_slicing = np.s_[chunk_size[1] * y_chunk_idx:
                              min(chunk_size[1] * (y_chunk_idx + 1), size[1])]
            for x_chunk_idx in range((size[0] - 1) // chunk_size[0] + 1):
                x_slicing = np.s_[chunk_size[0] * x_chunk_idx:
                                  min(chunk_size[0] * (x_chunk_idx + 1), size[0])]
                if len(volume.shape) == 4:
                    chunk = volume[x_slicing, y_slicing, z_slicing, :]
                elif len(volume.shape) == 3:
                    chunk = volume[x_slicing, y_slicing, z_slicing]
                    chunk = chunk[..., np.newaxis]

                if chunk_transformer is not None:
                    chunk = chunk_transformer(chunk)


                chunk = np.moveaxis(chunk, (0, 1, 2, 3), (3, 2, 1, 0))
                assert chunk.size == ((x_slicing.stop - x_slicing.start) *
                                      (y_slicing.stop - y_slicing.start) *
                                      (z_slicing.stop - z_slicing.start) *
                                      num_channels)

                chunk_coords = (x_slicing.start, x_slicing.stop,
                                y_slicing.start, y_slicing.stop,
                                z_slicing.start, z_slicing.stop)
                pyramid_writer.write_chunk(chunk.astype(dtype),
                                           info["scales"][0]["key"],
                                           chunk_coords)
                progress_bar.update()


def matrix_as_compact_urlsafe_json(matrix):
    # Transform tre matrix, transforming numbers whose floating-point
    # representation has a training .0 to integers
    array = [[int(x) if str(x).endswith(".0") and int(x) == x
              else x for x in row] for row in matrix]
    return json.dumps(array, indent=None, separators=('_', ':'))


def volume_file_to_raw_chunks(volume_filename,
                              dest_url,
                              generate_info=False,
                              ignore_scaling=False,
                              input_min=None,
                              input_max=None,
                              load_full_volume=False,
                              options={}):
    """Convert from neuro-imaging formats to pre-computed raw chunks"""
    img = nibabel.load(volume_filename)
    shape = img.header.get_data_shape()

    proxy = img.dataobj
    if ignore_scaling:
        proxy._slope = 1.0
        proxy._inter = 0.0

    if input_max is not None:
        # In case scaling is used, usually the result will be provided by
        # nibabel as float64
        input_dtype = np.dtype(np.float64)
    else:
        # There is no guarantee that proxy.dtype exists, so we have to
        # read a value from the file to see the result of the scaling
        zero_index = tuple(0 for _ in shape)
        input_dtype = proxy[zero_index].dtype

    logging.info("Input image shape is %s", shape)
    affine = img.affine
    voxel_sizes = nibabel.affines.voxel_sizes(affine)
    logging.info("Input voxel size is %s mm", voxel_sizes)

    logging.info("Detected input axis orientations %s+",
                 "".join(nibabel.orientations.aff2axcodes(affine)))

    if generate_info:
        if input_dtype.name in NG_DATA_TYPES:
            guessed_dtype = input_dtype.name
        else:
            guessed_dtype = "float32"
        header_info = """\
{{
    "num_channels": {num_channels},
    "data_type": "{data_type}",
    "scales": [
        {{
            "encoding": "raw",
            "size": {size},
            "resolution": {resolution},
            "voxel_offset": [0, 0, 0]
        }}
    ]
}}""".format(num_channels=shape[3] if len(shape) >= 4 else 1,
             data_type=guessed_dtype,
             size=list(shape[:3]),
             resolution=[vs * 1000000 for vs in voxel_sizes[:3]])

        info = json.loads(header_info)  # ensure well-formed JSON
        print(header_info)
        dest_dir = convert_file_url_to_pathname(dest_url)
        try:
            os.makedirs(dest_dir, exist_ok=True)
            with open(os.path.join(dest_dir, "info_fullres.json"), "w") as f:
                f.write(header_info)
        except OSError as exc:
            logging.critical("cannot write info_fullres.json to {0}: {1}"
                             .format(dest_dir, exc))
            return 1
        logging.info("The metadata above was written to info_fullres.json. "
                     "Please run generate_scales_info.py on that file "
                     "to generate the 'info' file, then run this program "
                     "again.")

        # We need to take the voxel scaling out of img.affine, and convert the
        # translation part from millimetres to nanometres.
        transform = np.empty((4, 4))
        transform[:, 0] = affine[:, 0] / voxel_sizes[0]
        transform[:, 1] = affine[:, 1] / voxel_sizes[1]
        transform[:, 2] = affine[:, 2] / voxel_sizes[2]
        transform[:3, 3] = affine[:3, 3] * 1000000
        transform[3, 3] = 1
        # Finally, compensate the half-voxel shift which is due to the
        # different conventions of Nifti and Neuroglancer.
        transform = nifti_to_neuroglancer_transform(
            transform, np.asarray(info["scales"][0]["resolution"]))
        json_transform = [list(row) for row in transform]
        try:
            with open(os.path.join(dest_dir, "transform.json"), "w") as f:
                json.dump(json_transform, f)
        except OSError as exc:
            logging.error("cannot write transform.json to {0}: {1}"
                          .format(dest_dir, exc))
        logging.info("Neuroglancer transform of the converted volume "
                     "(written to transform.json):\n%s",
                     matrix_as_compact_urlsafe_json(json_transform))

        if input_dtype.name not in NG_DATA_TYPES:
            logging.error("The %s data type is not supported by Neuroglancer. "
                          "float32 was set, please adjust if needed "
                          "(data_type must be one of %s). The values will be "
                          "rounded (if targeting an integer type) and cast "
                          "during the conversion.",
                          input_dtype.name, NG_DATA_TYPES)
            # return code indicating that manual intervention is needed
            return 4
        # return code indicating that ready-to-use info was output
        return 0

    accessor = neuroglancer_scripts.accessor.get_accessor_for_url(
        dest_url, options)
    try:
        info = accessor.fetch_info()
    except neuroglancer_scripts.accessor.DataAccessError as exc:
        logging.error("No 'info' file was found in the current directory "
                      "({0}). You can generate one by running this program "
                      "with the --generate-info option, then using "
                      "generate_scales_info.py on the result"
                      .format(exc))
        return 1
    except ValueError as e:  # TODO use specific exception for invalid JSON
        logging.error("Invalid 'info' file: {0}".format(e))
        return 1

    output_dtype = np.dtype(info["data_type"])
    info_voxel_sizes = 0.000001 * np.asarray(info["scales"][0]["resolution"])
    if not np.allclose(voxel_sizes, info_voxel_sizes):
        logging.warning("voxel size is inconsistent with resolution in the "
                        "info file(%s nm)", info_voxel_sizes)

    if not np.can_cast(input_dtype, output_dtype, casting="safe"):
        logging.warning("The volume has data type %s, but chunks will be "
                        "saved with %s. You should make sure that the cast "
                        "does not lose range/accuracy.",
                        input_dtype.name, output_dtype.name)

    # Scaling according to --input-min and --input-max. We modify the
    # slope/inter values used by Nibabel rather than re-implementing
    # post-scaling of the read data, in order to benefit from the clever
    # handling of data types by Nibabel
    if np.issubdtype(output_dtype, np.integer):
        output_min = np.iinfo(output_dtype).min
        output_max = np.iinfo(output_dtype).max
    else:
        output_min = 0.0
        output_max = 1.0
    if input_max is not None:
        if input_min is None:
            input_min = 0
        postscaling_slope = (output_max - output_min) / (input_max - input_min)
        postscaling_inter = output_min - input_min * postscaling_slope
        prescaling_slope = proxy.slope
        prescaling_inter = proxy.inter
        proxy._slope = prescaling_slope * postscaling_slope
        proxy._inter = prescaling_inter * postscaling_slope + postscaling_inter

    # Transformations applied to the voxel values
    # TODO put this in the library, for re-use in convert_chunks.py
    round_to_nearest = (
        np.issubdtype(output_dtype, np.integer)
        and not np.issubdtype(input_dtype, np.integer))
    if round_to_nearest:
        logging.warning("Values will be rounded to the nearest integer")

    clip_values = (
        np.issubdtype(output_dtype, np.integer)
        and not np.can_cast(input_dtype, output_dtype, casting="safe"))
    if clip_values:
        logging.warning("Values will be clipped to the range [%s, %s]",
                        output_min, output_max)

    def chunk_transformer(chunk):
        if round_to_nearest:
            np.rint(chunk, out=chunk)
        if clip_values:
            np.clip(chunk, output_min, output_max, out=chunk)
        return chunk.astype(output_dtype)

    if load_full_volume:
        logging.info("Loading full volume to memory... ")
        volume = img.get_data()
    else:
        volume = proxy
    logging.info("Writing chunks... ")
    pyramid_writer = neuroglancer_scripts.pyramid_io.PrecomputedPyramidIo(
        info, accessor, encoder_params=options)
    volume_to_raw_chunks(pyramid_writer, volume,
                         chunk_transformer=chunk_transformer)


def parse_command_line(argv):
    """Parse the script's command line."""
    import argparse
    parser = argparse.ArgumentParser(
        description="""\
Convert a volume from Nifti to Neuroglancer pre-computed format

Chunks are saved with the same data orientation as the input volume.

The image values will be scaled (additionally to any slope/intercept scaling
defined in the file header) if --input-max is specified. If --input-min is
omitted, it is assumed to be zero.
""")
    parser.add_argument("volume_filename",
                        help="source Nifti file containing the data")
    parser.add_argument("dest_url", help="directory/URL where the converted "
                        "dataset will be written")

    parser.add_argument("--generate-info", action="store_true",
                        help="generate an 'info_fullres.json' file containing "
                        "the metadata read for this volume, then exit")

    group = parser.add_argument_group("Option for reading the input file")
    group.add_argument("--ignore-scaling", action="store_true",
                       help="read the values as stored on disk, without "
                       "applying the data scaling (slope/intercept) from the "
                       "volume header")
    group.add_argument("--load-full-volume", action="store_true",
                       help="load full volume to memory. "
                       "This will significantly speed up the conversion if "
                       "the volume is small enough to fit into the system "
                       "memory")

    # TODO split into a module
    group = parser.add_argument_group(
        "Options for data type conversion and scaling")
    group.add_argument("--input-min", type=float, default=None,
                       help="input value that will be mapped to the minimum "
                       "output value")
    group.add_argument("--input-max", type=float, default=None,
                       help="input value that will be mapped to the maximum "
                       "output value")

    neuroglancer_scripts.accessor.add_argparse_options(parser)
    neuroglancer_scripts.chunk_encoding.add_argparse_options(parser,
                                                             allow_lossy=False)

    args = parser.parse_args(argv[1:])

    if args.input_max is None and args.input_min is not None:
        parser.error("--input-min cannot be specified if --input-max is "
                     "omitted")

    return args


def main(argv=sys.argv):
    """The script's entry point."""
    args = parse_command_line(argv)
    return volume_file_to_raw_chunks(args.volume_filename,
                                     args.dest_url,
                                     generate_info=args.generate_info,
                                     ignore_scaling=args.ignore_scaling,
                                     input_min=args.input_min,
                                     input_max=args.input_max,
                                     load_full_volume=args.load_full_volume,
                                     options=vars(args)) or 0


if __name__ == "__main__":
    sys.exit(main())
