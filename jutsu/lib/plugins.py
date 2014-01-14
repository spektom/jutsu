import os
import sys
import imp
from pprint import pprint

class Category(object):
	""" Plug-in category """
	
	def __init__(self, name, icon_class=None):
		self.name = name
		self.icon_class = icon_class
	
	def get_name(self):
		return self.name
	
	def get_icon_class(self):
		return self.icon_class

class Plugin(object):
	""" Base plugin class """
	
	def __init__(self, name, desc=None, version = None, author = None, category = None):
		self.name = name
		self.desc = desc
		self.version = version
		self.author = author
		self.category = category
	
	def get_name(self):
		return self.name

	def get_version(self):
		return self.version
	
	def get_author(self):
		return self.author

	def get_category(self):
		return self.category

	def get_ui(self):
		try:
			return self.ui
		except AttributeError:
			self.ui = self.create_ui()
		return self.ui
	
	def create_ui(self):
		return None

# Existing plug-in categories:
categories = [
	Category('Setup', icon_class='fa fa-gear'),
	Category('Network'),
]

def get_categories():
	return categories

def load_plugins():
	global plugins
	try:
		return plugins
	except NameError:
		plugins = []
		plugins_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'plugins'))
		for plugin_name in os.listdir(plugins_path):
			if os.path.isdir(os.path.join(plugins_path, plugin_name)):
				fp, pathname, description = imp.find_module(plugin_name, [plugins_path])
				try:
					plugin = imp.load_module('jutsu_plugin_%s' % plugin_name, fp, pathname, description)
					plugins.append(plugin.instance)
				finally:
					if fp:
						fp.close()
	return plugins

def get_plugins():
	return load_plugins()

def get_plugins_by_category(category):
	res = []
	for plugin in get_plugins():
		if plugin.get_category() == category:
			res.append(plugin)
	return res
