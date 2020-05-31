"""
Distributed Systems group project
Authors: Thomas Tapner, Abhinav Ram, Cooper Timewell
Student ID: 45387168, 45157855, 45429596
Practical session: Friday 10:00am
"""

from states import state
from job import Job
from server import Server

class JobExecutionState(state.State):

	def __init__(self, client):
		super().__init__(client)


	def receive_ok(self):
		# alert the server we are ready to receive jobs
		self.client.s.send("REDY".encode())


	def receive_none(self):
		# When there are no more jobs left, quit
		self.client.s.send("QUIT".encode())
		self.client.setState(self.client.getQuitState())


	def request_servers(self, current_job):

		# Get job information
		required_cores = str(current_job.get_cores())
		required_memory = str(current_job.get_memory())
		required_disk = str(current_job.get_disk())

		# Get servers capable of running current job
		servers = []
		self.client.s.send(' '.join(["RESC", "Capable", required_cores, required_memory, required_disk]).encode())
		data = self.client.s.recv(1024).decode()

		# No more servers when server sends '.'
		while data != ".":
			# Create server object when server data received
			if(data != "DATA"):
				servers.append(Server(data))
			# Continue to receive server information
			self.client.s.send("OK".encode())
			data = self.client.s.recv(1024).decode()
		return servers


	def handle_job_request(self, job):

		# Get job information
		current_job = Job(job)
		job_id = current_job.get_id()
		
		# Get server to run job on
		servers = self.request_servers(current_job)
		executing_server = self.client.getServer(servers, current_job)

		# send this server with the corresponding job id
		dataSend = " ".join(["SCHD", str(job_id), executing_server.get_name(), str(executing_server.get_id())])
		self.client.s.send(dataSend.encode())

