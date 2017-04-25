import setuptools


package_data = {
	'': ['proj.config', 'Snakefile']
}


setuptools.setup(name='OHSNAP',
	version='1.0',
	description='Optimised High-throughput SNakemaked Automation of PAML',
	author='Michael Clarke',
	author_email='michael.clarke@ucd.ie',
	url='https://github.com/batlabucd/OHSNAP',
	packages=['ohsnap'],
	include_package_data=True,
	entry_points = {
        'console_scripts': [ 
        	'ohsnap_new = ohsnap.new:main'
        ]
    },
)

