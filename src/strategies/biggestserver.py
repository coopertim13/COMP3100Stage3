from strategies import strategy

class BiggestServer(strategy.Strategy):

	def calculate(self, client, servers, job):

		biggest_server = servers[0]
		for server in servers:
		    if server.get_cores() > biggest_server.get_cores():
		        biggest_server = server
		return biggest_server
