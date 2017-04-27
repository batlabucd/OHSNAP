import argparse
import os
import subprocess
import sys


qsub_cmd = 'qsub -j oe -o {log} -l walltime=96:00:00,mem={params.mem},nodes=1:ppn={params.threads}'


parser = argparse.ArgumentParser()
parser.add_argument('--num_jobs', default=10, \
	help='The number of jobs to submit to the cluster execution system at any one time')
parser.add_argument('--cluster_cmd', default=qsub_cmd, \
	help="""The cluster execution system submission command, usually qsub. Use this option 
		to specify the command, how to request memory/threads, max walltime on your cluster""")
parser.add_argument('project_directory', nargs='?', default=os.getcwd(), \
	help='Run the OHSNAP project at this path on a cluster environment')


def ohsnap_runcluster(project_directory, num_jobs, cluster_cmd, latency_wait=60):
	"""Execute the OHSNAP project in project_directory on a cluster environment. The num_jobs 
		parameter specifies the maximum number of jobs to submit at once and the cluster_cmd 
		parameter details how to call the job submission command on this cluster. The 
		latency_wait parameter is the time to wait for output files to appear after a job 
		has finished executing (there can be a delay on NFS mounts)."""
	cmd = 'snakemake --latency-wait {latency_wait} --cluster "{cluster_cmd}" -j {num_jobs}'.format(\
		latency_wait=latency_wait, cluster_cmd=cluster_cmd, num_jobs=num_jobs)
	subprocess.call(cmd, cwd=project_directory, shell=True)


def main():
	args = parser.parse_args()
	ohsnap_runcluster(args.project_directory, args.num_jobs, args.cluster_cmd)

	
