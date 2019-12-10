#!/usr/bin/env python
from lib.strobe import Strobe


def main(connecterName):
	strobe = Strobe(connecterName)

if __name__ == "__main__":
	main('meteosat11') #There is only one connecter yet
