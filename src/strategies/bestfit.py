"""
Distributed Systems group project
Authors: Abhinav Ram
Student ID: 45157855
Practical session: Friday 10:00am
"""

from strategies import strategy

class BestFit(strategy.Strategy):
    def calculate(self, client, servers, job):

        # Initialise variables which mark best-fit
        bestFit = 9999999
        minAvail = 9999999
        bfServer = servers[0]

        # Get system data (Read in via inherited class Strategy.py)
        system = self.tree.getroot()

        # Iterate server types in order of appearance in system.xml
        for serverDefinitions in system[0]:
            serverType = serverDefinitions.attrib["type"]

            # Iterate all servers returned by ds-server response to RESC Capable
            for server in servers:

                #Check if name of current server matches server attribute in system.xml
                if(server.get_name() == serverType):

                    # If the first condition is true, bfServer satisfies "alt best fit" 
                    #    -> (i.e. bfServer = best-fit Active server based on initial resource capacity)
                    # OR
                    # bfServer satisfies "best fit" condition
                    #    -> (i.e. bfServer = best-fit server based on fitness value and minAvail time)
                    if((server.can_run(job) and server.cores_left(job) < bestFit) or
                        (server.can_run(job) and server.cores_left(job) == bestFit and server.get_available_time() < minAvail)):

                        # If new bfServer or Active bfServer found, then reassign marker variables
                        bestFit = server.cores_left(job)
                        minAvail = server.get_available_time()
                        bfServer = server

        return bfServer

