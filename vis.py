#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import utilities

x = [utilities.inter_arrival_time() for _ in range(1000000)]

plt.hist(x, bins=100, normed=1, facecolor='green', alpha=0.75)
plt.plot(bins, y, 'r', linewidth=2)

plt.xlabel('Inter-arrival time')
plt.ylabel('Frequency')
plt.title(r'Visualization of inter-arrival time distribution')
plt.axis([0, 8, 0, 1])

plt.show()


x = [utilities.pre_processor_service_time(2) for _ in range(1000000)]

plt.hist(x, bins=100, normed=1, facecolor='green', alpha=0.75)

plt.xlabel('Pre-processor service time')
plt.ylabel('Frequency')
plt.title(r'Pre-processing time required for n=2')
plt.axis([0, 1.5, 0, 5])

plt.show()


x = [utilities.pre_processor_service_time(5) for _ in range(1000000)]

plt.hist(x, bins=100, normed=1, facecolor='green', alpha=0.75)

plt.xlabel('Pre-processor service time')
plt.ylabel('Frequency')
plt.title(r'Pre-processing time required for n=5')
plt.axis([0, 4, 0, 2])

plt.show()


x = [utilities.pre_processor_service_time(9) for _ in range(1000000)]

plt.hist(x, bins=100, normed=1, facecolor='green', alpha=0.75)

plt.xlabel('Pre-processor service time')
plt.ylabel('Frequency')
plt.title(r'Pre-processing time required for n=9')
plt.axis([0, 6, 0, 1.2])

plt.show()



x = [utilities.sub_task_service_time(2) for _ in range(1000000)]

plt.hist(x, bins=np.arange(0,max(x)+0,0.25), normed=1, facecolor='green', alpha=0.75)

plt.xlabel('Server sub-task service time')
plt.ylabel('Frequency')
plt.title(r'Server sub-task time required for n=2')
plt.axis([0, 25, 0, 0.6])

plt.show()

x = [utilities.sub_task_service_time(5) for _ in range(1000000)]

plt.hist(x, bins=np.arange(0,max(x)+0,0.1), normed=1, facecolor='green', alpha=0.75)

plt.xlabel('Server sub-task service time')
plt.ylabel('Frequency')
plt.title(r'Server sub-task time required for n=5')
plt.axis([0, 8, 0, 2.5])

plt.show()

x = [utilities.sub_task_service_time(9) for _ in range(1000000)]

plt.hist(x, bins=np.arange(0,max(x)+0,0.03), normed=1, facecolor='green', alpha=0.75)

plt.xlabel('Server sub-task service time')
plt.ylabel('Frequency')
plt.title(r'Server sub-task time required for n=9')
plt.axis([0, 3, 0, 6])

plt.show()
