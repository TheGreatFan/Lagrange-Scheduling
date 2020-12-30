# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 13:16:58 2020

@author: Administrator
"""

# https://blog.csdn.net/wp_csdn/article/details/54577567
# https://zhuanlan.zhihu.com/p/100920122   比较详细
# https://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&dbname=CJFD2002&filename=XTLL200211006&v=kcdeKhm3qtgLUeBhnl4E%25mmd2BDdtB%25mmd2BgdLB1Hh5b3Q7qeIax8%25mmd2FcJXWz%25mmd2BiGcZYcQMiQsWx 知网

# 需要用的包
import numpy as np
import random # random 0，1 之间 uniform 自定义区间 random.random()
#import time

# 外部子程序
import problem_2 as problem # 导入 problem  problem_1 简单问题 problem_2 调度问题 

# 基本函数
# 初始中心点 （坐标原点）
def VacantC(n):
    return np.array([0 for i in range(n)])

# 生成一个随机方向(维度为 n 的 numpy 数组)
def Rand(n):
    return np.array([(-1 + 2*random.random()) for i in range(n)])

# 求两个点的距离 （两个 numpy 数组差的范数）
def Distan(I, J):
    return np.linalg.norm(I - J)

def Step():
    return random.random() * 20


# 四种主要行为
# Prey 觅食
def Prey(Xi):
    Yi = problem.reso(Xi)
    tn = 0
    while tn < maxt: # 最多尝试 maxt 次
        tn += 1
        Xj = Xi + S * Rand(4) # 视野范围内随机移动一步  S or V ?
        #Xj = Xi + V * Rand(4) # 视野范围内随机移动一步
        Yj = problem.reso(Xj)
        if Yj < Yi: # 如果视野内的新点更优
            #Xnext = Xi + (Xj - Xi)/np.linalg.norm(Xj - Xi) * Step()
            Xnext = Xi + (Xj - Xi)/np.linalg.norm(Xj - Xi) * S * random.random()
            return(Xnext)
    else:
        return Move(Xi) # 随机行为

# Swarm 群聚，聚群时会遵守两条规则：一是尽量向邻近伙伴的中心移动，二是避免过分拥挤。
def Swarm(Xi):
    Yi = problem.reso(Xi)
    nf = 1 # 统计有多少个 粒子 在 Vision 范围之内
    Xct = VacantC(4) # 群体的中心位置
    for n in range(psize): # 遍历一遍所有粒子
        if Distan(X[n], Xi) <= V:
            nf += 1 # 计数 + 1
            Xct = Xct + X[n] # 中心点坐标积累 加上
    Xc = Xct/nf # 中心点
    Yc = problem.reso(Xc)
    if Yc/nf > delta * Yi:
        #Xnext = Xi + (Xc - Xi)/np.linalg.norm(Xc - Xi) * Step()
        Xnext = Xi + (Xc - Xi)/np.linalg.norm(Xc - Xi) * S * random.random()    
        return Xnext
    else:
        return Prey(Xi)

# Follow 追尾
def Follow(Xi):
    Yi = problem.reso(Xi)
    #print("Yi", Yi)
    Xj = Xi # 最优点，暂定
    #print("Xj", Xj)
    Yj = Yi # 范围内最优值，如果有更好的就更新
    #print("Yj", Yj)
    nf = 1 # 统计有多少个 粒子 在 Vision 范围之内
    #print("开始遍历")
    for n in range(psize): # 遍历一遍所有粒子
        #print("X", X)
        #print("X[n]", X[n])
        #print("距离", Distan(X[n], Xi))
        if Distan(X[n], Xi) <= V: # 如果在视野范围内
            #print("发现了一个")
            nf += 1 # 计数 + 1
            #print("X[n]", X[n])
            Yn = problem.reso(X[n])
            #print("Yn", Yn)
            if Yn < Yj:
                Xj = X[n] # 更新最优
                Yj = Yn
    if Yj/nf > delta * Yi:
        Xnext = Xj + (Xj - Xi)/np.linalg.norm(Xj - Xi) * S * random.random()
        #Xnext = Xj + (Xj - Xi)/np.linalg.norm(Xj - Xi) * Step()
        return Xnext
    else:
        return Prey(Xi)

# Move 随机
def Move(Xi):
    return Xi + S * Rand(4)



# 算法流程
# 1 初始化设置
maxitr = 32 # 最大迭代次数 max iteration generation
psize = 20 # 种群数量  population size
#V = 30 # Visual 视野
#S = 50 # Step 步长
delta = 0.3 * psize # 拥挤度因子 在求极大值问题中，δ=1/(αnmax),α∈(0,1]δ=1/(αnmax),α∈(0,1]；在求极小值问题中，δ=αnmax,α∈(0,1]δ=αnmax,α∈(0,1]。其中α为极值接近水平， nmax为期望在该邻域内聚集的最大人工鱼数目。
maxt = 5 # 觅食行为最多尝试次数
BestX = VacantC(4) # 初始最优点，选默认点
BestY = problem.reso(BestX)  # 最优适应度值（暂定）


# 2 计算初始鱼群各个体的适应值，取最优人工鱼状态及其值赋予给公告牌
X = problem.criarRand(psize) # 生成数量为 psize 的初始种群
#X[1] = [109.76040464, 420.46471964, 156.15767451, 396.00807855]
print(X)

Adapt = [] # 适应度值的集合
for i in range(psize): # 都求解一遍
    Adapt.append(problem.reso(X[i])) # 结果保存到 adapt[] 中

Adapt = np.array(Adapt) # Adapt[n]： X[n]的适应度值
# print('初始适应度值：\n', Adapt)

Rank = Adapt.argsort()
# print('适应度值 adapt 顺序索引:')
# print(Rank)

print("初始最优点", X[Rank[0]]) # 初始最优点
print("初始最优适应度值", Adapt[Rank[0]]) # 初始最优适应度值



# 4 执行人工鱼的行为，更新自己，生成新鱼群
def update():
    global BestX
    global BestY
    for i in range(psize): # 3 对每个个体进行评价，对其要执行的行为进行选择，包括觅食、聚群、追尾和随机行为
        tempX = X[i]
        tempY = Adapt[i]
        Xs = Swarm(X[i]) # 尝试 聚群 
        Ys = problem.reso(Xs) # 求适应度
        if Ys < tempY:
            tempX = Xs
            tempY = Ys
        Xf = Follow(X[i]) # 尝试 追尾
        Yf = problem.reso(Xf) # 求适应度
        if Yf < tempY:
            tempX = Xf
            tempY = Yf
        Xp = Prey(X[i]) # 尝试 觅食
        Yp = problem.reso(Xp) # 求适应度
        if Yp < tempY:
            tempX = Xp
            tempY = Yp
        X[i] = tempX #
        Adapt[i] = tempY
        if tempY < BestY: # 5 评价所有个体。若某个体优于公告牌，则将公告牌更新为该个体
            BestX = tempX
            BestY = tempY

# 6 当公告牌上最优解达到满意误差界内或者达到迭代次数上限时算法结束，否则转步骤 3
ite = 0 # 迭代次数
while ite < maxitr:
    # S = 40 * (1 - ite/maxitr) + 2 # 逐渐缩小的步长
    # V = 0.6 * S
    V = 20 * (1 - ite/maxitr) + 2 # 逐渐缩小的步长
    S = V
    print("第%d次遍历" % ite)
    update()
    Adapt.sort()
    print(Adapt[0])
    ite += 1

print(X)
Adapt.sort()
print(Adapt)
print("最优 X:", BestX)
print("最优 Y:", BestY)