"""
Distributed Systems group project
Authors: Thomas Tapner, Abhinav Ram, Cooper Timewell
Student ID: 45387168, 45157855, 45429596
Practical session: Friday 10:00am
"""

class State:

	def __init__(self, client):
		self.client = client


	def receive_ok(self):
		raise Exception("Not implemented")


	def receive_none(self):
		raise Exception("Not implemented")


	def receive_quit(self):
		raise Exception("Not implemented")


	def handle_job_request(self):
		raise Exception("Not implemented")
