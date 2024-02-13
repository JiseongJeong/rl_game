import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import gym # for environment
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam # adaptive momentum
import random
import sys


class DQLAgent():

    def __init__(self, env):  ###  env: gym인스턴스클래스
                                # https://github.com/openai/gym/blob/master/gym/envs/classic_control/cartpole.py
        # (하이퍼)파라메터 설정
        # this part is for neural network or build_model()
        self.state_size = env.observation_space.shape[0] # network input 노드 사이즈 할당
        self.action_size = env.action_space.n # output(action to 선택 from 이전 state)

        # episode step시 학습률 조정 등(대충설정)
        self.gamma = 0.9
        self.learning_rate = 0.001

        # epsilon decay에 대한 설명 (최하단 별도 블럭)
        self.epsilon = 1
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01

        # 메모리 폭발 방지. 리스트 뒤쪽에 할당하고 앞쪽을 dequeing(pop)하는 방식
        self.memory = deque(maxlen = 1000) #선입선출 fifo
        self.model = self.build_model()

    # @classmethod
    # def jiseong_test(cls):
    #     if cls.sub_cls:
    #         attr: cls.sub_cls
    #         [attr for attr in cls.att_list_js_test]
    #     else:
    #         pass

    def build_model(self):
        # neural network for deep Q learning
        model = Sequential()
        model.add(Dense(48, input_dim = self.state_size, activation = 'tanh')) # first hidden layer
        model.add(Dense(self.action_size, activation = 'linear')) # output layer
        model.compile(loss = 'mse', optimizer = Adam(lr = self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        # 수제storaging해주기
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        # acting, exploit or explore
        if random.uniform(0,1) <= self.epsilon:
            return env.action_space.sample()
        else:
            act_values = self.model.predict(state)
            return np.argmax(act_values[0])  # 일종의 griddy picking이나 이는 가장 단순한 방식의 예


    def replay(self, batch_size):
        # training

        if len(self.memory) < batch_size:
            return # memory is still not full

        minibatch = random.sample(self.memory, batch_size) # take 16 (batch_size) random samples from memory
        for state, action, reward, next_state, done in minibatch:
            if done: # if the game is 끝, I dont have next state, I just have reward
                target = reward
            else:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
                # target = R(s,a) + gamma * max Q`(s`,a`)
                # target (max Q` value) is output of Neural Network which takes s` as an input
                # amax(): flatten the lists (make them 1 list) and take max value
            train_target = self.model.predict(state) # s --> NN --> Q(s,a)=train_target
            train_target[0][action] = target
            self.model.fit(state, train_target, verbose = 0) # verbose: dont show loss and epoch

    def adaptiveEGreedy(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


env = gym.make('CartPole-v1')
agent = DQLAgent(env)

batch_size = 32
episodes = 2
for e in range(episodes):

    # 매 iter의 맨앞 reset 필수.
    state = env.reset()
    state = np.reshape(state[0], [1,4])

    time = 0
    while True:

        # act
        action = agent.act(state)

        # step   -->튜플
        next_state, reward, done, _ , _= env.step(action)
        next_state = np.reshape(next_state, [1,4])

        # storage 저장한 후에 update state 실시
        agent.remember(state, action, reward, next_state, done)
        state = next_state

        # replay
        agent.replay(batch_size)

        # adjust epsilon
        agent.adaptiveEGreedy()

        time += 1

        if done:
            print('episode: {}, time: {}'.format(e, time))
            break