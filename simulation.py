#!/usr/bin/python3

import argparse
import sys
import random
from time import time
import utilities

class Simulator:
    def __init__(self, n):
        self.time = 0
        self.m = 10
        self.n = n
        self.preprocessor = []
        self.join = {}
        self.servers = []
        for i in range(self.m):
            self.servers.append([])
        self.next_arrival = utilities.inter_arrival_time()
        self.preprocessing_time = 0
        self.job_id = 0
        self.completed_requests = 0

    def simulate(self, requests=10, time=None, q=False):
        self.q = q
        self.time = self.next_arrival
        self.request_arrived()
        waiting_time = min(self.next_arrival, self.preprocessing_time)

        if time:
            while self.time < time:
                self.time += waiting_time
                waiting_time = self.recalculate_times(waiting_time)
        else:
            while requests > self.completed_requests:
                self.time += waiting_time
                waiting_time = self.recalculate_times(waiting_time)

    def seed(self, seed):
        random.seed(seed)

    def recalculate_times(self, waited_time):
        waiting_time = None

        for s in range(self.m):
            server = self.servers[s]
            if server:
                server[0][1] -= waited_time
                if not server[0][1]:
                    self.server_finish_sub_task(s)
                if server:
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

        self.next_arrival -= waited_time
        if not self.next_arrival:
            self.request_arrived()
        if not waiting_time:
            waiting_time = self.next_arrival
        else:
            waiting_time = min(waiting_time, self.next_arrival)

        return waiting_time

    def request_arrived(self):
        self.preprocessor.append(self.job_id)
        self.next_arrival = utilities.inter_arrival_time()
        self.preprocessing_time = utilities.pre_processor_service_time(self.n)

        if not self.q:
            self.log("Job number %d arrived, requiring %s time" % (self.job_id, self.preprocessing_time))

        self.job_id += 1

    def split_request(self):
        job_id = self.preprocessor[0]
        selected_servers = sorted(random.sample(range(self.m), self.n))
        if not self.q:
            self.log("Job number %d split to servers %s" % (job_id, selected_servers))

        for s in selected_servers:
            service_time = utilities.sub_task_service_time(self.n)
            self.servers[s].append([job_id, service_time])
            if not self.q:
                self.log("Time required at server %d: %s" % (s, service_time))
        self.preprocessor.pop(0)
        self.join[job_id] = self.n

    def server_finish_sub_task(self, i):
        (job_id, _) = self.servers[i].pop(0)
        self.join[job_id] -= 1
        if not self.q:
            self.log("Server %d finished subtask on job %d" % (i, job_id))

        if not self.join[job_id]:
            self.join.pop(job_id)
            if not self.q:
                self.log("Job number %d completed" % job_id)
            self.completed_requests += 1

    def log(self, message):
        print("%s - %s" % (self.time, message))

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('n', default=5, type=int, help='number of servers to split each request to')
    parser.add_argument('--avg', type=int, help='calculate the average system performance over several simulations')
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument('--requests', '-r', type=int, default=10, help='number of requests to process')
    mode_group.add_argument('--time', '-t', type=int, help='run simulation for specified amount of time')
    parser.add_argument('-q', action='store_true', help="don't print log to stdout")
    parser.add_argument('--seed', '-s', type=float, help='seed the simulation with a predetermined value')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    if args.seed:
        random.seed(args.seed)
    else:
        seed = time()
        random.seed(seed)
        print("System seeded with %s" % seed)
    if args.avg:
        total_throughput = 0
        for _ in range(args.avg):
            simulator = Simulator(args.n)
            simulator.simulate(args.requests, args.time, args.q)
            requests = simulator.completed_requests
            sim_time = simulator.time
            throughput = sim_time/requests
            total_throughput += throughput
        total_throughput /= args.avg
        print(total_throughput)
    else:
        simulator = Simulator(args.n)
        simulator.simulate(args.requests, args.time, args.q)

if __name__ == '__main__':
    main()
