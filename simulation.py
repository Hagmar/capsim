#!/usr/bin/python3

import sys
import random
import utilities

class Simulator:
    def __init__(self, n=5):
        self.time = 0
        self.m = 10
        self.n = 5
        self.preprocessor = []
        self.join = {}
        self.servers = []
        for i in range(self.m):
            self.servers.append([])
        self.next_arrival = utilities.inter_arrival_time()
        self.preprocessing_time = 0
        self.job_id = 0

    def simulate(self, requests=10):
        self.time = self.next_arrival
        self.request_arrived()
        waiting_time = min(self.next_arrival, self.preprocessing_time)

        while requests:
            self.time += waiting_time
            waiting_time = self.recalculate_times(waiting_time)

    def seed(self, seed):
        random.seed(seed)

    def recalculate_times(self, waited_time):
        waiting_time = None

        for s in range(self.m):
            server = self.servers[s]
            print(server)
            if server:
                server[0][1] -= waited_time
                if not server[0][1]:
                    self.server_finish_sub_task(s)
                if server[0][1]:
                    if not waiting_time:
                        waiting_time = server[0][1]
                    else:
                        waiting_time = min(waiting_time, server[0][1])

        if self.preprocessor:
            self.preprocessing_time -= waited_time
            if not self.preprocessing_time:
                self.split_request()
            if self.preprocessor:
                if not waiting_time:
                    waiting_time = self.preprocessing_time
                else:
                    waiting_time = min(waiting_time, self.preprocessing_time)
            print("Pre-processing time: %s" % self.preprocessing_time)

        self.next_arrival -= waited_time
        if not self.next_arrival:
            self.request_arrived()
        if not waiting_time:
            waiting_time = self.next_arrival
        else:
            waiting_time = min(waiting_time, self.next_arrival)
        print("Arrival time: %s" % self.next_arrival)

        return waiting_time

    def request_arrived(self):
        self.preprocessor.append(self.job_id)
        self.next_arrival = utilities.inter_arrival_time()
        self.preprocessing_time = utilities.pre_processor_service_time(self.n)

        self.log("Job number %d arrived, requiring %s time" % (self.job_id, self.preprocessing_time))

        self.job_id += 1

    def split_request(self):
        job_id = self.preprocessor[0]
        selected_servers = random.sample(range(self.m), self.n)
        for s in selected_servers:
            service_time = utilities.sub_task_service_time(self.n)
            self.servers[s].append([job_id, service_time])
        self.preprocessor.pop(0)
        self.join[job_id] = self.n

        self.log("Job number %d split to servers %s" % (job_id, sorted(selected_servers)))

    def server_finish_sub_task(self, i):
        (job_id, _) = self.servers[i].pop(0)
        self.join[job_id] -= 1
        if not self.join[job_id]:
            self.join.pop(job_id)

        self.finished_job(job_id)

    def finished_job(self, job_id):
        self.log("Finished job number %d" % (self.time, job_id))

    def log(self, message):
        print("%s - %s" % (self.time, message))

def main():
    simulator = Simulator(5)
    simulator.simulate()

if __name__ == '__main__':
    main()
