import flask
from flask.templating import DispatchingJinjaLoader
from flask.globals import _request_ctx_stack

class PatchedJinjaLoader(DispatchingJinjaLoader):
	""" Patch for templates resolution issue in blueprints with same template names:
		https://github.com/mitsuhiko/flask/issues/266 """
	def _iter_loaders(self, template):
		bp = _request_ctx_stack.top.request.blueprint
		if bp is not None and bp in self.app.blueprints:
			loader = self.app.blueprints[bp].jinja_loader
			if loader is not None:
				yield loader, template

		loader = self.app.jinja_loader
		if loader is not None:
			yield loader, template

def apply_patch(app):
	""" Applies the patch """
	app.jinja_options = flask.Flask.jinja_options.copy() 
	app.jinja_options['loader'] = PatchedJinjaLoader(app)
