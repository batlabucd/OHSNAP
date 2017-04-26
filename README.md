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

The species tree (`data/species.tfl`) is a phylogenetic tree of all species in Newick format (http://scikit-bio.org/docs/0.4.2/generated/skbio.io.format.newick.html) that are present in the alignments.

The `phy` directory is a directory of gene alignment files in Phylip format (http://scikit-bio.org/docs/0.2.3/generated/skbio.io.phylip.html), with each file named after the gene and with the extension `.phy`. The sequence ID of each sequence in an alignment is the name of a species present in the species tree (`data/species.tfl`).


