from Bio import Phylo
from Bio.Phylo.Newick import Clade
from snakemake.io import expand
from util import mkdir_p
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
			
	
def get_species_groups(branchlbl_dir):
	"""Return the species group names (basename no extension) for branch label files in 
		branchlbl_dir."""
	basenames = [ os.path.basename(f) if os.path.splitext(f)[1] == '.txt' else None for f in os.listdir(branchlbl_dir) ]
	species_groups = list(map(lambda f: os.path.splitext(f)[0], filter(None, basenames)))
	return species_groups
	
def get_phy_to_group_mapping(branchlbl_dir, phy_dir, phy_ext='.phy'):
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
		if not os.path.splitext(groupfile)[1] == '.txt':
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
	mod_ext='.mod', phy_ext='.phy', out_ext='.out'):
	"""Return the control filenames for a set of models and phy alignment files. If a model 
		requires a labelled branch (i.e. the model name is in the labelled_models list), a 
		control file for each species group present in branchlbl_dir will be generated."""
	lbl_mod_wcs = []
	mod_wcs = []
	for mod in os.listdir(mod_dir):
		name, ext = os.path.splitext(mod)
		if ext == mod_ext and name in labelled_models:
			lbl_mod_wcs.append(name)
		elif ext == mod_ext:
			mod_wcs.append(name)
	phy_wcs = [ os.path.splitext(f)[0] for f in os.listdir(phy_dir) if os.path.splitext(f)[1] == phy_ext ]
	#species_groups = get_species_groups(branchlbl_dir)
	#return expand('{mod}/{phy}/{group}/{phy}.{mod}{ext}', mod=lbl_mod_wcs, phy=phy_wcs, group=species_groups, ext=out_ext) + \
	#	expand('{mod}/{phy}/{phy}.{mod}{ext}', mod=mod_wcs, phy=phy_wcs, ext=out_ext)
	phy_group_map = get_phy_to_group_mapping(branchlbl_dir, phy_dir, phy_ext)
	return expand('{mod}/{phy_group_map}.{mod}{ext}', mod=lbl_mod_wcs, phy_group_map=phy_group_map, ext=out_ext) + \
		expand('{mod}/{phy}/{phy}.{mod}{ext}', mod=mod_wcs, phy=phy_wcs, ext=out_ext)
	
def label_species_tree(input_tree, species_list, output_tree, label='#1', allow_not_found=False):
	"""Label a clade in a species tree that is the common ancestor of all species in 
		species_list. If allow_not_found is False, a ValueError will be raised if a species 
		in species_list is not found in the input_tree."""
	species = []
	with open(species_list) as f:
		species = f.read().strip().split(',')
	tree = None
	with open(input_tree) as f:
		tree = next(Phylo.parse(f, 'newick'))
	clades = []
	not_found = []
	for sp in species:
		try:
			clade = next(tree.find_clades(name=sp))
			clades.append(clade)
		except StopIteration:
			not_found.append(sp)
	if len(not_found) > 0 and not allow_not_found:
		raise ValueError('Cound not find species {0}'.format(not_found))
	elif len(clades) == 0:
		raise ValueError('No species in species_tree found to label.')
	common_anc_clade = tree.common_ancestor(*clades)
	if not common_anc_clade.name is None:
		common_anc_clade = tree.get_path(common_anc_clade)[-2]
	common_anc_clade.name = '#1'
	with open(output_tree, 'w') as o:
		Phylo.write([tree], o, 'newick', plain=True)

def phy_parser(phy):
	"""Parse a phylip formatted file returning a list of tuples of seqname and alignment."""
	num_records = None
	align_length = None
	with open(phy) as f:
		num_records, align_length = list(map(int, filter(None, f.readline().split(' '))))
		records = []
		for i in range(0, num_records):
			seqname = f.readline().strip()
			alignment = ''
			parts = list(filter(None, seqname.split('  ')))
			if len(parts) > 1:
				seqname, alignment = list(map(lambda x: x.strip(), parts))
			while len(alignment) < align_length:
				alignment += f.readline().strip()
				if len(alignment) > align_length:
					break
			if not len(alignment) == align_length:
				raise ValueError(\
					'Sequence name {0}: alignment length is not the expected length ({1})'.format(\
						seqname, align_length))
			records.append((seqname, alignment))
	if not num_records == len(records):
		raise ValueError(\
			'Number of records read ({0}) does not match the number of expected records ({1})'.format(\
				num_records, len(records)))
	return records
	
def prune_species_tree(input_tree, phy, output_tree):
	"""Remove species from input_tree that are not in phy."""
	phy_names = list(map(lambda x: x[0], phy_parser(phy)))
	tree = None
	with open(input_tree) as f:
		tree = next(Phylo.parse(f, 'newick'))
	for element in tree.find_elements():
		if not isinstance(element, Clade):
			continue
		elif not element.name is None and not element.name in phy_names:
			tree.prune(element)
	with open(output_tree, 'w') as o:
		Phylo.write([tree], o, 'newick', plain=True)
		
def write_control_file(input, output, wildcards):
	"""Generate a CodeML control file."""
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
	
	
