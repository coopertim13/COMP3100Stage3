#!/usr/bin/env python3

"""
Distributed Systems group project
Authors: Thomas Tapner
Student ID: 45387168
Practical session: Friday 10:00am
"""

class Job:

	def __init__(self, job_params):

		# set job parameters
		self.submit_time = int(job_params[0])
		self.job_id = int(job_params[1])
		self.estimated_runtime = int(job_params[2])
		self.cores = int(job_params[3])
		self.memory = int(job_params[4])
		self.disk = int(job_params[5])


	def get_submit_time(self):
		return self.submit_time


	def get_id(self):
		return self.job_id


	def get_estimated_runtime(self):
		return self.estimated_runtime


	def get_cores(self):
		return self.cores


	def get_memory(self):
		return self.memory


	def get_disk(self):
		return self.disk
