import errno
import os
import os.path
import subprocess


def which(cmd):
	"""Check if cmd is an executable in the system path."""
	# modified from http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
	def is_exe(fpath):
		return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
	fpath, fname = os.path.split(cmd)
	if fpath:
		if is_exe(cmd):
			return cmd
	else:
		for path in os.environ['PATH'].split(os.pathsep):
			path = path.strip('"')
			exe_file = os.path.join(path, cmd)
			if is_exe(exe_file):
				return exe_file
	return None


def checkcmdlist(cmds):
	"""Take a list of cmds and check if they are executable i.e. they exist in the path 
		and can be executed. An OSError exception will be raised when a cmd that is not 
		executable is encountered."""
	assert isinstance(cmds, list)
	for cmd in cmds:
		if which(cmd) is None:
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
			
			
def msplit_path(path):
	"""Split a path into multiple/all components."""
	folders = []
	while 1:
		path, folder = os.path.split(path)
		if folder != '':
			folders.append(folder)
		else:
			if path != '':
				folders.append(path)
			break
	folders.reverse()
	return folders
			

def versioncmd(cmd):
	"""Run a command that returns a version number and return a string."""
	return str(subprocess.check_output(cmd, shell=True), encoding='UTF-8').split('\n')[0]
	
	
	
