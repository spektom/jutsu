from jutsu.lib.plugins import Plugin
from jutsu.lib.ui import UI
from jutsu.plugins.packages.pkg_manager import current
from flask import jsonify, request

class PackagesPlugin(Plugin):
	
	def __init__(self):
		super(PackagesPlugin, self).__init__(
			name='packages',
			version='1.0',
			author='Michael Spector <michael@gmail.com>',
			category='Setup');

	def create_ui(self):
		return PackagesUI(self)
		

class PackagesUI(UI):
	def __init__(self, plugin):
		super(PackagesUI, self).__init__(plugin)

	def list(self, request, installed):
		pattern = request.args.get('sSearch', '')
		data = current.list_installed(pattern) if installed else current.list_available(pattern) 
		total = len(data)
		start = int(request.args.get('iDisplayStart', 0))
		end = start + int(request.args.get('iDisplayLength', total))
		aaData = []
		for v in data[start:end]:
			aaData.append([ v['name'], v['version'], v['summary'] ])
		return jsonify({
			'aaData': aaData,
			'iTotalDisplayRecords': total
		})

	def setup_routes(self):
		UI.setup_routes(self)
		
		@self.page.route('/installed')
		def list_installed():
			return self.list(request, True)

		@self.page.route('/available')
		def list_available():
			return self.list(request, False)

		@self.page.route('/refresh')
		def refresh():
			current.refresh()
		
	def get_menu_html(self):
		return '<span class="fa fa-archive"></span><a href="/packages">Packages</a>'
