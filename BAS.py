# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 13:16:58 2020

@author: Administrator
"""

# 需要用的包
#import numba
import numpy as np
import random # random 0，1 之间 uniform 自定义区间 random.random()
#import copy
import time
import matplotlib.pyplot as plt

# 外部子程序
import problem_2 as problem # 导入 problem 2

t0 = time.process_time()
###########################-最大迭代次数（百次）-##################################
maxitr = 16
###########################-生成初始天牛-##################################
x = problem.defalt() # 天牛的初始质心，选取默认点
xbest = x
fbest = problem.reso(xbest)
#x = [100, 100, 100, 100]
R = len(x) # 粒子的维度
print('初始天牛质心：\n', x)
d0 = 1.0 # 两须之间距离的1/2 1.0

dire = np.array([random.random() for i in range(R)]) # 天牛右须指向左须的向量，天牛运动方向，随机生成
np.linalg.norm(dire) # 归一化

xl = x + d0 * (dire) # 天牛左须位置
xr = x - d0 * (dire) # 天牛右须位置

step = 20 # 初始步长 20
eta = 0.997 # 步长更新系数 997

###########################-对初始种群求解-####################################
# 更新
def update(): # 一次迭代更新
    global xl
    global xr
    global x
    global step
    global dire
    global fbest
    global xbest
    fleft = problem.reso(xl) # 左须适应度
    fright = problem.reso(xr) # 右须适应度
    if fleft < fright: # 如果左须优于右须
        x = x + step * dire * d0 * 2 # 质心向左须方向移动
        if fleft < fbest: # 如果左须比当前最优结果要好
            fbest = fleft # 更新最好适应度
            xbest = xl
    else: # 操作同上
        x = x - step * dire *  d0 * 2
        if fright < fbest:
            fbest = fright # 更新最好适应度
            xbest = xr
    dire = np.array([random.random() for i in range(R)]) # 更新天牛运动方向，随机产生
    np.linalg.norm(dire) # 归一化
    xl = x + d0 * (dire) # 更新天牛左须位置
    xr = x - d0 * (dire) # 更新天牛右须位置
    step = step*eta # 更新步长
    
#############-迭代-############################################################
line = [0 for i in range(maxitr)]
for t in range(maxitr): # 迭代
    print('第%d百次迭代:'%t)
    for inner in range(100):
        update()
    print('适应度值：', problem.reso(xbest))
    line[t] = problem.reso(xbest)
    #print(step)
print(xbest)

print('求解时间：', time.process_time() - t0)

print(problem.showT(xbest))

x = [i for i in range(maxitr)]
y = line

print(x)
print(y)
# 调用绘制线性图函数plot()
plt.plot(x, y)
# 调用show方法显式
plt.show()