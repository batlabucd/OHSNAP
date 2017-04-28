import argparse
import os
import subprocess
import sys


parser = argparse.ArgumentParser()
parser.add_argument('--num_threads', default=1, \
	help='The maximum number of threads to use for local job execution (default: 1)')
parser.add_argument('project_directory', nargs='?', default=os.getcwd(), \
	help='Run the OHSNAP project at this path locally (default: current directory)')


def ohsnap_runlocal(project_directory, num_threads):
	"""Execute the OHSNAP project in project_directory on a local machine. The num_threads 
		parameter is the maximum number of threads to use."""
	cmd = 'snakemake -j {threads}'.format(threads=num_threads)
	subprocess.call(cmd, cwd=project_directory, shell=True)


def main():
	args = parser.parse_args()
	ohsnap_runlocal(args.project_directory, args.num_threads)

	
