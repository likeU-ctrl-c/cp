# -*- coding:utf-8 -*-
#@Time : 2021/3/18 16:30
#@Author: deepLove
#@File : env.py.py
import itertools

import gym
from gym import spaces
from gym.utils import seeding
import numpy as np

class RouletteEnv(gym.Env):
    """Simple roulette environment
    The roulette wheel has 37 spots. If the bet is 0 and a 0 comes up,
    you win a reward of 35. If the parity of your bet matches the parity
    of the spin, you win 1. Otherwise you receive a reward of -1.
    The long run reward for playing 0 should be -1/37 for any state
    The last action (38) stops the rollout for a return of 0 (walking away)
    """

    def __init__(self):
        print("初始化环境")
        self.box = self.allboll()
        print("得到所有可能号码")
        self.n = len(self.box)
        self.action_space = spaces.Discrete(self.n)

        self.seed()
        self.currentZ = 0  # 当前的中奖号码
        self.zjarray=[]  # 中奖号的下标
        print("处理中奖号码")
        # 中奖号码
        self.zhongall()
        self.observation_space = np.array(self.zjarray)

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        print("进入选择判断环节")
        assert self.action_space.contains(action)
        selectArray = self.box[action]

        self.currentZ += 1

        if self.currentZ >=len(self.zjarray)-1:
            self.currentZ = 0
        zhongjiang = self.box[self.zjarray[self.currentZ]]
        reward = self.rule(zhongjiang, selectArray)
        print(selectArray,'/',zhongjiang,"=",self.currentZ)

        return 0, reward, True, {}
        # if action == self.n - 1:
        #     # observation, reward, done, info
        #     return 0, 0, True, {}
        #
        # # N.B. np.random.randint draws from [A, B) while random.randint draws from [A,B]
        # val = self.np_random.randint(0, self.n - 1)
        # if val == action == 0:
        #     reward = self.n - 2.0
        # elif val != 0 and action != 0 and val % 2 == action % 2:
        #     reward = 1.0
        # else:
        #     reward = -1.0
        # return 0, reward, False, {}

    def reset(self):
        return self.zjarray[self.currentZ]
    # 工具
    def red(self):
        reds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                29,
                30, 31, 32, 33]
        r = itertools.combinations(reds, 6)
        r = list(r)
        return list(r)

    def allboll(self):
        print("开始读取所有号码")
        f = open('all.csv', 'r')
        data = f.readlines()
        f.close()
        res = []
        print("处理所有号码格式")
        for i in data:
            i = i.strip().split(',')
            tmp = []
            for r in i:
                tmp.append(int(r))
            res.append(tmp)
        return res
        # reds = self.red()
        # allbos = []
        # f = open('all.csv', 'a')
        # for r in reds:
        #     r = list(r)
        #
        #     for i in range(1, 17):
        #         tmpr = r[:]
        #         tmpr.append(i)
        #         print(tmpr)
        #         sum = 0
        #         for t in tmpr:
        #             sum+=1
        #             if sum<7:
        #                 f.write(str(t)+',')
        #             else:
        #                 f.write(str(t))
        #         f.write('\n')
        #
        #         allbos.append(tmpr)
        # f.close()

        return allbos
    def zhongall(self):
        print("所有中奖号码")
        f=open('index.csv','r')
        data = f.read().strip().split(',')
        print(data[-1])
        for i in data[:-1]:
            # print(i)
            self.zjarray.append(int(i))
        print(self.zjarray)
        # data=f.readlines()
        # f.close()
        # for i in data:
        #     i=i.strip().split(',')
        #     tmp = []
        #     for j in i:
        #         j = int(j)
        #         tmp.append(j)
        #     self.zjarray.append(tmp[1:])
        # print(self.zjarray[:10])
        # f=open("index.csv",'a')
        # print("开始找下标")
        # for i in range(len(self.box)):
        #     # print(self.box[i])
        #     while(self.box[i] in self.zjarray) :
        #         index = self.zjarray.index(self.box[i])
        #         print(index)
        #         self.zjarray[index] = i
        # print("找下标结束")
        # for m in self.zjarray:
        #     print(m)
        #     f.write(str(m)+',')
        f.close()


            # print(self.box.index(tmp[1:]))
        print("所有中奖号码结束")
        # print(data)

    def rule(self, z, select):
        allcount = -1
        d = z
        red = select[:6]
        blue = select[-1]
        zrnum = 0  # 中红球的数量
        zblue = False
        for r in red:
            if r in d[:6]:
                zrnum += 1
        if int(blue) == int(d[-1]):
            zblue = True
        # 1
        if zblue and zrnum == 6:
            allcount = 6

        # 2
        elif zrnum == 6:
            allcount = 5

        # 3
        elif zblue and zrnum == 5:
            allcount = 4

        # 4
        elif (zblue and zrnum == 4) or zrnum == 5:
            allcount = 3

        # 5
        elif (zblue and zrnum == 3) or zrnum == 4:
            allcount = 2

        # 6
        elif zblue:
            allcount = 1

        return allcount


# r = RouletteEnv()
# print(r.zhongall())
