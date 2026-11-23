#!/usr/bin/env python3
"""Copy the entry image to the output directory.

The grader runs this program twice; both runs must write the same bytes.
The image itself is drawn by render.py and shipped in this repository.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main():
    os.makedirs(OUT, exist_ok=True)
    dst = os.path.join(OUT, "entry.png")
    shutil.copyfile(SRC, dst)
    size = os.path.getsize(dst)
    print("wrote " + dst + " (" + str(size) + " bytes)")


if __name__ == "__main__":
    main()
