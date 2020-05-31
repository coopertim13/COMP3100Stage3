#!/usr/bin/env python3

"""
Distributed Systems group project
Authors: Thomas Tapner, Abhinav Ram, Cooper Timewell
Student ID: 45387168, 45157855, 45429596
Practical session: Friday 10:00am
"""

import socket
import sys
import argparse
from states import *
from strategies import *


class Client:

    def __init__(self):

        # Define and set the states
        self.startState = start.StartState(self)
        self.authState = authentication.AuthenticationState(self)
        self.jobExecutionState = jobexecution.JobExecutionState(self)
        self.quitState = quitstate.QuitState(self)
        self.setState(self.getStartState())
        self.jobExecutionTimes = []
        self.medianExecutionTime = 0
        self.timeIdle = {}


    def setState(self, state):
        self.state = state


    def getStartState(self):
        return self.startState


    def getAuthenticationState(self):
        return self.authState


    def getJobExecutionState(self):
        return self.jobExecutionState


    def getQuitState(self):
        return self.quitState


    def readSystemData(self):
        self.serverStrategy.readSystemData()


    def getServer(self, servers, job):
        # Use the strategy set to find the server given a job
        server = self.serverStrategy.calculate(self, servers, job)
        return server


    def buildSocket(self):
        self.s = socket.socket()
        self.s.connect(('127.0.0.1', 50000))


    def closeSocket(self):
        self.s.close()


    def checkArgs(self):

        # check if -a command line argument exists
        parser = argparse.ArgumentParser()
        parser.add_argument('-a', help="specify algorithm")
        args = parser.parse_args()

        # set the strategy dependant on what the value of -a is
        if args.a:
            if args.a == "ff":
                self.serverStrategy = firstfit.FirstFit()
            elif args.a == "bf":
                self.serverStrategy = bestfit.BestFit()
            elif args.a == "wf":
                self.serverStrategy = worstfit.WorstFit()
            elif args.a == "ar":
                self.serverStrategy = allrounder.AllRounder()
        else:
            self.serverStrategy = biggestserver.BiggestServer()


    def run(self):

        # setup client
        self.checkArgs()
        self.buildSocket()

        # call upon state method depending on message received from server
        # state handles responses
        self.s.send("HELO".encode())
        while True:
            data = self.s.recv(1024).decode()
            if data.startswith("OK"):
                self.state.receive_ok()
            elif data.startswith("NONE"):
                self.state.receive_none()
            elif data.startswith("JOBN") or data.startswith("JOBP"):
                self.state.handle_job_request(data.split()[1:])
            elif data.startswith("QUIT"):
                self.state.receive_quit()
            else:
                print("Unknown command", flush=True)
                break


if __name__ == "__main__":

    # run the client
    client = Client()
    client.run()


