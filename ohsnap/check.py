import argparse
import os
import subprocess
import sys


parser = argparse.ArgumentParser()
parser.add_argument('project_directory', nargs='?', default=os.getcwd(), \
	help='Perform a dry run check on the OHSNAP project at this path (default: current directory)')


def ohsnap_check(project_directory):
	"""Performs a dry run check on the OHSNAP project in project_directory."""
	subprocess.call('snakemake -n', cwd=project_directory, shell=True)


def main():
	args = parser.parse_args()
	ohsnap_check(args.project_directory)

	
