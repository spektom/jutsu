import subprocess
import os

class PackageManager(object):
	@staticmethod
	def check_available(cmd):
		try:
			devnull = open(os.devnull, 'w')
			subprocess.call(cmd, stdout=devnull, stderr=devnull)
			return True
		except OSError:
			pass
		return False
	
	def list_available(self, pattern=None):
		raise NotImplementedError

	def list_installed(self, pattern=None):
		raise NotImplementedError

	def refresh(self):
		raise NotImplementedError

class DebPackageManager(PackageManager):
	""" Package manager utilities for Debian based system """
	@staticmethod
	def is_available():
		return PackageManager.check_available(['apt-get', '--version'])
	
	def list(self, pattern='', installed=True):
		import apt
		cache = apt.cache.Cache()
		res = []
		for name in sorted(cache.keys()):
			if name.find(pattern) != -1:
				package = cache[name]
				if package.is_installed == installed:
					for ver in package.versions:
						res.append({ 'name': package.name, 'version': ver.version, 'summary': package.candidate.summary })
		return res

	def list_available(self, pattern=''):
		return self.list(pattern, False)
	
	def list_installed(self, pattern=''):
		return self.list(pattern, True)

	def refresh(self):
		import apt
		from apt.progress.base import AcquireProgress, InstallProgress
		cache = apt.cache.Cache()
		cache.update()
		cache.commit(AcquireProgress(), InstallProgress())

class RPMPackageManager(PackageManager):
	""" Package manager utilities for Redhat based system """
	@staticmethod
	def is_available():
		return PackageManager.check_available(['yum', '--version'])


if DebPackageManager.is_available():
	current = DebPackageManager()
elif RPMPackageManager.is_available():
	current = RPMPackageManager()
else:
	raise Exception('The system neither RPM nor DEB based')
