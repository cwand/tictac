import argparse
import tictac
import sys
import importlib.metadata
import time


def main(sys_args: list[str]):

    # Get version number from pyproject.toml
    __version__ = importlib.metadata.version("tictac")
    start_time = time.time_ns()

    print("Starting TICTAC", __version__)
    print()

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", metavar="IMG_PATH",
                        help="Path to dynamic image data",
                        required=True)
    parser.add_argument("-o", metavar="OUT_PATH",
                        help="Output path",
                        required=True)
    parser.add_argument("--roi", nargs=4, action="append",
                        metavar=("PATH", "VOX_VALUE", "LABEL", "RESAMPLE"),
                        help="Define a ROI to extract. PATH is the path to "
                             "the ROI-file. VOX_VALUE is the value of the ROI "
                             "voxels in the file. LABEL is the name of the "
                             "ROI in the output file. RESAMPLE states whether "
                             "to resample either the ROI or the image data "
                             "before extraction (possible values are 'img', "
                             "'roi' or 'none'.")
    parser.add_argument("--scale", action='append', nargs=3,
                        metavar=("label_in", "label_out", "factor"),
                        help="Apply a scale factor to label_in and save it "
                             "as label_out")
    args = parser.parse_args(sys_args)

    # Run ROI-means code
    dyn = tictac.series_roi_means(
        series_path=args.i,
        roi_list=args.roi)

    # Apply scales if required
    if args.scale:
        for scale in args.scale:
            factor = float(scale[2])
            scaled_arr = factor * dyn[scale[0]]
            dyn[scale[1]] = scaled_arr

    tictac.save_table(table=dyn, path=args.o)

    # Report successful end of program
    run_time = (time.time_ns() - start_time) * 1e-9
    print(f'TICTAC finished successfully in {run_time:.1f} seconds.')
    print()


if __name__ == "__main__":
    main(sys.argv[1:])
