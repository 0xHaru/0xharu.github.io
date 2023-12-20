#!/usr/bin/env python

import glob
import os
import re


def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split("([0-9]+)", key)]
    return sorted(l, key=alphanum_key)


def main():
    base_path = os.path.dirname(os.path.abspath(__file__))

    files = glob.glob(f"{base_path}/*.jpg")
    files = natural_sort(files)

    i = 0

    for path in files:
        new_path = path.rsplit("/")[:-1]
        new_path = "/".join(new_path)
        new_path = f"{new_path}/{i}.jpg"
        os.rename(path, new_path)
        i += 1


if __name__ == "__main__":
    main()
