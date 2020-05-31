"""
Distributed Systems group project
Authors: Thomas Tapner
Student ID: 45387168
Practical session: Friday 10:00am
"""

from strategies import strategy


class FirstFit(strategy.Strategy):
	def calculate(self, client, servers, job):
		# get the root element
		system = self.tree.getroot()
		# sort the servers in system.xml by core count
		server_definitions = sorted(system[0], key=lambda x: int(x.attrib["coreCount"]))
		# Iterate over the server
		for server_definition in server_definitions:
			server_type = server_definition.attrib["type"]
			# Iterate over possible servers, only returning the first match of the server type that can run the job
			for server in servers:
				if(server.get_name() == server_type and server.can_run(job)):
					return server
		# If none capable of running job, just return the first server
		return servers[0]
