import gym
import tensorflow
import numpy as np
from collections import deque 
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import random
class MyAgent:
    def __init__(self, state_size, action_size):
        self.state_size=state_size
        self.action_size = action_size

        #Khởi tạo replat buffer
        self.replay_buffer=deque(maxlen=50000000)
        
        #Tham số của Agent
        self.gamma=0.99
        self.epsilon=1.0
        self.epsilon_min=0.01
        self.epsilon_decay=0.9995
        self.learning_rate=0.001
        self.update_targetnn_rate = 10

        self.main_network = self.get_nn()
        self.target_network = self.get_nn()

        #Update weight cua mang target bang mang main
        self.target_network.set_weights(self.main_network.get_weights())

    def get_nn(self):
        model = Sequential()

        model.add(Dense(350, activation = 'relu', input_dim = self.state_size))
        model.add(Dense(140, activation='relu'))
        model.add(Dense(self.action_size))

        model.compile(loss= 'mse', optimizer= Adam(learning_rate=self.learning_rate))
        return model
    
    def save_experience(self, state, action, reward, next_sate, terminal):
        self.replay_buffer.append((state, action, reward, next_sate, terminal))

    def get_batch_from_buffer(self, batch_size):
        exp_batch = random.sample(self.replay_buffer, batch_size)

        state_batch = np.array([batch[0] for batch in exp_batch]).reshape(batch_size, self.state_size)
        action_batch = np.array([batch[1] for batch in exp_batch])
        reward_batch = [batch[2] for batch in exp_batch]
        next_state_batch = np.array([batch[3] for batch in exp_batch]).reshape(batch_size, self.state_size)
        terminal_batch = [batch[4] for batch in exp_batch]
        return state_batch, action_batch, reward_batch, next_state_batch, terminal_batch
    
    def train_main_network(self, batch_size):
        state_batch, action_batch, reward_batch, next_state_batch, terminal_batch = self.get_batch_from_buffer(batch_size)


        #Lấy Q value của state hiện tại
        q_values = self.main_network.predict(state_batch, verbose=0)
        #Lấy max Q value của state s'(State chuyển từ s với action A)
        next_q_values = self.target_network.predict(next_state_batch, verbose=0)
        max_next_q = np.amax(next_q_values, axis=1)
        
        for i in range(batch_size):
            new_q_values = reward_batch[i] if terminal_batch[i] else reward_batch[i] + self.gamma*max_next_q[i]
            q_values[i][action_batch[i]]= new_q_values
        self.main_network.fit(state_batch, q_values, verbose=1)
    
    def make_decison(self, state):
        if random.uniform(0,1) < self.epsilon:
            return np.random.randint(self.action_size)
        
        number = int(state[3])
        valid_agv = bin(number)[2:].zfill(12)
        valid_actions=[]

        for agv in range(len(valid_agv)):
            if valid_agv[agv]=='1':
                for i in range(3):
                    valid_actions.append(12*i + agv)
        
        state = state.reshape((1, self.state_size))
        q_values = self.main_network.predict(state, verbose=0)
        valid_q_values = [q_values[0][action] for action in valid_actions]

        return valid_actions[np.argmax(valid_q_values)]
    

