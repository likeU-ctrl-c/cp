
# -*- coding:utf-8 -*-
#@Time : 2021/3/19 15:05
#@Author: deepLove
#@File : test.py.py

# -*- coding: utf-8 -*-
import random
import gym
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

from env import RouletteEnv

EPISODES = 1000000000  # 让 agent 玩游戏的次数


class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95  # 计算未来奖励时的折算率
        self.epsilon = 1.0  # agent 最初探索环境时选择 action 的探索率
        self.epsilon_min = 0.01  # agent 控制随机探索的阈值
        self.epsilon_decay = 0.995  # 随着 agent 玩游戏越来越好，降低探索率
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma *
                          np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def saveMode(self):
        self.model.save_weights('my_model_weights.h5')

    def loadMode(self):
        # 需要在代码中初始化一个完全相同的模型
        self.model.load_weights('my_model_weights.h5')


if __name__ == "__main__":

    # 初始化 gym 环境和 agent
    # env = gym.make('CartPole-v1')
    # state_size = env.observation_space.shape[0]
    # action_size = env.action_space.n
    env = RouletteEnv()
    state_size = 1
    action_size = env.action_space.n
    agent = DQNAgent(state_size, action_size)

    done = False
    batch_size = 32

    # 开始迭代游戏
    for e in range(EPISODES):

        # 每次游戏开始时都重新设置一下状态
        state = env.reset()
        print("state=",state)
        # state = np.reshape(state, [1, state_size])

        # time 代表游戏的每一帧，
        # 每成功保持杆平衡一次得分就加 1，最高到 500 分，
        # 目标是希望分数越高越好
        for time in range(500):
            # 每一帧时，agent 根据 state 选择 action
            action = agent.act(state)
            # 这个 action 使得游戏进入下一个状态 next_state，并且拿到了奖励 reward
            # 如果杆依旧平衡则 reward 为 1，游戏结束则为 -10
            next_state, reward, done, _ = env.step(action)
            reward = reward if not done else -10
            next_state = np.reshape(next_state, [1, state_size])

            # 记忆之前的信息：state, action, reward, and done
            agent.remember(state, action, reward, next_state, done)

            # 更新下一帧的所在状态
            state = next_state

            # 如果杆倒了，则游戏结束，打印分数
            if done:
                print("episode: {}/{}, score: {}, e: {:.2}"
                      .format(e, EPISODES, time, agent.epsilon))
                break

        # # 用之前的经验训练 agent
        # if len(agent.memory) > batch_size:
        #     agent.replay(batch_size)

        if e > 10000:
            agent.saveMode()
