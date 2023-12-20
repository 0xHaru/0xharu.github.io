#!/usr/bin/env python

import glob

import exif


def main():
    noexif = True
    images = glob.glob("./**/*.jpg", recursive=True)
    print(f"Scanning {len(images)} images...")

    for path in images:
        with open(path, "rb") as f:
            im = exif.Image(f)

        if im.has_exif:
            noexif = False
            print(f"{path} has EXIF data")

    if noexif:
        print(f"None of the {len(images)} images has EXIF data")


if __name__ == "__main__":
    main()
