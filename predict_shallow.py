import argparse
from glob import glob

"""
Create a non-deep learning classifier (e.g. multiclass SVM, decision tree, random forest)
to perform activity detection that improves upon your prior algorithm.

Usage:
    
    python3 predict_shallow.py <IMU .txt sample>

    python3 predict_shallow.py --label_folder <folder with IMU .txt samples>
"""


def predict_shallow(imu_data):
    """Run prediction on an IMU data sample.

    Replace the return value of this function with the output activity label
    of your shallow classifier for the given sample. Feel free to load any files and write
    helper functions as needed.
    """
    return "JOG"


def predict_shallow_folder(data_folder, output):
    """Run the model's prediction on all the IMU data in data_folder, writing labels
    in sequence to an output text file."""

    data_files = sorted(glob(f"{data_folder}/*.txt"))
    labels = map(predict_shallow, data_files)

    with open(output, "w+") as output_file:
        output_file.write("\n".join(labels))


if __name__ == "__main__":
    # Parse arguments to determine whether to predict on a file or a folder
    # You should not need to modify the below starter code, but feel free to
    # add more arguments for debug functions as needed.
    parser = argparse.ArgumentParser()

    sample_input = parser.add_mutually_exclusive_group(required=True)
    sample_input.add_argument(
        "sample", nargs="?", help="A .txt IMU data file to run predictions on"
    )
    sample_input.add_argument(
        "--label_folder",
        type=str,
        required=False,
        help="Folder of .txt data files to run predictions on",
    )

    parser.add_argument(
        "--output",
        type=str,
        default="test-labels-shallow.txt",
        help="Output filename of labels when running predictions on a directory",
    )

    args = parser.parse_args()

    if args.sample:
        print(predict_shallow(args.sample))

    elif args.label_folder:
        predict_shallow_folder(args.label_folder, args.output)
