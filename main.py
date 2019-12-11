#!/usr/bin/env python
from lib.strobe import Strobe
import argparse



def main(connecterName):
	strobe = Strobe(connecterName)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--source", type=str, default='meteosat11',help="Image connecter name. Available : meteosat11, himawari8 (default : meteosat11)")
	args = parser.parse_args()
	main(args.source)
