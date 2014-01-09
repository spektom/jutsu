from jutsu.lib.plugins import Plugin
from jutsu.lib.ui import UI

class WifiPlugin(Plugin):
	
	def __init__(self):
		super(WifiPlugin, self).__init__(
			name='wifi',
			version='1.0',
			author='Michael Spector <michael@gmail.com>',
			category='Network');
		
	def create_ui(self):
		return WifiUI(self)
		

class WifiUI(UI):
	def __init__(self, plugin):
		super(WifiUI, self).__init__(plugin)
		
	def get_menu_html(self):
		return '<span class="fa fa-signal"></span><a href="/wifi">Wi-Fi</a>'
