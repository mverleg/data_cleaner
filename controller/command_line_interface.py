
"""
	Command-line interface
"""

from argparse import ArgumentParser


parser = ArgumentParser(description = 'Reads operations from a json file and applies them to data row-by-row.')
parser.add_argument('ops', help = 'The operations file (json) for the transformations.')
parser.add_argument('data', help = 'The data to apply transformations to.')
args = parser.parse_args()
print(args)


