# OHSNAP
OHSNAP (**O**ptimised **H**igh-throughput **Sn**akemake **A**utomisation of **P**AML) is a software tool built using the Snakemake workflow management system to automate and massively parellalise the execution of CodeML.

## Requirements
- Mac/UNIX/Linux OS
- Git
- Python 3 (https://www.python.org/download/releases/3.0/)
- Snakemake (https://bitbucket.org/snakemake/snakemake/wiki/Home)
- Biopython (http://biopython.org/)
- PAML (http://abacus.gene.ucl.ac.uk/software/paml.html)

Optional, recommended:
- A cluster environment with a batch execution system like PBS, Torque, Open Grid Engine etc.

## Installation
Install Git, Python 3 and PAML, if necessary. Download OHSNAP and install:

```
git clone https://github.com/batlabucd/OHSNAP.git
cd OHSNAP
python3 setup.py install
```

This will also install the Snakemake and BioPython dependencies.

## Creating an example project
You can create an example project with the following command:

```
ohsnap_example <project_path>
```

This will create the following files and directories:

```
<project_path>
  \branch_lbls
    myotis.txt
    nmr.txt
  \data
    species.tfl
  \models
    alt.mod
    CladeModelC.mod
    M2aRel.mod
    null.mod
  \phy
    CBX1.phy
    CBX3.phy
    CHEK2.phy
    MEI4.phy
  proj.config
  Snakefile
```

## Explaining the inputs

The species tree (`data/species.tfl`) is a phylogenetic tree of all species present in the analysis in Newick format (http://scikit-bio.org/docs/0.4.2/generated/skbio.io.format.newick.html).

`branch_lbls` is a directory of `.txt` files, each containing a comma-separated list of species to be used for branch labelled models. In each case, the species tree (`data/species.tfl`) is searched with the list of species for the first common ancestor clade and labelled.

`models` is a directory of CodeML control file templates for each model to be run. An example model file is here: https://github.com/batlabucd/OHSNAP/blob/master/ohsnap/example/models/CladeModelC.mod. These control file templates contain placeholders e.g. `{phy_fn}`, `{mod}`, `{out_dir}`, that are given values by OHSNAP during run time and should be present in all model files.

The `phy` directory is a directory of gene alignment files in Phylip format (http://scikit-bio.org/docs/0.2.3/generated/skbio.io.phylip.html), with each file named after the gene and with the extension `.phy`. The sequence ID of each sequence in an alignment is the name of a species present in the species tree (`data/species.tfl`).

The `proj.config` file is a project configuration file. Here is a template:

```
{
  "branchlbl_dir": "branch_lbls/",
  "labelled_models": [],
  "mod_dir": "models/",
  "phy_dir": "phy/",
  "species_tree": ""
}
```

The `branchlbl_dir`, `mod_dir` and `phy_dir` give the paths to the `branch_lbls`, `models` and `phy` directories explained above and don't need to changed if the default directory locations are used. `labelled_models` is a list of models (filenames without the `.mod` file extension) that require branch labels e.g. `"labelled_models": ["alt", "null", "CladeModelC"],`. Lastly, `species_tree` is the path to the Newick tree of all species explained above i.e. `species_tree: "data/species.tfl`.

`Snakefile` is the `snakemake` workflow file that is executed when running a project.




