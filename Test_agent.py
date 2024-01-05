from Enviroment import Enviroment
from Task import Task, QueueTask, ContainerTask
import keras
import numpy as np
import random

queue_task=QueueTask()
container_task=ContainerTask()
queue_task1=QueueTask()
container_task1=ContainerTask()
queue_task2=QueueTask()
container_task2=ContainerTask()
queue_task3=QueueTask()
container_task3=ContainerTask()
f = open('test.txt',"r")
for k in range(1,9):
    for i in range(10):
        locate="QC"+str(k)

        tmp = f.readline().split()
        destination_x=float(tmp[0])
        destination_y=float(tmp[1])
        task=Task(locate, destination_x, destination_y)
        queue_task.push_task(task)
        queue_task1.push_task(task)
        queue_task2.push_task(task)
        queue_task3.push_task(task)
for k in range(1,9):
    task = queue_task.pop_task("QC"+str(k))
    task1 = queue_task1.pop_task("QC"+str(k))
    task2 = queue_task2.pop_task("QC"+str(k))
    task3 = queue_task3.pop_task("QC"+str(k))
    container_task.add_task(task.locate, task)
    container_task1.add_task(task1.locate, task1)
    container_task2.add_task(task1.locate, task1)
    container_task3.add_task(task1.locate, task1)
f.close()

f = open("action_1.txt", "w")
my_agent = keras.models.load_model("Agent.keras")
env = Enviroment(queue_task, container_task)

state = env.reset()
state_size = env.observation_space.shape[0]

terminal=False
total_reward=0
waiting_time = 0
compile_time = 0

f.write("Mix:\n")

while(terminal==False):
    number = int(state[3])
    valid_agv = bin(number)[2:].zfill(12)
    valid_actions=[]

    for agv in range(len(valid_agv)):
        if valid_agv[agv]=='1':
            for i in range(3):
                valid_actions.append(12*i + agv)
                
    state = state.reshape((1, state_size))
    q_values = my_agent.predict(state, verbose=0)
    valid_q_values = [q_values[0][action] for action in valid_actions]
    action = valid_actions[np.argmax(valid_q_values)]
    next_state, reward, terminal, time, qc_choose, destination = env.step(action)

    print("Choose agv", action%12, "with rule", action//12+1, "take", qc_choose)
    f.write(f"Choose agv {action%12} with rule {action//12+1} take {qc_choose} to destiantion {destination} \n")
    
    total_reward+=reward
    state=next_state
    waiting_time+=time[0]
    compile_time+=time[1]
print("Mix:",total_reward)
print("Waiting_time:",waiting_time)
print("Compile_time:",compile_time)

#Rule 1
my_agent = keras.models.load_model("Agent_new.keras")
env = Enviroment(queue_task1, container_task1)

waiting_time_1 = 0
compile_time_1 = 0

state = env.reset()
state_size = env.observation_space.shape[0]

terminal=False
total_reward1=0

f.write("Rule 1: \n")
while(terminal==False):
    number = int(state[3])
    valid_agv = bin(number)[2:].zfill(12)
    valid_actions=[]

    for agv in range(len(valid_agv)):
        if valid_agv[agv]=='1':
            valid_actions.append(agv)

    state = state.reshape((1, state_size))
    q_values = my_agent.predict(state, verbose=0)
    valid_q_values = [q_values[0][action] for action in valid_actions]
    action = valid_actions[np.argmax(valid_q_values)]
    next_state, reward, terminal, time, qc_choose, destination = env.step(action)


    f.write(f"Choose agv {action%12} with rule {action//12+1} take {qc_choose} to destionation {destination} \n")

    total_reward1+=reward
    state=next_state
    waiting_time_1+=time[0]
    compile_time_1+=time[1]
print("Rule 1:", total_reward1)
print("Waiting time:",waiting_time_1)
print("Compile_time:",compile_time_1)


#Rule 2
my_agent = keras.models.load_model("Agent.keras")
env = Enviroment(queue_task2, container_task2)

state = env.reset()
state_size = env.observation_space.shape[0]

waiting_time_2 = 0
compile_time_2 = 0
terminal=False
total_reward2=0

f.write("Rule 2: \n")

while(terminal==False):
    number = int(state[3])
    valid_agv = bin(number)[2:].zfill(12)
    valid_actions=[]

    for agv in range(len(valid_agv)):
        if valid_agv[agv]=='1':
            valid_actions.append(12+agv)

    state = state.reshape((1, state_size))
    q_values = my_agent.predict(state, verbose=0)
    valid_q_values = [q_values[0][action] for action in valid_actions]
    action = valid_actions[np.argmax(valid_q_values)]
    next_state, reward, terminal, time, qc_choose, destination = env.step(action)


    f.write(f"Choose agv {action%12} with rule {action//12+1} take {qc_choose} to destionation {destination} \n")
    
    total_reward2+=reward
    state=next_state
    waiting_time_2+=time[0]
    compile_time_2+=time[1]
print("Rule 2:", total_reward2)
print("Waiting time:",waiting_time_2)
print("Compile_time:",compile_time_2)

#Rule 3
my_agent = keras.models.load_model("Agent.keras")
env = Enviroment(queue_task3, container_task3)

state = env.reset()
state_size = env.observation_space.shape[0]

terminal=False
total_reward3=0
waiting_time_3 = 0
compile_time_3 = 0
f.write("Rule 3:\n")
while(terminal==False):
    number = int(state[3])
    valid_agv = bin(number)[2:].zfill(12)
    valid_actions=[]

    for agv in range(len(valid_agv)):
        if valid_agv[agv]=='1':
            valid_actions.append(24+agv)

    state = state.reshape((1, state_size))
    q_values = my_agent.predict(state, verbose=0)
    valid_q_values = [q_values[0][action] for action in valid_actions]
    action = valid_actions[np.argmax(valid_q_values)]
    next_state, reward, terminal, time, qc_choose, destination = env.step(action)

    f.write(f"Choose agv {action%12} with rule {action//12+1} take {qc_choose}to destionation {destination} \n")

    total_reward3+=reward
    state=next_state
    waiting_time_3+=time[0]
    compile_time_3+=time[1]
print("Rule 3", total_reward3)
print("Waiting time:",waiting_time_3)
print("Compile_time:",compile_time_3)



