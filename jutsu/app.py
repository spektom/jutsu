#!/usr/bin/env python

import sys
# Disable creating .pyc files
sys.dont_write_bytecode = True

import os
import flask
import jinja_patch
from jutsu.lib.plugins import get_plugins
from jutsu.lib.db import db_session

class JutsuApp(flask.Flask):
	def __init__(self, name):
		super(JutsuApp, self).__init__(name)
		jinja_patch.apply_patch(self)
		
		@self.teardown_appcontext
		def shutdown_session(exception=None):
			db_session.remove()
		
	def send_static_file(self, filename):
		""" Patch for solving static folder search path issue for multiple blueprints:
			https://github.com/mitsuhiko/flask/issues/348#issuecomment-16264133 """
		for blueprint in self.blueprints.values():
			filepath = os.path.join(blueprint.static_folder, filename)
			if os.path.exists(filepath):
				return flask.send_from_directory(blueprint.static_folder, filename)
		return super(JutsuApp, self).send_static_file(filename)
	
	def run(self, **args):
		# Bootstrap the application by initializing all the modules:
		for plugin in get_plugins():
			plugin_ui = plugin.get_ui()
			if not plugin_ui is None:
				# Inject needed variables into plug-in UI module
				plugin_ui_module = sys.modules[plugin_ui.__module__]
				plugin_ui_module.app = self 
				url_prefix = '/' if plugin.get_name() == "core" else '/' + plugin.get_name()
				self.register_blueprint(plugin_ui.page, url_prefix=url_prefix)

		super(JutsuApp, self).run(**args)

if __name__ == '__main__':
	app = JutsuApp(__name__)
	app.run(debug=True, use_reloader=False)
