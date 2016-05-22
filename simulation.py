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
        self.server_times = [0]*self.m
        for i in range(self.m):
            self.servers.append([])
        self.next_arrival = utilities.inter_arrival_time()
        self.preprocessing_time = 0
        self.job_id = 0
        self.completed_requests = 0
        self.job_start_times = {}
        self.job_response_times = []

# Run the simulation
    def simulate(self, requests=10, time=None, v=False):
        self.v = v
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

# Seed the system
    def seed(self, seed):
        random.seed(seed)

# Wait for a specified time, perform an event, and recalculate new waiting
# time
    def recalculate_times(self, waited_time):
        waiting_time = None

        for s in range(self.m):
            server = self.servers[s]
            if server:
                self.server_times[s] -= waited_time
                if not self.server_times[s]:
                    self.server_finish_sub_task(s)

        if self.preprocessor:
            self.preprocessing_time -= waited_time
            if not self.preprocessing_time:
                self.split_request()

        self.next_arrival -= waited_time
        if not self.next_arrival:
            self.request_arrived()
        waiting_time = self.next_arrival

        for s in range(self.m):
            if self.servers[s]:
                waiting_time = min(waiting_time, self.server_times[s])

        if self.preprocessor:
            waiting_time = min(waiting_time, self.preprocessing_time)

        return waiting_time

# Event: when i new request arrives to the system
# Adds the job to the pre-processors queue
    def request_arrived(self):
        if not self.preprocessor:
            self.preprocessing_time = utilities.pre_processor_service_time(self.n)
            if self.v:
                self.log("Job {} arrived, requiring {:0.6f} time".format(self.job_id, self.preprocessing_time))
        else:
            if self.v:
                self.log("Job %d arrived and was added to pre-processor queue" % self.job_id)
        self.preprocessor.append(self.job_id)
        self.next_arrival = utilities.inter_arrival_time()
        self.job_start_times[self.job_id] = self.time

        self.job_id += 1

# Event: when the pre-processor has finished a task
# Distributes sub-tasks to n random servers
    def split_request(self):
        job_id = self.preprocessor.pop(0)
        selected_servers = sorted(random.sample(range(self.m), self.n))
        if self.v:
            self.log("Job %d split to servers %s" % (job_id, selected_servers))

        for s in selected_servers:
            if not self.server_times[s]:
                service_time = utilities.sub_task_service_time(self.n)
                self.server_times[s] = service_time
                if self.v:
                    self.log("S{} started subtask of job {}, requiring {:0.6f} time".format(s, job_id, service_time))
            self.servers[s].append(job_id)
        self.join[job_id] = self.n

        if self.preprocessor:
            self.preprocessing_time = utilities.pre_processor_service_time(self.n)
            if self.v:
                self.log("Job {} started, requiring {:0.6f} time".format(self.preprocessor[0], self.preprocessing_time))

# Event: when a server finishes a sub-task
# The join point collects the result
    def server_finish_sub_task(self, i):
        job_id = self.servers[i].pop(0)
        self.join[job_id] -= 1
        if self.v:
            self.log("S%d finished subtask on job %d" % (i, job_id))
        if self.servers[i]:
            service_time = utilities.sub_task_service_time(self.n)
            self.server_times[i] = service_time
            if self.v:
                self.log("S{} started subtask of job {}, requiring {:0.6f} time".format(i, self.servers[i][0], service_time))

        if not self.join[job_id]:
            self.join.pop(job_id)
            total_time = self.time - self.job_start_times.pop(job_id)
            if self.v:
                self.log("Job {} completed after {:0.6f} time".format(job_id, total_time))
            self.completed_requests += 1
            self.job_response_times.append(total_time)

# Show logging information
    def log(self, message):
        print("{:0.6f} - {}".format(self.time, message))

# Parse command line arguments
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('n', default=5, type=int, help='number of servers to split each request to')
    parser.add_argument('--avg', type=int, help='calculate the average system performance over several simulations')
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument('--requests', '-r', type=int, default=10, help='number of requests to process')
    mode_group.add_argument('--time', '-t', type=int, help='run simulation for specified amount of time')
    parser.add_argument('-v', action='store_true', help="don't print log to stdout")
    parser.add_argument('--seed', '-s', help='seed the simulation with a predetermined value')
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
        total_response_time = 0
        for i in range(args.avg):
            simulator = Simulator(args.n)
            simulator.simulate(args.requests, args.time, args.v)
            (throughput, mean_response_time) = evaluate(simulator)
            total_throughput += throughput
            total_response_time += mean_response_time
        total_throughput /= args.avg
        total_response_time /= args.avg
        print("Average throughput: %s" % total_throughput)
        print("Average mean response time: %s" % total_response_time)
    else:
        simulator = Simulator(args.n)
        simulator.simulate(args.requests, args.time, args.v)
        (throughput, mean_response_time) = evaluate(simulator)
        print("Throughput: %s" % throughput)
        print("Mean response time: %s" % mean_response_time)

# Calculate throughput and mean response time for a simulation
def evaluate(simulator):
    requests = simulator.completed_requests
    sim_time = simulator.time
    throughput = requests/sim_time
    mean_response_time = sum(simulator.job_response_times)/float(requests)
    return (throughput, mean_response_time)

if __name__ == '__main__':
    main()
