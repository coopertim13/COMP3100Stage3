"""
Distributed System Group Project: Stage 2
Author: Cooper Timewell
Student ID: 45429596
Practical Session: Friday 10:00am
"""

from strategies import strategy

class WorstFit(strategy.Strategy):

    def calculate(self, client, servers, job):

        # Initialise variables which mark worst/alt fit
        worstFit = -9999999
        altFit = -9999999
        worst_server = servers[0]
        alt_server = servers[0]

        # Get system data (read in via inherited class strategy.py)
        system = self.tree.getroot()

        # Iterate server types in order of appearance in system.xml
        for serverDefinitions in system[0]:
            serverType = serverDefinitions.attrib["type"]

            # Iterate all servers returned by ds-server response to RESC Capable
            for server in servers:

                # Check if name of current server matches server attribute in system.xml, and the server has sufficient resources (CPU cores, memory and disk)
                if(server.get_name() == serverType and server.can_run(job)):

                    # If the first condition is true, server satifies "worst fit"
                    #    -> (i.e. worst_server = worst immediately available server based on fitness value
                    # OR
                    # If the second condition is true, server satifies "alt fit"
                    #    -> (i.e. alt_server = worst server available in a short definite amount of time based on fitness value
                    if (server.cores_left(job) > worstFit) and ((2 <= server.get_state() <= 3) or server.get_available_time() == job.get_submit_time()):
                        worstFit = server.cores_left(job)
                        worst_server = server
                    elif server.cores_left(job) > altFit and (server.get_state() != 2 and server.get_state() != 3):
                        altFit = server.cores_left(job)
                        alt_server = server

        # If "worst fit" is found
        if worstFit >= 0:
            return worst_server

        # If "alt fit" is found
        if altFit >= 0:
            return alt_server

        # Otherwise, return worst-fit active server based on initial resouce capacity
        return worst_server
