#!/usr/bin/env python3
import os
from pathlib import Path
import argparse


if __name__ == '__main__':
    # parse inputs
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, help="which model to download")
    args = parser.parse_args()

    # default folder
    MAINPATH = f"{str(Path.home())}/flexion_data"

    # Download Schmid's SMOR transducer (2005)
    # see https://www.cis.uni-muenchen.de/~schmid/tools/SMOR/
    if args.model == "smor":
        PATH = f"{MAINPATH}/smor"
        URL = "https://www.cis.uni-muenchen.de/~schmid/tools/SMOR/data/"
        ZIPFILE = "SMOR-linux.zip"
        os.makedirs(PATH, exist_ok=True)
        os.system(f"wget -O '{PATH}/{ZIPFILE}' '{URL}/{ZIPFILE}'")
        os.system(f"unzip -o -d '{PATH}' '{PATH}/{ZIPFILE}'")
        os.system(f"rm '{PATH}/{ZIPFILE}'")
