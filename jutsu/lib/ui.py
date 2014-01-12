import flask
from jutsu.lib.plugins import get_categories, get_plugins_by_category

class UI(object):
	""" Plug-in UI component """
	
	def __init__(self, plugin):
		"""
			Initializes plug-in UI component
			
			Arguments:
			name -- Plug-in name
		"""
		self.name = plugin.get_name()
		self.page = flask.Blueprint(self.name, plugin.__module__, template_folder='views', static_folder='static')
		self.setup_routes()
		
	def render(self, template, **context):
		# Call render method, and pass all used variables:
		context['get_categories'] = get_categories
		context['get_plugins_by_category'] = get_plugins_by_category
		return flask.render_template(template, **context)
		
	def setup_routes(self):
		"""
			This method is used for adding new routes using Flask method decoration style.
		"""
		
		# Add default route to the index page:
		@self.page.route('/')
		def index():
			return self.render(self.name + '/index.html')

	def get_menu_html(self):
		""" Returns HTML code for the main page menu """
		return None

