"""
Distributed Systems - Stage 3
Authors: Cooper Timewell
Student ID: 45429596
Practical session: Friday 10:00am
"""
import random
from strategies import strategy

class AllRounder(strategy.Strategy):

	def update(self, client, servers, job):

		##UPDATE JOB EXECUTION TIMES, AND FIND NEW MEDIAN EXECUTION TIME
		client.jobExecutionTimes.append(job.get_estimated_runtime())
		client.jobExecutionTimes.sort()
		client.medianExecutionTime = client.jobExecutionTimes[int(len(client.jobExecutionTimes)/2)]

		##IDLE SERVERS UPDATE - ADD NEW IDLE SERVERS, REMOVE SERVERS THAT AREN'T IDLE
		for server in servers:
			if(server.get_state() == 2):
				if str(server.get_id())+":"+str(server.get_name()) not in client.timeIdle:
					client.timeIdle[str(server.get_id())+":"+str(server.get_name())] = int(job.get_submit_time())
			else:
				if str(server.get_id())+":"+str(server.get_name()) in client.timeIdle:
					del client.timeIdle[str(server.get_id())+":"+str(server.get_name())]


	def idleUpdate(self, client, servers, job):
		deleted = []
		for idle_server in client.timeIdle:
			#Calculation that determines a server has been idle for too long, and should be terminated to save money
			if((job.get_submit_time() - client.timeIdle[idle_server]) > client.medianExecutionTime):
				#Terminate that server
				client.s.send(' '.join(["TERM", idle_server.split(":")[1], idle_server.split(":")[0]]).encode())
				data = client.s.recv(1024).decode()
				deleted.append(idle_server)
				if(data == "OK"):
					client.s.send("REDY".encode())
					data = client.s.recv(1024).decode()
		for toDelete in deleted:
			#Delete all idle servers that have been terminated from the array of idle servers
			del client.timeIdle[toDelete]


	#Returns all idle servers that have the same type as server_name
	def idlesExist(self, server_name, servers):
		idles = []
		for server in servers:
			if (server.get_name() == server_name):
				if(server.get_state() == 2):
					idles.append(server)
		return idles


	#Returns True if all servers that have the same type as server_name have the same number of cores available, False otherwise
	def allSameCores(self, server_name, servers, server):
		coreToCompare = server.get_cores()
		for serve in servers:
			if(serve.get_name() == server_name):
				if(serve.get_cores() != coreToCompare):
					return False
		return True


	#Returns all servers of type server_name
	def arrayOfSameServer(self, server_name, servers):
		toReturn = []
		for server in servers:
			if server.get_name() == server_name:
				toReturn.append(server)
		return toReturn


	#Calculates and returns the server of type server_name with the most cores available
	def serverWithMostCores(self, server_name, servers):
		mostCores = -999999
		largestServer = None
		for server in servers:
			if server.get_name() == server_name:
				if server.get_cores() > mostCores:
					mostCores = server.get_cores()
					largestServer = server
		return largestServer


	#Returns all servers of type server_name that are not inactive and can run the specified job
	def spareSpaceServers(self, server_name, servers, job):
		toReturn = []
		for server in servers:
			if server.get_name() == server_name:
				if(server.can_run(job) and 1 <= server.get_state() <= 3):
					toReturn.append(server)
		return toReturn


	def calculate(self, client, servers, job):
		self.update(client, servers, job)
		self.idleUpdate(client, servers, job)
		system = self.tree.getroot()
		#Sorts servers in system.xml by rate (cheapest servers are prioritised)
		systemServers = sorted(system[0], key = lambda x : float(x.attrib["rate"]))
		for sysServer in systemServers:
			actualServerName = sysServer.attrib["type"]
			for server in servers:
				if(actualServerName == server.get_name()):
					#1st priority: idle servers
					#   --> if at least 1 idle server of type actualServerName is found, allocate the job randomly to one of these servers
					if (len(self.idlesExist(server.get_name(), servers)) >= 1):
						return random.choice(self.idlesExist(server.get_name(), servers))

					#2nd priority: servers that aren't inactive and can run the job - if found, randomly allocate the job to one of these servers
					elif (len(self.spareSpaceServers(server.get_name(), servers, job)) >= 1):
						return random.choice(self.spareSpaceServers(server.get_name(), servers, job))

					else:
						#4th priority: all servers of type actualServerName have same number of cores free - randomly allocate job to any server of this type
						if (self.allSameCores(server.get_name(), servers, server)):
							return random.choice(self.arrayOfSameServer(server.get_name(), servers))

						#3rd priority: assign job to server of type actualServerName with most cores free to reduce queuing on other servers
						else:
							return self.serverWithMostCores(server.get_name(), servers)
