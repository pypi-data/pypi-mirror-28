#!/usr/bin/env python3

import os, sys, argparse, logging
import requests

def main():

	parser = argparse.ArgumentParser()

	# hivehome.com credentials
	parser.add_argument("--username", help="hivehome.com username", default=os.getenv("HIVE_USERNAME", ''))
	parser.add_argument("--password", help="hivehome.com password", default=os.getenv("HIVE_PASSWORD", ''))

	# Verbose mode
	parser.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
	args = parser.parse_args()

	if args.verbose:
		logging.basicConfig(level=logging.DEBUG)
	else:
		logging.basicConfig(level=logging.INFO)
	log = logging.getLogger(__name__)

	try:
		assert args.username != ''
		assert args.password != ''
	except AssertionError:
		exit("Missing hivehome.com username or password. Exiting")

if __name__ == '__main__':
	main()