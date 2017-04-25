: ${1?"Usage: $0 <Snakefile>"}
snakemake -s $1 --latency-wait 60 --cluster "qsub -j oe -o {log} -l walltime=240:00:00,mem={params.mem},nodes=1:ppn={params.threads}" -j 13
