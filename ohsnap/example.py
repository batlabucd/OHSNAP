from ohsnap.new import ohsnap_new
from ohsnap.util import mkdir_p
import argparse
import os
import os.path
import pkg_resources
import shutil


parser = argparse.ArgumentParser()
parser.add_argument('output_path', help='Create an example OHSNAP project at this path')


data_dirs = ['branch_lbls', 'data', 'models', 'phy']


def ohsnap_example(project_path):
	"""Copy example data into a new project."""
	configfile = pkg_resources.resource_filename('ohsnap', 'example/proj.config')
	shutil.copy(configfile, os.path.join(project_path, 'proj.config'))
	#copy the data files in data_dirs
	for data_dir in data_dirs:
		pkg_dir = pkg_resources.resource_filename('ohsnap', os.path.join('example', data_dir))
		mkdir_p(os.path.join(project_path, data_dir))
		for data_file in os.listdir(pkg_dir):
			pkg_file = pkg_resources.resource_filename('ohsnap', os.path.join('example', \
				data_dir, data_file))
			shutil.copy(pkg_file, os.path.join(project_path, data_dir, data_file))


def main():
	args = parser.parse_args()
	ohsnap_new(args.output_path)
	ohsnap_example(args.output_path)
	
	
	