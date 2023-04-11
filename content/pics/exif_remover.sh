#!/bin/sh

exiftool -all= . &&
rm -f *.jpg_original
