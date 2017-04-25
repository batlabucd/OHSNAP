import errno
import os
import os.path
import subprocess


def checkcmdlist(cmds):
	"""Take a list of cmds and check if they are executable i.e. they exist in the path 
		and can be executed. An OSError exception will be raised when a cmd that is not 
		executable is encountered."""
	assert isinstance(cmds, list)
	for cmd in cmds:
		if not subprocess.call("type " + cmd, shell=True, \
			stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0:
			raise OSError('Command {0} not found.'.format(cmd))
	
	
def mkdir_p(path):
	"""Provides a mkdir implementation with -p functionality."""
	try:
		os.makedirs(path)
	except OSError as exc:
		if exc.errno == errno.EEXIST and \
			os.path.isdir(path):
			pass
		else:
			raise
			

def versioncmd(cmd):
	"""Run a command that returns a version number and return a string."""
	return str(subprocess.check_output(cmd, shell=True), encoding='UTF-8').split('\n')[0]
	
	
	
