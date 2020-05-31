"""
Distributed Systems group project
Authors: Thomas Tapner, Abhinav Ram, Cooper Timewell
Student ID: 45387168, 45157855, 45429596
Practical session: Friday 10:00am
"""

from states import state

class AuthenticationState(state.State):

	def __init__(self, client):
		super().__init__(client)


	def receive_ok(self):
		# When we authenticate we are okay to read system.xml and 
		# begin executing jobs
		self.client.readSystemData()
		self.client.s.send("REDY".encode())
		self.client.setState(self.client.getJobExecutionState())