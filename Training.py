import numpy as np
from collections import deque 
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import random
import keras
from Enviroment import Enviroment
from Task import Task, QueueTask, ContainerTask
from Agent import MyAgent

queue_task=QueueTask()
container_task=ContainerTask()

evn = Enviroment(queue_task, container_task)
state_size = evn.observation_space.shape[0]
action_size = evn.action_space.n

# Định nghĩa tham số khác
n_episodes = 5000
n_timesteps = 500000
batch_size = 32

#Khởi tạo agent
my_agent = MyAgent(state_size, action_size)
my_agent.main_network = keras.models.load_model("Agent.h5")
my_agent.target_network.set_weights(my_agent.main_network.get_weights())
my_agent.epsilon = 0.44923907735


total_time_step = 0


for ep in range(n_episodes):

    ep_rewards = 0
    queue_task=QueueTask()
    container_task=ContainerTask()
    f = open('test.txt',"r")
    for k in range(1,9):
        for i in range(10):
            locate="QC"+str(k)
            tmp = f.readline().split()
            destination_x=float(tmp[0])
            destination_y=float(tmp[1])
            task=Task(locate, destination_x, destination_y)
            queue_task.push_task(task)
    for k in range(1,9):
        task=queue_task.pop_task("QC"+str(k))
        container_task.add_task(task.locate, task)
    f.close()
        
    evn=Enviroment(queue_task, container_task)
    state = evn.reset()
    for t in range(n_timesteps):
        total_time_step+=1
        if total_time_step % my_agent.update_targetnn_rate ==0:
            my_agent.target_network.set_weights(my_agent.main_network.get_weights())
        
        tmp=0
        
        old_state=state.copy()
        action = my_agent.make_decison(state)
        next_state, reward, terminal, _, _, _= evn.step(action)
        my_agent.save_experience(old_state, action, reward, next_state, terminal)
        state = next_state
        ep_rewards+=reward

        if terminal:
            print("Ep", ep+1, "reach terminal reward: ", ep_rewards)
            break

        if len(my_agent.replay_buffer) > batch_size:
            my_agent.train_main_network(batch_size)
    
    if my_agent.epsilon > my_agent.epsilon_min:
        my_agent.epsilon = my_agent.epsilon*my_agent.epsilon_decay
    my_agent.main_network.save("Agent_new.keras")