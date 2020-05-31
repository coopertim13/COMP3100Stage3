import xml.etree.ElementTree as ET

class Strategy:

	def readSystemData(self):
		self.tree = ET.parse('../simulator/system.xml')


	def calculate(self, client, servers, job):
		raise Exception("Not implemented")
