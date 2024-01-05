from collections import deque
import math

class Task:
    def __init__(self, locate, destination_x, destination_y):
        self.locate=locate
        self.destination_x=destination_x
        self.destination_y=destination_y
        self.waiting_time = 0
        self.arrival_order = 0

        self.transport_distance = destination_y + math.fabs(destination_x-int(locate[2])*450+225)

    def update_waiting_time(self, now):
        self.wating_time = now-self.time_arrival

    def add_waiting_time(self, time_bonus):
        self.waiting_time+=time_bonus

class QueueTask:
    def __init__(self):
        self.queue_task={}
        for k in range (1, 9):
            self.queue_task["QC"+str(k)]= deque()

    def push_task(self ,task):
        self.queue_task[task.locate].append(task)

    def pop_task(self,locate):
        if len(self.queue_task[locate])!=0:
            return self.queue_task[locate].popleft()
        return None
    
    def check_empty(self):
        for qc, queue in self.queue_task.items():
            if len(queue)!=0:
                return True
        return False
    
class ContainerTask:
    def __init__(self):
        self.container_task={}

    def add_task(self, locate, task):
        task.arrival_order=len(self.container_task)+1
        self.container_task[locate]=task

    def pop_task(self, locate):
        task = self.container_task.pop(locate)
        for key, value in self.container_task.items():
            if value.arrival_order > task.arrival_order:
                value.arrival_order-=1
        return task

    def firstComeFirstServed(self):
        min_arrival_order=1e9
        qc_choose="QC0"
        for qc, task in self.container_task.items():
            if task.arrival_order<min_arrival_order:
                qc_choose=qc
        return qc_choose
    
    def longestWatingTime(self):
        max_waiting_time=-1e9
        qc_choose="QC0"
        for qc, task in self.container_task.items():
            if task.waiting_time>max_waiting_time:
                qc_choose=qc
        return qc_choose
    
    def shortestJobFirst(self):
        min_distance=1e9
        qc_choose="QC0"
        for qc, task in self.container_task.items():
            if task.transport_distance<min_distance:
                qc_choose=qc
        return qc_choose

