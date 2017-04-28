import setuptools


setuptools.setup(name='OHSNAP',
	version='1.0',
	description='Optimised High-throughput SNakemake Automation of PAML',
	author='Michael Clarke',
	author_email='michael.clarke@ucd.ie',
	url='https://github.com/batlabucd/OHSNAP',
	licence='MIT',
	packages=['ohsnap'],
	include_package_data=True,
	install_requires=['biopython', 'snakemake'],
	entry_points = {
        'console_scripts': [ 
        	'ohsnap_new = ohsnap.new:main',
        	'ohsnap_example = ohsnap.example:main',
        	'ohsnap_check = ohsnap.check:main',
        	'ohsnap_run_local = ohsnap.run_local:main',
        	'ohsnap_run_cluster = ohsnap.run_cluster:main'
        ]
    },
)

