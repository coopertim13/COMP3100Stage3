"""
Distributed Systems group project
Authors: Thomas Tapner, Abhinav Ram, Cooper Timewell
Student ID: 45387168, 45157855, 45429596
Practical session: Friday 10:00am
"""

from states import state

class StartState(state.State):

	def __init__(self, client):
		super().__init__(client)
		self.creds = "root"


	def receive_ok(self):
		# Send the authentication details when the server starts
		self.client.s.send("AUTH {}".format(self.creds).encode())
		self.client.setState(self.client.getAuthenticationState())