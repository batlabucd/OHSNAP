from os.path import join


configfile: 'proj.config'


include: "rules/codeml.rules"


rule all:
	input: all_files
	params: mem='1G', threads='1'
	log: join('logs', 'all.log')
		

