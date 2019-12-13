#!/usr/bin/env python
import argparse

from lib.strobe import Strobe
from lib.utils import Utils


def main(source_name, platform, max_size):
    Utils.set_screen_size(max_size)
    Strobe(source_name, platform)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--platform",
        type=str,
        default="windows",
        help="Specify platform. Available : windows, linux or freebsd, others WiP (default : windows)",
    )
    parser.add_argument(
        "-s",
        "--source",
        type=str,
        default="meteosat11",
        help="Image source name. Available : meteosat11, himawari8, europe"
        "(default : meteosat11)",
    )
    parser.add_argument(
        "-r",
        "--resolution",
        type=str,
        default="1920x1080",
        help="Wallpaper maximum resolution e.g.: 1440x900. (default: 1920x1080)",
    )
    args = parser.parse_args()
    main(args.source, args.platform, args.resolution)
