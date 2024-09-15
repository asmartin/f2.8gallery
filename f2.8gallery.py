#!/usr/bin/python3
import argparse
import datetime
import os
import re
import shutil
import sys
import urllib
from jinja2 import Environment, FileSystemLoader
from pprint import pprint
from jinja2 import Environment, PackageLoader
from urllib.request import urlretrieve

# PIL may be installed as "Pil" or similar on case-insensitive filesytems
try:
    from PIL import Image
except ImportError:
    try:
        from Pil import Image
    except ImportError:
        from pil import Image

def regex_replace(s, find, replace):
    """Implement a regex filter for jinja2"""
    return re.sub(find, replace, s)


def create_if_not_exists(dir):
    """Create a directory if it does not exist"""
    if not os.path.isdir(dir):
        os.mkdir(path=dir, mode=0o755)


def main():
    parser = argparse.ArgumentParser(description="f2.8gallery static site generator")
    parser.add_argument(
        "-c",
        "--clean",
        help="Clean the output directory before building",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "-t",
        "--title",
        help="Title of the site",
        required=False,
        default="John Smith's Portfolio",
    )
    parser.add_argument(
        "-a",
        "--author",
        help="Name of the photographer",
        required=False,
        default="John Smith",
    )
    parser.add_argument(
        "-w",
        "--thumbwidth",
        help="Width of thumbnails in the gallery (in pixels)",
        required=False,
        default=400,
        type=int,
    )
    parser.add_argument(
        "-d",
        "--debug",
        help="Enable debug messages",
        required=False,
        action="store_true",
    )
    parser.add_argument("galleries", help="Path to the input directory of galleries")
    parser.add_argument(
        "output",
        help="Path to the directory where the output files should be generated",
    )
    args = parser.parse_args()

    if args.clean is not None and args.clean:
        print(f"cleaning {args.output}")
        shutil.rmtree(args.output, ignore_errors=True)

    if not os.path.isdir(args.galleries):
        print(f"Error: cannot find galleries directory: {args.galleries}")
        sys.exit(1)

    # create necessary directories if they don't exist
    create_if_not_exists(args.output)
    thumbnails_dir = f"{args.output}/thumbnails"
    create_if_not_exists(thumbnails_dir)
    create_if_not_exists(f"{args.output}/assets")
    create_if_not_exists(f"{args.output}/assets/img")
    create_if_not_exists(f"{args.output}/assets/js")
    create_if_not_exists(f"{args.output}/assets/css")
    create_if_not_exists(f"{args.output}/assets/css/font")

    shutil.copytree(args.galleries, f"{args.output}/galleries", dirs_exist_ok=True)
    shutil.copytree("assets/img", f"{args.output}/assets/img", dirs_exist_ok=True)
    shutil.copytree("assets/css", f"{args.output}/assets/css", dirs_exist_ok=True)
    shutil.copytree("assets/root", f"{args.output}", dirs_exist_ok=True)

    thumbnail_size_scaled_up = (
        args.thumbwidth * 1.2
    )  # comes from "scale120" hover effect
    thumbnail_wh = (thumbnail_size_scaled_up, thumbnail_size_scaled_up)
    gallery_names = []
    galleries = {}

    print("generating thumbnails")
    gallery_paths = [x[0] for x in os.walk(args.galleries)]
    for path in gallery_paths:
        if path != args.galleries:
            gallery_name = path.split("/")[-1]
            thumbnail_dir = f"{thumbnails_dir}/{gallery_name}"
            galleries[gallery_name] = {}
            galleries[gallery_name]["gallery_dir"] = path
            galleries[gallery_name]["thumbnail_dir"] = thumbnail_dir
            galleries[gallery_name]["files"] = []
            create_if_not_exists(thumbnail_dir)
            for file in os.listdir(path):
                gallery_names.append(gallery_name)
                galleries[gallery_name]["files"].append(file)
                thumbnail = f"{thumbnail_dir}/{file}"
                if not os.path.isfile(thumbnail):
                    if args.debug:
                        print(f"Creating thumbnail for {file} as {thumbnail}")
                    image = Image.open(f"{path}/{file}")
                    image.thumbnail(thumbnail_wh)
                    image.save(thumbnail)

    if args.debug:
        pprint(galleries)

    print("generating HTML page")
    env = Environment(loader=FileSystemLoader("."))
    env.filters["regex_replace"] = regex_replace
    template = env.get_template("index.j2")
    index = open(f"{args.output}/index.html", "w")
    index.write(
        template.render(
            webpage_name=args.title,
            author=args.author,
            thumbwidth=args.thumbwidth,
            now=datetime.datetime.now(),
            base=args.galleries,
            galleries=galleries,
            output=args.output,
        )
    )
    index.close()

    print("downloading required libraries")
    urlretrieve(
        "https://code.jquery.com/jquery-3.7.1.slim.min.js",
        f"{args.output}/assets/js/jquery.min.js",
    )
    urlretrieve(
        "https://raw.githubusercontent.com/nanostudio-org/nanogallery2/master/dist/css/nanogallery2.min.css",
        f"{args.output}/assets/css/nanogallery2.min.css",
    )
    urlretrieve(
        "https://raw.githubusercontent.com/nanostudio-org/nanogallery2/master/dist/jquery.nanogallery2.min.js",
        f"{args.output}/assets/js/jquery.nanogallery2.min.js",
    )
    urlretrieve(
        "https://raw.githubusercontent.com/kylefox/jquery-modal/v0.9.1/jquery.modal.min.js",
        f"{args.output}/assets/js/jquery.modal.min.js",
    )
    urlretrieve(
        "https://raw.githubusercontent.com/kylefox/jquery-modal/v0.9.1/jquery.modal.min.css",
        f"{args.output}/assets/css/jquery.modal.min.css",
    )
    urlretrieve(
        "https://cdn.jsdelivr.net/npm/purecss@3.0.0/build/pure-min.css",
        f"{args.output}/assets/css/pure-min.css",
    )
    urlretrieve(
        "https://cdn.jsdelivr.net/npm/purecss@3.0.0/build/grids-responsive-min.css",
        f"{args.output}/assets/css/grids-responsive-min.css",
    )
    urlretrieve(
        "https://github.com/nanostudio-org/nanogallery2/raw/master/dist/css/font/ngy2_icon_font.woff",
        f"{args.output}/assets/css/font/ngy2_icon_font.woff",
    )
    urlretrieve(
        "https://github.com/nanostudio-org/nanogallery2/raw/master/dist/css/font/ngy2_icon_font.woff2",
        f"{args.output}/assets/css/font/ngy2_icon_font.woff2",
    )
    print(f"site successfully generated at {args.output}!")


if __name__ == "__main__":
    main()
