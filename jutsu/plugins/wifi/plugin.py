from jutsu.lib.plugins import Plugin
from jutsu.lib.ui import UI
from flask import jsonify
from wifi import Cell
from subprocess import Popen, PIPE, STDOUT
from time import sleep

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
		
	def setup_routes(self):
		UI.setup_routes(self)
		
		@self.page.route('/interfaces')
		def list_ifaces():
			exp_backoff=1
			for _ in range(5):
				ifaces = []
				proc = Popen('/sbin/iwconfig', stderr=STDOUT, stdout=PIPE)
				while True:
					retcode = proc.poll() #returns None while subprocess is running
					line = proc.stdout.readline()
					if line.find("IEEE") != -1:
						ifaces.append(line.split(' ', 1)[0])
					if retcode is not None:
						break
				if (len(ifaces) > 0):
					break
				sleep(exp_backoff)
				exp_backoff *= 2
				# retry
			return jsonify(ifaces=ifaces)
		
		@self.page.route('/scan/<iface>')
		def scan(iface):
			exp_backoff=1
			for _ in range(5):
				results = []
				for cell in Cell.all(iface):
					c = {
						'ssid': cell.ssid,
						'frequency': cell.frequency,
						'bitrates': cell.bitrates,
						'encrypted': cell.encrypted,
						'channel': cell.channel,
						'address': cell.address,
						'mode': cell.mode,
						'quality': cell.quality,
						'signal': cell.signal
					}
					if cell.encrypted:
						c['encryption_type'] = cell.encryption_type
					results.append(c)
	
				results.sort(key=lambda x: x['signal'], reverse=True)
				if (len(results) > 0):
					break
				sleep(exp_backoff)
				exp_backoff *= 2
				#retry
			return jsonify(results=results)

		@self.page.route('/configure')
		def configure():
			return UI.render(self, self.name + '/configure.html')

	def get_menu_html(self):
		return '<span class="fa fa-signal"></span><a href="/wifi">Wi-Fi</a>'
