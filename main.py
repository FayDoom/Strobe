#!/usr/bin/env python
import argparse

from lib.strobe import Strobe


def main(connectorName, platform):
    strobe = Strobe(connectorName, platform)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--platform",
        type=str,
        default="windows",
        help="Specify platform (currently: windows, linux or freebsd, others WiP)",
    )
    parser.add_argument(
        "-s",
        "--source",
        type=str,
        default="meteosat11",
        help="Image connector name. Available : meteosat11, himawari8 (default : meteosat11)",
    )
    args = parser.parse_args()
    main(args.source, args.platform)
