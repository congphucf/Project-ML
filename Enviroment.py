import gym
from gym.spaces import Discrete, Box
import numpy as np
from Task import Task, QueueTask, ContainerTask 
import math
import random
class Enviroment(gym.Env):
    def __init__(self, queue_task, container_task) -> None:
        super().__init__()
        #Action can take
        self.action_space = Discrete(36) # Action i in chose AGV i%12+1 and rule i//12+1
        self.observation_space = Box(low=0, high=1, shape=(28,), dtype=np.float32)
        self.queue_task=queue_task
        self.container_task=container_task

        self.agv_complie_time =[0]*12
        self.agv_busy=[0]*12
        self.qc_waiting_time = [0]*8
        self.qc_wait = [0]*8
    def reset(self):
        self.state = np.array([0, 0, 0, 4095, 150, 1200, 450, 1200, 750, 1200, 1050, 1200, 1350, 1200, 1650, 1200, 1950, 1200, 2250, 1200, 2550, 1200, 2850, 1200, 3150, 1200, 3450, 1200], dtype=np.float32)

        self.state[0]=len(self.container_task.container_task)
        sum_dadt=0
        for key, value in self.container_task.container_task.items():
            sum_dadt+=value.transport_distance
        self.state[2]=sum_dadt/self.state[0]
        self.agv_complie_time =[0]*12
        self.qc_waiting_time = [0]*8
        self.qc_wait = [0]*8
        return self.state
    
    def step(self, action):
        agv=action%12
        rule=action//12+1

        if (self.agv_busy[agv]==1):
            reward = 0
            return self.state, reward, False, [0,0], None, None
        else:
            #Chon qc
            if rule ==1:
                qc_choose = self.container_task.firstComeFirstServed()
            if rule ==2:
                qc_choose = self.container_task.longestWatingTime()
            if rule ==3:
                qc_choose = self.container_task.shortestJobFirst()

        #Update wait time cho qc
        task = self.container_task.pop_task(qc_choose)
        self.qc_wait[int(qc_choose[2])-1] = 1
        self.qc_waiting_time[int(qc_choose[2])-1] = (self.state[4+agv*2] + math.fabs(self.state[3+agv*2]-int(qc_choose[2])*450+225))/10

        #Update complie time cho agv
        self.agv_complie_time[agv]= self.qc_waiting_time[int(qc_choose[2])-1]  + task.transport_distance/10
        self.state[3+agv*2]=task.destination_x
        self.state[4+agv*2]=task.destination_y
        self.agv_busy[agv]=1
        destination = []
        destination.append(task.destination_x)
        destination.append(task.destination_y)

        #Tinh reward
        reward = 0.1*((230-task.waiting_time)+(230-self.agv_complie_time[agv]))
        
        time_to_caculate=[]
        time_to_caculate.append(task.waiting_time)
        time_to_caculate.append(self.agv_complie_time[agv])

        #Tim next state
        if(len(self.container_task.container_task)==0):
            min_wait_time=1e9
            for k in range(len(self.qc_waiting_time)):
                if self.qc_waiting_time[k]<min_wait_time and self.qc_wait[k]==1 and len(self.queue_task.queue_task["QC"+str(k+1)]):
                    min_wait_time=self.qc_waiting_time[k]

            for qc, task_in_container in self.container_task.container_task.items():
                self.container_task.container_task[qc].waiting_time+=min_wait_time

            for k in range(len(self.agv_complie_time)):
                if self.agv_busy[k]==1:
                    self.agv_complie_time[k]=max(0, self.agv_complie_time[k]-min_wait_time)
                    if self.agv_complie_time[k]==0:
                        self.agv_busy[k]=0
            
            for k in range(len(self.qc_waiting_time)):
                if self.qc_wait[k]==1 and len(self.queue_task.queue_task["QC"+str(k+1)])!=0:
                    self.qc_waiting_time[k]=max(0, self.qc_waiting_time[k]-min_wait_time)
                    tmp = min_wait_time - self.qc_waiting_time[k]
                    if self.qc_waiting_time[k]==0:
                        self.qc_wait[k]=0
                        task=self.queue_task.pop_task("QC"+str(k+1))
                        if task!=None:
                            self.container_task.add_task("QC"+str(k+1), task)
                            self.container_task.container_task["QC"+str(k+1)].waiting_time = tmp

            """for k in range(len(self.qc_waiting_time)):
                self.qc_waiting_time[k]=max(0,self.qc_waiting_time[k]-min_wait_time)
                tmp = min_wait_time - self.qc_waiting_time[k]
                if self.qc_waiting_time[k]==0 and self.qc_wait[k]==1:
                    self.qc_wait[k]=0
                    task=self.queue_task.pop_task("QC"+str(k+1))
                    if task!=None:
                        self.container_task.add_task("QC"+str(k+1), task)
                        self.container_task.container_task["QC"+str(k+1)].waiting_time = tmp
            """

        count=0
        for agv in self.agv_busy:
            if agv==0:
                count+=1
        if(count==0):
            min_time=1e9
            for time in self.agv_complie_time:
                if time<min_time and time>0:
                    min_time=time

            for qc, task_in_container in self.container_task.container_task.items():
                self.container_task.container_task[qc].waiting_time+=min_time

            for k in range(len(self.agv_complie_time)):
                self.agv_complie_time[k]=max(0, self.agv_complie_time[k]-min_time)
                if self.agv_complie_time[k]==0 and self.agv_busy[k]==1:
                    self.agv_busy[k]=0

            """for k in range(len(self.qc_waiting_time)):
                self.qc_waiting_time[k]=max(0,self.qc_waiting_time[k]-min_time)
                tmp=min_time-self.qc_waiting_time[k]
                if self.qc_waiting_time[k]==0 and self.qc_wait[k]==1 :
                    self.qc_wait[k]=0
                    task=self.queue_task.pop_task("QC"+str(k+1))
                    if task!=None:
                        self.container_task.add_task("QC"+str(k+1), task)
                        self.container_task.container_task["QC"+str(k+1)].waiting_time = tmp
            """
            for k in range(len(self.qc_waiting_time)):
                if self.qc_wait[k]==1 and len(self.queue_task.queue_task["QC"+str(k+1)])!=0:
                    self.qc_waiting_time[k]=max(0, self.qc_waiting_time[k]-min_time)
                    tmp = min_time - self.qc_waiting_time[k]
                    if self.qc_waiting_time[k]==0:
                        self.qc_wait[k]=0
                        task=self.queue_task.pop_task("QC"+str(k+1))
                        if task!=None:
                            self.container_task.add_task("QC"+str(k+1), task)
                            self.container_task.container_task["QC"+str(k+1)].waiting_time = tmp


        self.state[0]=len(self.container_task.container_task)
        if self.state[0]!=0:
            sum_dadt=0
            sum_waiting_time=0
            for qc, task_on_qc in self.container_task.container_task.items():
                sum_dadt+=task_on_qc.transport_distance
                sum_waiting_time+=task_on_qc.transport_distance
            self.state[2]=sum_dadt/self.state[0]
            self.state[1]=sum_waiting_time/self.state[0]
            terminal = False
        else:
            terminal=True
            self.state[1]=0
            self.state[2]=0
        tmp=0
        for k in range(len(self.agv_busy)):
            if(self.agv_busy[k]==0):
                tmp = tmp+pow(2,(12-k-1))
        self.state[3]=tmp
        return self.state, reward, terminal, time_to_caculate, qc_choose, destination
    


