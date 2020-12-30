# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 20:44:54 2020

@author: Administrator
"""

import random
import numpy as np
#import matplotlib.pyplot as plt
import time

# 外部子程序
import problem_2 as problem # 导入 problem 2

y = [] # 记录迭代的解
t0 = time.process_time()
class PSO:
    def __init__(self, parameters):
        """
        particle swarm optimization
        parameter: a list type, like [NGEN, pop_size, var_num_min, var_num_max]
        """
        # 初始化
        self.NGEN = parameters[0]    # 迭代的代数
        self.pop_size = parameters[1]    # 种群大小
        self.var_num = len(parameters[2])     # 变量个数
        self.bound = []                 # 变量的约束范围
        self.bound.append(parameters[2])
        self.bound.append(parameters[3])
 
        self.pop_x = np.zeros((self.pop_size, self.var_num))    # 所有粒子的位置
        self.pop_v = np.zeros((self.pop_size, self.var_num))    # 所有粒子的速度
        self.p_best = np.zeros((self.pop_size, self.var_num))   # 每个粒子最优的位置
        self.g_best = np.zeros((1, self.var_num))   # 全局最优的位置
 
        # 初始化第0代初始全局最优解
        temp = -1
        for i in range(self.pop_size):
            for j in range(self.var_num):
                self.pop_x[i][j] = random.uniform(self.bound[0][j], self.bound[1][j])
                self.pop_v[i][j] = random.uniform(0, 1)
            self.p_best[i] = self.pop_x[i]      # 储存最优的个体
            fit = self.fitness(self.p_best[i])
            if fit > temp:
                self.g_best = self.p_best[i]
                temp = fit
 
    def fitness(self, ind_var):
        """
        个体适应值计算
        """
        return problem.reso(ind_var)
        # x1 = ind_var[0]
        # x2 = ind_var[1]
        # x3 = ind_var[2]
        # x4 = ind_var[3]
        # y = x1 ** 2 + x2 ** 2 + x3 ** 3 + x4 ** 4
        # return y
 
    def update_operator(self, pop_size):
        """
        更新算子：更新下一时刻的位置和速度
        """
        c1 = 2     # 学习因子，一般为2
        c2 = 2
        w = 0.4    # 自身权重因子
        for i in range(pop_size):
            # 更新速度
            self.pop_v[i] = w * self.pop_v[i] + c1 * random.uniform(0, 1) * (
                        self.p_best[i] - self.pop_x[i]) + c2 * random.uniform(0, 1) * (self.g_best - self.pop_x[i])
            # 更新位置
            self.pop_x[i] = self.pop_x[i] + self.pop_v[i]
            # 越界保护
            for j in range(self.var_num):
                if self.pop_x[i][j] < self.bound[0][j]:
                    self.pop_x[i][j] = self.bound[0][j]
                if self.pop_x[i][j] > self.bound[1][j]:
                    self.pop_x[i][j] = self.bound[1][j]
            # 更新p_best和g_best
            if self.fitness(self.pop_x[i]) < self.fitness(self.p_best[i]):
                self.p_best[i] = self.pop_x[i]
            if self.fitness(self.pop_x[i]) < self.fitness(self.g_best):
                self.g_best = self.pop_x[i]
 
    def main(self):
        global y
        popobj = []
        self.ng_best = np.zeros((1, self.var_num))[0]
        for gen in range(self.NGEN):
            self.update_operator(self.pop_size)
            popobj.append(self.fitness(self.g_best))
            print('############ Generation {} ############'.format(str(gen + 1)))
            if self.fitness(self.g_best) < self.fitness(self.ng_best):
                self.ng_best = self.g_best.copy()
            print('最好的位置：{}'.format(self.ng_best))
            print('最优的函数值：{}'.format(self.fitness(self.ng_best)))
            y.append(self.fitness(self.ng_best))
        print("---- End of (successful) Searching ----")
 
#        plt.figure()
#        plt.title("Figure1")
#        plt.xlabel("iterators", size=14)
#        plt.ylabel("fitness", size=14)
#        t = [t for t in range(self.NGEN)]
#        plt.plot(t, popobj, color='b', linewidth=2)
#        plt.show()
 
 
if __name__ == '__main__':
    NGEN = 32
    popsize = 100
    low = [0, 0, 0, 0]
    up = [800, 800, 800, 800]
    parameters = [NGEN, popsize, low, up]
    pso = PSO(parameters)
    pso.main()

print(y)
print('求解时间：', time.process_time() - t0)