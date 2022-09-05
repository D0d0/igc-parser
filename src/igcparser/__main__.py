import argparse
import pathlib

from igcparser.cli import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse IGC file.")
    parser.add_argument("file_path", type=pathlib.Path, help="Path to an IGC file")

    args = parser.parse_args()
    main(args)
