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
    parser.add_argument("img_dir", help="Path to dynamic image directory")
    parser.add_argument("roi_path", help="Path to ROI-file")
    parser.add_argument("out_path", help="Path to write output file")
    parser.add_argument("--resample", choices=['roi', 'img'],
                        help="Resample either the ROI or the images to the "
                             "physical space of the other")
    parser.add_argument("--labels", nargs="*",
                        help="New labels to print in out file")
    parser.add_argument("--ignore", nargs="*",
                        help="List of labels to ignore")
    args = parser.parse_args(sys_args)

    # Handle list of labels:
    labels = None
    if args.labels is not None:
        labels = {}
        for label_string in args.labels:
            roi_label, new_label = label_string.split(',')
            labels[roi_label] = new_label

    dyn = tictac.series_roi_means(
        series_path=args.img_dir,
        roi_path=args.roi_path,
        resample=args.resample,
        labels=labels,
        ignore=args.ignore)
    tictac.save_table(table=dyn, path=args.out_path)

    run_time = (time.time_ns() - start_time) * 1e-9
    print(f'TICTAC finished in {run_time:.1f} seconds.')
    print()


if __name__ == "__main__":
    main(sys.argv[1:])
