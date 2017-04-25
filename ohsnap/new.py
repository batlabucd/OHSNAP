from ohsnap.util import mkdir_p
import argparse
import os
import os.path
import pkg_resources


parser = argparse.ArgumentParser()
parser.add_argument('output_path', help='Create a new OHSNAP project at this path')


project_dirs = [ 'branch_lbls', 'models', 'phy' ]


def ohsnap_new(project_path):
	"""Create a new empty project at project_path."""
	if os.path.isdir(project_path):
		raise FileExistsError('Cannot create project, path {0} exists'.format(project_path))
	for dir_ in project_dirs:
		mkdir_p(os.path.join(project_path, dir_))
	snakefile = pkg_resources.resource_filename('ohsnap', 'snakemake/Snakefile')
	configfile = pkg_resources.resource_filename('ohsnap', 'snakemake/proj.config')
	shutil.copy(snakefile, os.path.join(project_path, 'Snakefile'))
	shutil.copy(configfile, os.path.join(project_path, 'proj.config'))
	
	
def main():
	args = parser.parse_args()
	ohsnap_new(args.output_path)
	
	
	