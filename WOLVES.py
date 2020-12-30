# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 13:16:58 2020

@author: Administrator
"""

# 需要用的包
import numpy as np
import random # random 0，1 之间 uniform 自定义区间 random.random()
import time

# 外部子程序
import problem_2 as problem # 导入 problem  problem_1 简单问题 problem_2 调度问题 

###########################-设置迭代次数及种群大小-#############################
maxitr = 20 # 最大迭代次数 max iteration generation
psize = 200 # 种群数量  population size

t0 = time.process_time()
###########################-随机生成初始种群-##################################
X = problem.criarRand(psize) # 生成数量为 psize 的初始解集

###########################-对初始种群求解-####################################
Adapt = [] # 适应度值的集合
for i in range(psize): # 都求解一遍
    Adapt.append(problem.reso(X[i])) # 结果保存到 adapt[] 中
Adapt = np.array(Adapt)
# print('初始适应度值：\n', Adapt)

Rank = Adapt.argsort()
# print('适应度值 adapt 顺序索引:')
# print(Rank)

# solu 是一个待更新的解
def probe(solu): # 根据原 X 向 XA XB XC 三个方向探测  （A 和 C 每次都是随机？） 经测试，此种效果更好
    a = 0.2+2*(2 - 2*t/maxitr) # 控制距离参数（从第 1 代开始） t 当前迭代次数，a 控制距离参数，MI 最大迭代次数 # 测试学习率系数 # 增大学习率，增加随机性？ 产生一定变异有助于随机寻优？
    X1 = X[Rank[0]] + (2*a*random.random() - a)*abs((2*t/maxitr + random.random())*X[Rank[0]] - solu) # 提示不能对 float 类型进行乘法，改成 np.array 格式可破
    X2 = X[Rank[1]] + (2*a*random.random() - a)*abs((2*t/maxitr + random.random())*X[Rank[1]] - solu)
    X3 = X[Rank[2]] + (2*a*random.random() - a)*abs((2*t/maxitr + random.random())*X[Rank[2]] - solu)
    return (X1 + X2 + X3)/3 #  + X4 + X5 + X6

def update(n): # 对排名第 n 的 X 向量进行试探更新
    explor = probe(X[Rank[n]]) # Rank[n] 为第 n 好的 X 向量位置，固定根据 X[Rank[n]]向三个方向延申的 探测向量值
    resexp = problem.reso(explor) # 对 探测值 求解
    if resexp <= Adapt[Rank[n]]: # 如果新 PX 值更优
        X[Rank[n]] = explor # X[i] 更新为 探测值 **********************************************************    用 onea 归一化
        Adapt[Rank[n]] = resexp # 排名第 n 的 X 向量对应的适应度值更新为 resexp

def Iteration(t): # 第 t 代迭代
    for n in range(3, psize): # 从 第 4 个 X[arrange[3]] 开始试探
        update(n) # 逐个更新
#    print('适应度值：\n', Adapt) # 把 适应度值 显示出来看看
    global Rank # ******************************************* global 变为全局变量
    Rank = Adapt.argsort() # 全部求解完成后排列一下
    #print(Rank)
#    print('Rank', Rank)

## 前三的结果显示一下    
    print('第 1', X[Rank[0]], '适应度值：', Adapt[Rank[0]])
    #print('第 2', X[Rank[1]], '适应度值：', Adapt[Rank[1]])
    #print('第 3', X[Rank[2]], '适应度值：', Adapt[Rank[2]])
#############-迭代-############################################################
for t in range(maxitr): # 迭代
    print('第%d次迭代:'%t)
    Iteration(t)
print('最优解为：\n', X[Rank[0]]) # 最终输出排在第 0 位的解，即最优解
print('最优适应度：\n', Adapt[Rank[0]])
#print('设备选择：\n', MCH)
#print('开始时间：\n', STP)
#print('浇次开始时间：\n', STP)

print('求解时间：', time.process_time() - t0)
#############-解一编最优解-#####################################################

#problem.reso(X[Rank[0]])
