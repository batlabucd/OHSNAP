# OHSNAP
OHSNAP (**O**ptimised **H**igh-throughput **Sn**akemake **A**utomisation of **P**AML) is a software tool built using the [Snakemake](https://bitbucket.org/snakemake/snakemake/wiki/Home) workflow management system to automate and massively parellalise the execution of CodeML. OHSNAP scales effectively from single workstations to large clusters, making efficient use of available resources.

## Requirements
- Mac/UNIX/Linux OS
- Git
- Python 3 (https://www.python.org/download/releases/3.0/)
- Snakemake (https://bitbucket.org/snakemake/snakemake/wiki/Home)
- Biopython (http://biopython.org/)
- PAML (http://abacus.gene.ucl.ac.uk/software/paml.html)

Optional, recommended:
- A cluster environment with a batch execution system like Open Grid Engine (http://gridscheduler.sourceforge.net/), PBS, Torque etc.

## Installation
Install Git, Python 3 and PAML, if necessary. 

*Optional*:
If you want to install OHSNAP in a custom location or as a non-root user, you can do so with a Python virtual environment. Create one as follows:

```
pyvenv /home/username/ohsnap
source /home/username/ohsnap/bin/activate
```

The above will create a Python virtual environment called ohsnap in username's home directory. To use the virtual environment, you will need to source the activate script in the bin directory of the virtual environment each time you login, or add the above source command to your `.bashrc`.

Download OHSNAP and install:

```
git clone https://github.com/batlabucd/OHSNAP.git
cd OHSNAP
python3 setup.py install
```

This will also install the Snakemake and Biopython dependencies.

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

`branch_lbls` is a directory of `.txt` files, each containing a comma-separated list of species to be used for branch labelled models. In each case, the species tree (`data/species.tfl`) is searched with the list of species for the first common ancestor clade and this clade is labelled for branch analysis.

`models` is a directory of CodeML control file templates for each model to be run. An example model file is here: https://github.com/batlabucd/OHSNAP/blob/master/ohsnap/example/models/CladeModelC.mod. These control file templates contain placeholders e.g. `{phy_fn}`, `{mod}`, `{out_dir}`, that are replaced with values by OHSNAP during run time. They tell CodeML how the inputs are named and how the outputs should be named. They should be present unaltered in all model files.

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

The `branchlbl_dir`, `mod_dir` and `phy_dir` variables give the paths to the `branch_lbls`, `models` and `phy` directories explained above and don't need to changed if the default directory locations are used. `labelled_models` is a list of models (filenames without the `.mod` file extension) that require branch labels e.g. `"labelled_models": ["alt", "null", "CladeModelC"],`. `species_tree` is the path to the Newick tree of all species explained above i.e. `species_tree: "data/species.tfl"`.

`Snakefile` is the `snakemake` workflow file that is executed when running a project.

## Running OHSNAP

OHSNAP can be run on a local workstation, with the `ohsnap_run_local` command, or a compute cluster, with the `ohsnap_run_cluster` command.

### `ohsnap_run_local`

```
usage: ohsnap_run_local [-h] [--num_threads NUM_THREADS] [project_directory]

positional arguments:
  project_directory     Run the OHSNAP project at this path locally

optional arguments:
  -h, --help            show this help message and exit
  --num_threads NUM_THREADS
                        The maximum number of threads to use for local job
                        execution
```

The `ohsnap_run_local` command executes an OHSNAP project on a single node/workstation and optionally accepts the path to an OHSNAP project folder. If none is given, the current directory is checked. If a supplied path or current directory are not OHSNAP directories, the `ohsnap_run_local` command with exit with a **"Error: Snakefile "Snakefile" not present."** message. You can set the number of threads to use for execution with the `--num_threads` option, the default is 1. It is recommended that you allow approximately 16GB of RAM for each CodeML run, so although you might have 4 threads, you should set num_threads to 2 if you only have 32GB of RAM.



