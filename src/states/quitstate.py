"""
Distributed Systems group project
Authors: Thomas Tapner, Abhinav Ram, Cooper Timewell
Student ID: 45387168, 45157855, 45429596
Practical session: Friday 10:00am
"""

from states import state
import sys

class QuitState(state.State):

	def __init__(self, client):
		super().__init__(client)


	def receive_quit(self):
		# Close the socket and the client when server is done
		self.client.closeSocket()
		sys.exit(0)