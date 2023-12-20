#!/usr/bin/env python

import glob
import os
import re
import shlex
import shutil
import subprocess


def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split("([0-9]+)", key)]
    return sorted(l, key=alphanum_key)


def gen_pics_dot_html():
    """Generates pics.html"""

    def get_subdirs(dirpath):
        subdirs = [f.path for f in os.scandir(dirpath) if f.is_dir()]
        return natural_sort(subdirs)

    def get_relative_filepaths(globpath, sep):
        files = glob.glob(globpath)
        files = [f"/{sep}{f.rsplit(sep)[1]}" for f in files]
        return natural_sort(files)

    html = """<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Pics | 0xHaru</title>
    <link
      rel="stylesheet"
      href="https://fonts.googleapis.com/css?family=Noto%20Serif"
    />
    <!-- https://www.flaticon.com/free-icon/lambda_7288373 -->
    <link rel="shortcut icon" type="image/png" href="favicon.png" />
    <style>
      body {
        font-family: "Noto Serif", serif;
        font-size: 16px;
        margin: 2em auto;
        max-width: 800px;
      }

      img {
        object-fit: cover;
        width: 240px;
        height: 180px;
      }

      a {
        text-decoration: none;
      }

      div {
        text-align: center;
      }

      h1 {
        font-size: 2em;
      }
    </style>
  </head>
  <body>
    <div>"""

    pics_subdirs = get_subdirs(f"docs/pics")
    thumb_subdirs = get_subdirs(f"docs/thumbnails")

    for ps, ts in zip(pics_subdirs, thumb_subdirs):
        dirname = ps.rsplit("/")[-1]
        html += f"\n      <h1>{dirname}</h1>"

        pics = get_relative_filepaths(f"{ps}/*.jpg", "pics")
        thumbnails = get_relative_filepaths(f"{ts}/*.jpg", "thumbnails")

        for p, t in zip(pics, thumbnails):
            html += f'\n      <a href="{p}" target="_blank"> <img src="{t}"> </a>'

    html += "\n    </div>"
    html += "\n  </body>"
    html += "\n</html>"

    with open("docs/pics/index.html", "w") as f:
        f.write(html)


def pandoc(f):
    """Invokes Pandoc from the command line to convert a Markdown file to HTML"""

    extension = f.rsplit(".")[-1]
    assert extension == "md"

    relative_filepath = "/".join(f.split("/")[1:])  # Extract relative path
    relative_filepath = relative_filepath.rsplit(".")[0]  # Remove file extension

    subprocess.run(
        shlex.split(
            f"pandoc --from markdown --to html5 --standalone "
            f"--include-in-header common/header.html "
            f"--include-before-body common/body.html "
            f"--css /style.css "
            f"--output docs/{relative_filepath}.html {f}"
        )
    )


def main():
    # Create a new docs directory from scratch
    if os.path.isdir("docs"):
        shutil.rmtree(f"docs")
    shutil.copytree(f"static", f"docs")

    # Mimic the directory structure of content/ in docs/
    content_subdirs = glob.glob(f"content/**/", recursive=True)
    content_subdirs.remove("content/")

    for d in content_subdirs:
        d = d.replace("content", "docs", 1)
        if not os.path.isdir(d):
            os.makedirs(d)

    # Create .nojekyll in docs/
    with open("docs/.nojekyll", "w"):
        pass

    markdown_files = glob.glob(f"content/**/*.md", recursive=True)
    for f in markdown_files:
        pandoc(f)

    gen_pics_dot_html()


if __name__ == "__main__":
    main()
