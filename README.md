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
usage: ohsnap_example [-h] output_path

positional arguments:
  output_path  Create an example OHSNAP project at this path

optional arguments:
  -h, --help   show this help message and exit
```

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

## Performing a dry run

You can see exactly what steps will be executed in a project using the `ohsnap_check` command. It simply takes the path to an OHSNAP directory as an argument, or if none is given, it assumes the current directory is an OHSNAP project directory. If a supplied path or current directory is not an OHSNAP project directory, the `ohsnap_check` command will exit with an **'Error: Snakefile "Snakefile" not present.'** error message. Here is an example of its output (with omissions for space reasons):

```
usage: ohsnap_check [-h] [project_directory]

positional arguments:
  project_directory  Perform a dry run check on the OHSNAP project at this
                     path (default: current directory)

optional arguments:
  -h, --help         show this help message and exit
```

```
ohsnap_check /path/to/example/project_dir

...

Job counts:
	count	jobs
	1	all
	4	c_codeml
	24	c_codeml_lbl
	24	c_lbl_species_tree
	4	c_mk_ctl
	24	c_mk_ctl_lbl
	4	c_mk_output
	24	c_mk_output_lbl
	16	c_prune_species_tree
	125

```

The above shows a summary of the jobs to be run on `project_dir`, which contains data from the included example. There are two versions of each job: with and without *\_lbl*, which refers to analysis done with and without labelled branches. In the example project, there are four sets of gene alignments. From the above, we can conclude that there is 1 model that is run on an unlabelled tree (1 model x 4 genes = 4 codeml jobs). The example data has two sets of species groups/labels: `myotis.txt` and `nmr.txt`, meaning there should be 3 labelled models to be run (3 labelled models x 4 genes x 2 species groups = 24 codeml jobs).

## Running OHSNAP

OHSNAP can be run on a local workstation, with the `ohsnap_run_local` command, or a compute cluster, with the `ohsnap_run_cluster` command.

### `ohsnap_run_local`

```
usage: ohsnap_run_local [-h] [--num_threads NUM_THREADS] [project_directory]

positional arguments:
  project_directory     Run the OHSNAP project at this path locally (default:
                        current directory)

optional arguments:
  -h, --help            show this help message and exit
  --num_threads NUM_THREADS
                        The maximum number of threads to use for local job
                        execution (default: 1)
```

The `ohsnap_run_local` command executes an OHSNAP project on a single node/workstation and optionally accepts the path to an OHSNAP project directory. If none is given, the current directory is checked. If a supplied path or current directory is not an OHSNAP project directory, the `ohsnap_run_local` command will exit with an **'Error: Snakefile "Snakefile" not present.'** error message. You can set the number of threads to use for execution with the `--num_threads` option, the default is 1. It is recommended that you allow approximately 16GB of RAM for each CodeML run, so although you might have 4 CPU cores, you should set num_threads to 2 if you only have 32GB of RAM.

### `ohsnap_run_cluster`

```
usage: ohsnap_run_cluster [-h] [--num_jobs NUM_JOBS]
                          [--cluster_cmd CLUSTER_CMD]
                          [project_directory]

positional arguments:
  project_directory     Run the OHSNAP project at this path on a cluster
                        environment (default: current directory)

optional arguments:
  -h, --help            show this help message and exit
  --num_jobs NUM_JOBS   The number of jobs to submit to the cluster execution
                        system at any one time (default: 10)
  --cluster_cmd CLUSTER_CMD
                        The cluster execution system submission command,
                        usually qsub. Use this option to specify the command,
                        how to request memory/threads, max walltime on your
                        cluster (default: qsub -j oe -o {log} -l walltime=96:0
                        0:00,mem={params.mem})
```

The `ohsnap_run_cluster` command requires a batch execution system, such as, Open Grid Engine, PBS, Torque etc. The command executes an OHSNAP project on a compute cluster and optionally accepts the path to an OHSNAP project directory. If none is given, the current directory is checked. If a supplied path or current directory is not an OHSNAP project directory, the ohsnap_run_local command will exit with an 'Error: Snakefile "Snakefile" not present.' error message. The maximum number of jobs submitted to the execution queue at any one time is specified by the `--num_jobs` option, the default is 10. Jobs are submitted to the batch execution system using the command specified by the `--cluster_cmd` option, the default is:

```
qsub -j oe -o {log} -l walltime=96:00:00,mem={params.mem}
```

`qsub` is the queue submission command to submit jobs to most batch execution systems. The `-j oe -o {log}` options specify that the standard error should be merged with the standard output and this should be directed to `{log}`, which is replaced with a path to a log file specific for each job. The `-l` option specifies the resources for the job. The walltime is the maximum time a job can run for, and in this case it is 96 hours, 0 minutes and 0 seconds. When a job reaches this limit, it will be killed and you may need to increase this limit depending on your input dataset (the time limit refers to the time taken to run a single job on a single gene and in most cases, 96 hours is more than sufficient). The `mem={params.mem}` section of the resource list is the memory requirement of a job and `params.mem` will be a specific value for each job e.g. codeml requests 16GB of memory.


