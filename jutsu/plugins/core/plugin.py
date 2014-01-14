from jutsu.lib.plugins import Plugin
from jutsu.lib.ui import UI

class CorePlugin(Plugin):
	def __init__(self):
		super(CorePlugin, self).__init__('core');
		
	def create_ui(self):
		return CoreUI(self)
		

class CoreUI(UI):
	def __init__(self, plugin):
		super(CoreUI, self).__init__(plugin)
