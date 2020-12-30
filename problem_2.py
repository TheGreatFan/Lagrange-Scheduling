# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 14:32:32 2020

@author: Administrator
"""

import numpy as np
import copy # 直接 = 是地址相等，修改一个会导致源地址也被修改，因此用 deepcopy 复制出一个

# 信息
# 加工类型及加工时间
P = [[[0, 40], [1, 30], [3, 45]], [[0, 30], [1, 34], [3, 46]], [[0, 30], [1, 30], [3, 49]], [[0, 34], [1, 35], [3, 50]], [[0, 37], [1, 32], [2, 33], [1, 31], [3, 48]], [[0, 39], [1, 34], [3, 44]], [[0, 39], [1, 36], [2, 37], [3, 45]], [[0, 33], [2, 30], [1, 40], [3, 42]], [[0, 31], [1, 33], [3, 50]], [[0, 35], [1, 40], [3, 48]], [[0, 30], [1, 40], [3, 43]], [[0, 32], [1, 32], [3, 40]], [[0, 33], [1, 30], [3, 41]], [[0, 40], [1, 33], [3, 45]], [[0, 35], [2, 40], [1, 36], [3, 44]], [[0, 36], [1, 39], [3, 41]], [[0, 31], [1, 40], [2, 40], [1, 35], [3, 47]], [[0, 33], [1, 33], [2, 32], [3, 42]], [[0, 36], [1, 40], [3, 49]], [[0, 38], [1, 40], [3, 50]]]
# 连铸计划炉次序号
CP = [[[0, 1, 2, 3, 4], [10, 11, 12, 13, 14]], [[5, 6, 7, 8, 9], [15, 16, 17, 18, 19]]] # cast plan
# 计划浇铸时间
DT = np.array([110, 420, 150, 240]) # due time of casting 要优化的变量，开始浇铸时间 # 一维向量，对应四个浇次

MQ = [2, 3, 1, 2] # machine quantity - 各种工艺类型的设备数

ut = 15 # 运输时间，暂且统一设置为 15，可用二维列表
gap = 10 # 浇次前换结晶器时间
q = len(P) # 炉次个数
N = len(DT) # 浇次个数

c1 = 1 # 总驻留时间惩罚系数
c2 = 10 # 总提前开浇时间惩罚系数
c3 = 10 # 总滞后开浇时间惩罚系数
c4 = 1000 # 开始时间出现负数惩罚系数
c5 = 1000 # 浇次时间出现重叠的惩罚系数

#DT = np.array([140, 380, 140, 380]) # due time of casting 要优化的变量，开始浇铸时间 # 一维向量，对应四个浇次

def defalt():
    return DT

devia = 100 # 生成初始解的最大偏差值

def criarRand(n): # 完全随机产生初始解
    X = np.random.uniform(-100,100,(n,len(DT))) # 生成随机波动值
    for i in range(len(X)): # 遍历每一个初始值
        X[i] = X[i] + DT
    X[0] = DT
    return X

# def criarUnif(n): # 让初始解均匀分布在定义域中
#     s = n**(1/len(DT))
#     while n <= len()
#     X = np.zeros((n, len(DT))) # 生成随机波动值
#     for i in range(s):
        
#         for j in range(s):
#             for k in range(s):

#print(criarUnif(20))

CL = [] # 浇次的长度
for k in range(len(CP)): # 遍历连铸机
    for n in range(len(CP[k])): # 遍历浇次
        CL.append(sum(P[i][-1][1] for i in CP[k][n]) + gap) # 把浇次长度加上
#print('浇次长度（包含后续gap）', CL)

CN = [] # 需要检查和前序浇次时间冲突的浇次
cout = 0
for k in range(len(CP)): # 遍历连铸机
    for n in range(len(CP[k])): # 遍历浇次
        if n != 0:
            CN.append(cout)
            cout += 1
        else:
            cout += 1
#print('需要检查和前序浇次时间冲突的浇次', CN)

S = np.array([len(P[i])-1 for i in range(q)]) # 准备安排的前一阶段
#print('准备安排的前一阶段', S)

def fmc(j, k): # 第 j 阶段序号为 k 的设备总编号是多少
    if k <= MQ[j]-1:
        return k + sum(MQ[n] for n in range(j))
    return -1

def convert(X): # 转换浇次序列的格式，按照姐的时间点确定每一个炉次浇的时间
    CX = [[0 for i in range(len(CP[k]))] for k in range(len(CP))] # 
    c = 0 # count
    for k in range(len(CP)):
        for n in range(len(CP[k])):
            CX[k][n] = X[c]
            c += 1
    return CX

def reso(X): # 通过每一个浇次的开始时间安排其他开工信息，测试前检查是否符合条件，不符合要重新随机生成
#    print(X)
    ##########################-初始系数-###########################################
    MRT = [[10000 for k in range(MQ[j])] for j in range(len(MQ))] # initial machine release time 初始释放时间，设置大一些，明显大于计划完工时间
    #print('初始设备释放时间：', MRT)
    #STP = np.zeros((len(P), 5)) # 阶段开始时间
    STP = np.full((len(P), 5), -100) # 炉次的阶段开始时间，工序不超过5个，先设置一个不可能的数（-100），错了会比较明显 (np.full 填充)
    MCH = np.full((len(P), 5), -1) # 设备选择 machine selection，默认 -1 不可能值
#    print('炉次工序开始时间\n', STP)
#    print('炉次工序选择设备\n', MCH)
    
    NS = np.array([len(P[i])-1 for i in range(q)]) # 准备安排的前一阶段
    RT = np.array([0 for i in range(q)]) # 已安排工序的开始时间
    # 浇次
    CT = convert(X)
    #print('浇次开始时间', CT)
    CRT = copy.deepcopy(CT) # 连铸机的占用时间，暂时计算用
    for k in range(len(CP)): # 遍历 连铸机
        for n in range(len(CP[k])): # 遍历 浇次
            for i in range(len(CP[k][n])): # 遍历浇次中的炉次
                w = CP[k][n][i] # w 为此位置的炉次号
                STP[w][NS[w]] = CRT[k][n] # 浇铸工序开始时间 为 连铸机释放时间 
                RT[w] = STP[w][NS[w]] - ut # 炉次释放时间 为 开始时间 - 运输时间
                MCH[w][NS[w]] = fmc(3, k) # 设备选择 安排上
                CRT[k][n] += P[w][-1][1] # 连铸机释放时间 + 工序时间
                NS[w] -= 1
    #print('连铸时间安排后的炉次释放时间：', RT)
    #print('******************************-第一阶段连铸时间安排完成-******************************')
    while min(NS) != 10: # 检查是否 全部工件 已安排完成（未安排的工序为 -1）
        nr = np.where(RT==np.max(RT))[0][0] # 找出下一个安排的（最晚需要准备就绪的工序）， print(np.where(a==np.max(a))) 可以试试 list 形式的速度
#        print(RT)
#        print('下一安排炉次', nr)
        s = NS[nr] # 阶段
#        print('准备安排的阶段', NS)
#        print('准备安排的阶段', s)
        ty = P[nr][s][0] # 工艺类型
        #print('工艺类型', ty)
        k = MRT[ty].index(max(MRT[ty])) # 该阶段的最晚空闲设备
        #print('安排的设备', k)
        MCH[nr][s] = fmc(ty, k) # 设备安排上 fmc(nt, k)
        #print('安排的设备\n', MCH)
    #    print('设备释放时间', MRT[ty][k])
    #    print('炉次释放时间', RT[nr])
    #    print('炉次工序时间', P[nr][s][1])
        STP[nr][s] = min(MRT[ty][k], RT[nr]) - P[nr][s][1] # 开始时间 = min（设备时间，炉次需要就绪） - 工序时间
    #    print('安排的开始时间：', STP[nr][s])
        RT[nr] = STP[nr][s] - ut # 炉次释放时间（可以安排的前一阶段结束时间） = 炉次开始时间 - 运输时间
        #RT[nr] = max(MRT[ty][k], RT[nr]) + P[nr][s][1] - ut # 炉次本阶段完工时间 为 max(最早空闲设备释放时间 或 炉次释放时间) + 炉次本阶段工时，就绪时间需要加上 运输时间
        MRT[ty][k] = STP[nr][s] # 设备释放时间 与 上表达式前半部分 相等
    #    print('设备释放时间：', MRT)
    #    NS[nr] -= 1 # 更新 待加工阶段
        if s == 0: # 如果已安排了最初阶段
            RT[nr] = -100000 # 预期开始时间赋值为极小，表示工件所有工序已安排完成 # 学习过程中 初始值 可能产生比较大的值，因此这里设为绝对值比较大的负数
            NS[nr] = 10 # 所有阶段安排完，把待安排阶段赋一个 足够大 的值
        else:
            NS[nr] -= 1 # 更新 待加工阶段
    # target 1.驻留时间 2.提前开浇时间 3.滞后开浇时间 4.负时间惩罚 5.浇次时间重叠惩罚
    target = c1*sum((STP[i][S[i]] - STP[i][0]) for i in range(q)) + c2*sum(max(DT[n] - X[n], 0) for n in range(N)) + c3*sum(max(X[n] - DT[n], 0) for n in range(N)) + c4*sum(max(-STP[i][0], 0) for i in range(q)) + c5*sum(max(-(X[n] - X[n-1] - CL[n-1]), 0) for n in CN) # 1.驻留时间 2.提前开浇时间 3.滞后开浇时间 4.负时间惩罚 5.浇次时间重叠惩罚
    return target

def showT(X):
#    print(X)
    ##########################-初始系数-###########################################
    MRT = [[10000 for k in range(MQ[j])] for j in range(len(MQ))] # initial machine release time 初始释放时间，设置大一些，明显大于计划完工时间
    #print('初始设备释放时间：', MRT)
    #STP = np.zeros((len(P), 5)) # 阶段开始时间
    STP = np.full((len(P), 5), -100) # 炉次的阶段开始时间，工序不超过5个，先设置一个不可能的数（-100），错了会比较明显 (np.full 填充)
    MCH = np.full((len(P), 5), -1) # 设备选择 machine selection，默认 -1 不可能值
#    print('炉次工序开始时间\n', STP)
#    print('炉次工序选择设备\n', MCH)
    
    NS = np.array([len(P[i])-1 for i in range(q)]) # 准备安排的前一阶段
    RT = np.array([0 for i in range(q)]) # 已安排工序的开始时间
    # 浇次
    CT = convert(X)
    #print('浇次开始时间', CT)
    CRT = copy.deepcopy(CT) # 连铸机的占用时间，暂时计算用
    for k in range(len(CP)): # 遍历 连铸机
        for n in range(len(CP[k])): # 遍历 浇次
            for i in range(len(CP[k][n])): # 遍历浇次中的炉次
                w = CP[k][n][i] # w 为此位置的炉次号
                STP[w][NS[w]] = CRT[k][n] # 浇铸工序开始时间 为 连铸机释放时间 
                RT[w] = STP[w][NS[w]] - ut # 炉次释放时间 为 开始时间 - 运输时间
                MCH[w][NS[w]] = fmc(3, k) # 设备选择 安排上
                CRT[k][n] += P[w][-1][1] # 连铸机释放时间 + 工序时间
                NS[w] -= 1
    #print('连铸时间安排后的炉次释放时间：', RT)
    #print('******************************-第一阶段连铸时间安排完成-******************************')
    while min(NS) != 10: # 检查是否 全部工件 已安排完成（未安排的工序为 -1）
        nr = np.where(RT==np.max(RT))[0][0] # 找出下一个安排的（最晚需要准备就绪的工序）， print(np.where(a==np.max(a))) 可以试试 list 形式的速度
#        print(RT)
#        print('下一安排炉次', nr)
        s = NS[nr] # 阶段
#        print('准备安排的阶段', NS)
#        print('准备安排的阶段', s)
        ty = P[nr][s][0] # 工艺类型
        #print('工艺类型', ty)
        k = MRT[ty].index(max(MRT[ty])) # 该阶段的最晚空闲设备
        #print('安排的设备', k)
        MCH[nr][s] = fmc(ty, k) # 设备安排上 fmc(nt, k)
        #print('安排的设备\n', MCH)
    #    print('设备释放时间', MRT[ty][k])
    #    print('炉次释放时间', RT[nr])
    #    print('炉次工序时间', P[nr][s][1])
        STP[nr][s] = min(MRT[ty][k], RT[nr]) - P[nr][s][1] # 开始时间 = min（设备时间，炉次需要就绪） - 工序时间
    #    print('安排的开始时间：', STP[nr][s])
        RT[nr] = STP[nr][s] - ut # 炉次释放时间（可以安排的前一阶段结束时间） = 炉次开始时间 - 运输时间
        #RT[nr] = max(MRT[ty][k], RT[nr]) + P[nr][s][1] - ut # 炉次本阶段完工时间 为 max(最早空闲设备释放时间 或 炉次释放时间) + 炉次本阶段工时，就绪时间需要加上 运输时间
        MRT[ty][k] = STP[nr][s] # 设备释放时间 与 上表达式前半部分 相等
    #    print('设备释放时间：', MRT)
    #    NS[nr] -= 1 # 更新 待加工阶段
        if s == 0: # 如果已安排了最初阶段
            RT[nr] = -100000 # 预期开始时间赋值为极小，表示工件所有工序已安排完成 # 学习过程中 初始值 可能产生比较大的值，因此这里设为绝对值比较大的负数
            NS[nr] = 10 # 所有阶段安排完，把待安排阶段赋一个 足够大 的值
        else:
            NS[nr] -= 1 # 更新 待加工阶段
    # target 1.驻留时间 2.提前开浇时间 3.滞后开浇时间 4.负时间惩罚 5.浇次时间重叠惩罚
    #target = c1*sum((STP[i][S[i]] - STP[i][0]) for i in range(q)) + c2*sum(max(DT[n] - X[n], 0) for n in range(N)) + c3*sum(max(X[n] - DT[n], 0) for n in range(N)) + c4*sum(max(-STP[i][0], 0) for i in range(q)) + c5*sum(max(-(X[n] - X[n-1] - CL[n-1]), 0) for n in CN) # 1.驻留时间 2.提前开浇时间 3.滞后开浇时间 4.负时间惩罚 5.浇次时间重叠惩罚
    return STP