from Bio import Phylo
from Bio.Phylo.Newick import Clade
from snakemake.io import expand
from ohsnap.util import mkdir_p
import os
import os.path


def cmp_anc_phy_names(species_tree, phy):
	"""Check the names in the species tree and make sure they match the names in the phy 
		alignment file."""
	anc_names = []
	with open(species_tree, 'rU') as f:
		formatted = f.read()
		# extract the species names, remove all other notation
		for c in ['(', ')', ';', '#1']:
			formatted = formatted.replace(c, '')
		species_names = list(filter(None, formatted.strip().split(',')))
	# parse the sequence names from the phy file
	phy_names = list(map(lambda x: x[0], phy_parser(phy)))
	# check each species name in the species tree is in the phy file
	for species_name in species_names:
		if not species_name in phy_names:
			raise ValueError('Unknown species name "{0}" {1}'.format(species_name, phy_names))
	# check each sequence name in the phy file is in the species tree
	for phy_name in phy_names:
		if not phy_name in species_names:
			raise ValueError('Unknown phylip name "{0}"'.format(phy_name))
			
	
def get_species_groups(branchlbl_dir, blbl_ext='.txt'):
	"""Return the species group names (basename no extension) for branch label files in 
		branchlbl_dir."""
	# get the .txt files in branchlbl_dir
	basenames = [ os.path.basename(f) if os.path.splitext(f)[1] == blbl_ext else None for f in os.listdir(branchlbl_dir) ]
	# make a list of the filenames without extension
	species_groups = list(map(lambda f: os.path.splitext(f)[0], filter(None, basenames)))
	return species_groups
	
	
def get_phy_to_group_mapping(branchlbl_dir, phy_dir, phy_ext='.phy', blbl_ext='.txt'):
	"""Return a dictionary of species groups to phy mappings, where only phy files that 
		contain at least one species are mapped."""
	map_list = []
	#get a list of phy filenames in the phy directory
	phy_fnames = [ f for f in os.listdir(phy_dir) if os.path.splitext(f)[1] == phy_ext ]
	phy_species = {}
	#get a list of species in each phy file
	for phy_fname in phy_fnames:
		phy_file = os.path.join(phy_dir, phy_fname)
		species = list(map(lambda x: x[0], phy_parser(phy_file)))
		phy_species[os.path.splitext(phy_fname)[0]] = species
	#check each branch label file and create a phy_name/group_name/phy_name mapping if 
	#there's at least one species in the label file present in a phy file
	for groupfile in os.listdir(branchlbl_dir):
		if not os.path.splitext(groupfile)[1] == blbl_ext:
			continue
		group_name = os.path.splitext(groupfile)[0]
		with open(os.path.join(branchlbl_dir, groupfile)) as f:
			group_species = f.readline().strip().split(',')
			for phy_name, phy_species_list in phy_species.items():
				for s in group_species:
					if s in phy_species_list:
						map_list.append(os.path.join(phy_name, group_name, phy_name))
						break
	return map_list
	

def get_output_files_phy_names(branchlbl_dir, mod_dir, phy_dir, labelled_models, \
	mod_ext='.mod', phy_ext='.phy', out_ext='.out', blbl_ext='.txt'):
	"""Return the control filenames for a set of models and phy alignment files. If a model 
		requires a labelled branch (i.e. the model name is in the labelled_models list), a 
		control file for each species group present in branchlbl_dir will be generated."""
	# create and populate the lists of labelled an unlabelled models
	lbl_mod_wcs = []
	mod_wcs = []
	for mod in os.listdir(mod_dir):
		name, ext = os.path.splitext(mod)
		if ext == mod_ext and name in labelled_models:
			lbl_mod_wcs.append(name)
		elif ext == mod_ext:
			mod_wcs.append(name)
	# get the list of phy file names (no extension)
	phy_wcs = [ os.path.splitext(f)[0] for f in os.listdir(phy_dir) if os.path.splitext(f)[1] == phy_ext ]
	# get the phy file name to group mapping, where only phy files that contain at least one species are 
	# present in the map
	phy_group_map = get_phy_to_group_mapping(branchlbl_dir, phy_dir, phy_ext)
	# return the list of output filenames for each model and each phy file, for both labelled 
	# and unlabelled models
	labelled_model_outputs = expand('{mod}/{phy_group_map}.{mod}{ext}', mod=lbl_mod_wcs, \
		phy_group_map=phy_group_map, ext=out_ext)
	unlabelled_model_outputs = expand('{mod}/{phy}/{phy}.{mod}{ext}', mod=mod_wcs, \
		phy=phy_wcs, ext=out_ext)
	return labelled_model_outputs + unlabelled_model_outputs	
		
	
def label_species_tree(input_tree, species_list, output_tree, label='#1', allow_not_found=False):
	"""Label a clade in a species tree that is the common ancestor of all species in 
		species_list. If allow_not_found is False, a ValueError will be raised if a species 
		in species_list is not found in the input_tree."""
	# read the list of species to label
	species = []
	with open(species_list) as f:
		species = f.read().strip().split(',')
	# read the tree file
	tree = None
	with open(input_tree) as f:
		tree = next(Phylo.parse(f, 'newick'))
	# find the clades in the tree that contain each species
	clades = []
	not_found = []
	for sp in species:
		try:
			clade = next(tree.find_clades(name=sp))
			clades.append(clade)
		except StopIteration:
			not_found.append(sp)
	# raise a ValueError if there were species not found and allow_not_found is False or
	# raise a ValueError if no species were found
	if len(not_found) > 0 and not allow_not_found:
		raise ValueError('Cound not find species {0}'.format(not_found))
	elif len(clades) == 0:
		raise ValueError('No species in species_tree found to label.')
	# get the clade common to all clades found
	common_anc_clade = tree.common_ancestor(*clades)
	if not common_anc_clade.name is None:
		common_anc_clade = tree.get_path(common_anc_clade)[-2]
	common_anc_clade.name = label
	with open(output_tree, 'w') as o:
		Phylo.write([tree], o, 'newick', plain=True)
		

def phy_parser(phy):
	"""Parse a phylip formatted file returning a list of tuples of seqname and alignment."""
	num_records = None
	align_length = None
	with open(phy) as f:
		# the first line in the file contains the number of alignments and the length of 
		# each alignment
		num_records, align_length = list(map(int, filter(None, f.readline().split(' '))))
		records = []
		for i in range(0, num_records):
			seqname = f.readline().strip()
			alignment = ''
			# alignment can either start two spaces after the sequence name or on the 
			# next line
			parts = list(filter(None, seqname.split('  ')))
			if len(parts) > 1:
				seqname, alignment = list(map(lambda x: x.strip(), parts))
			while len(alignment) < align_length:
				alignment += f.readline().strip()
				if len(alignment) > align_length:
					break
			# make sure the alignment length is the same as the length given at the start 
			# of the file and raise a ValueError if it is not
			if not len(alignment) == align_length:
				raise ValueError(\
					'Sequence name {0}: alignment length is not the expected length ({1})'.format(\
						seqname, align_length))
			records.append((seqname, alignment))
	# make sure the number of records parsed was the same as the number given at the start 
	# of the file
	if not num_records == len(records):
		raise ValueError(\
			'Number of records read ({0}) does not match the number of expected records ({1})'.format(\
				num_records, len(records)))
	return records
	
	
def prune_species_tree(input_tree, phy, output_tree):
	"""Remove species from input_tree that are not in phy."""
	# get the list of sequence names (named after species)
	phy_names = list(map(lambda x: x[0], phy_parser(phy)))
	# parse the species tree
	tree = None
	with open(input_tree) as f:
		tree = next(Phylo.parse(f, 'newick'))
	# loop through each named clade and make sure it is present in the list of sequence names
	for element in tree.find_elements():
		if not isinstance(element, Clade):
			continue
		elif not element.name is None and not element.name in phy_names:
			tree.prune(element)
	with open(output_tree, 'w') as o:
		Phylo.write([tree], o, 'newick', plain=True)
		
		
def write_control_file(input, output, wildcards):
	"""Generate a CodeML control file from a template and replace variable placeholder 
		with values from Snakemake wildcards."""
	namespace = {}
	namespace.update(vars(wildcards))
	namespace['species_tree_fn'] = os.path.abspath(input.species_tree)
	namespace['mod_fn'] = os.path.abspath(input.mod)
	namespace['phy_fn'] = os.path.abspath(input.phy)
	namespace['out_dir'] = os.path.abspath(os.path.split(output.ctl)[0])
	mkdir_p(namespace['out_dir'])
	with open(input.mod) as f, open(output.ctl, 'wb') as o:
		try:
			ctlstr = f.read().format(**namespace)
			o.write(bytes(ctlstr, 'UTF-8'))
		except KeyError as e:
			print('Unknown key {0} in model file {1}'.format(e, input.mod_file))
			raise
	
	
