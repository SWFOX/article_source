# -*- coding:utf-8 -*-
# python2.7

import sys

from random import choice,random,randint
from copy import deepcopy
from math import log

# 用来对函数进行封装
class fwrapper:
    def __init__(self, function, childcount, name):
        self.function = function
        self.childcount = childcount
        self.name = name

# 函数节点，内节点
class node:
    def __init__(self, fwrapper, children):
        self.function = fwrapper.function
        self.children = children
        self.name = fwrapper.name

    def evaluate(self, input):
        results = [n.evaluate(input) for n in self.children]
        return self.function(results)

    def display(self, indent=0):
        print ((" "*indent) + self.name)
        for c in self.children:
            c.display(indent+1)

# 变量节点，叶子节点，idx表示第几个参数,input表示输入的数据
class paramnode:
    def __init__(self, idx):
        self.idx = idx

    def evaluate(self, input):
        return input[self.idx]

    def display(self,indent=0):
        print ('%sp%d' % (' '*indent, self.idx))

# 常量节点,返回常量，叶子节点
class constnode:
    def __init__(self, v):
        self.v = v

    def evaluate(self, input):
        return self.v

    def display(self, indent=0):
        print ('%s%d' % (' '*indent, self.v))

addw = fwrapper(lambda l : l[0] + l[1], 2, 'add')
subw = fwrapper(lambda l : l[0] - l[1], 2, 'sub')
mulw = fwrapper(lambda l : l[0] * l[1], 2, 'mul')

def iffunc(l):
    if l[0]>0: 
        return l[1]
    else:
        return l[2]
ifw = fwrapper(iffunc, 3, 'if')

def isgreater(l):
    if l[0] > l[1]:
        return 1
    else:
        return 0
gtw = fwrapper(isgreater, 2, 'isgreater')

flist = [addw, subw, mulw, ifw, gtw]

def exampletree():
    return node(ifw,[
                    node(gtw, [paramnode(0), constnode(3)]),
                    node(addw, [paramnode(1), constnode(5)]),
                    node(subw, [paramnode(1), constnode(2)]),
                    ]
        )

# 随机构建程序，pc 表示变量个数
# maxdepth:树的最大深度，fpr:生成函数节点的概率，ppr:生成变量节点的概率
def makerandomtree(pc, maxdepth=4, fpr=0.6, ppr=0.6):
    if random()<fpr and maxdepth>0:
        f = choice(flist)
        children = [makerandomtree(pc, maxdepth-1, fpr, ppr)
                                 for i in range(f.childcount)]
        return node(f, children)
    elif random()<ppr:
        return paramnode(randint(0, pc-1))
    else:
        return constnode(randint(0, 10))

# 二元二次方程的公式
def hiddenfunction(x, y):
    return x**2+5*y+3*x+5

# 返回数据集列表
def buildhiddenset():
    rows = []
    for i in range(200):
        x = randint(0, 40)
        y = randint(0, 40)
        rows.append([x, y, hiddenfunction(x, y)])
    return rows

# 计算程序与正确结果的差距,datalists为上面的函数返回值
def scorefunction(tree, datalists):
    dif = 0
    for data in datalists:
        v = tree.evaluate([data[0], data[1]])
        dif += abs(v-data[2])
    return dif

# 突变变异操作，pc为变量个数
def mutate(tree, pc, probchange=0.3):
    if random()<probchange:
        return makerandomtree(pc)
    else:
        result = deepcopy(tree)
        if isinstance(tree, node):
            result.children = [mutate(c, pc, probchange) for c in tree.children]
        return result

# 交叉变异，top=1表示到达第二层才考虑交换
def crossover(t1, t2, probswap=0.7, top=1):
    if random() < probswap and top<1:
        return deepcopy(t2)
    else:
        result = deepcopy(t1)
        if isinstance(t1, node) and isinstance(t2, node):
            result.children = [crossover(c, choice(t2.children), probswap, top-1) 
                                            for c in t1.children]
        return result

# 返回一个可以进行优劣排序的函数
def getrankfunction(dataset):
    # 此函数输入种群，返回排序后的列表，优秀在前
    def rankfunction(population):
        scores=[(scorefunction(tree,dataset), tree) for tree in population]
        scores.sort()
        return scores
    return rankfunction

# pc为变量个数，popsize为种群大小，rankfunction为排序函数
# maxgen为迭代代数，mutationrate 为突变概率，crossrate为交叉概率
# probexp 的值越小，得到的随机数越小
# probnew 表示产生一个全新的程序的概率
def evolve(pc, popsize, rankfunction, maxgen=500,
            mutationrate=0.2, crossrate=0.5, probexp=0.7, probnew=0.1):

    # 返回一个随机数
    def selectindex():
        return int(log(random())/log(probexp))

    # 初始种群
    population = [makerandomtree(pc) for i in range(popsize)]

    for i in range(maxgen):
        scores=rankfunction(population)
        print (scores[0][0])

        # 如果产生了最优解，就退出
        if scores[0][0] == 0:break

        # 保留最优两个
        newpop = [scores[0][1], scores[1][1]]
        # 继续产生新的种群
        while  len(newpop) < popsize:
            if random() > probnew:
                newpop.append(mutate(
                        crossover(scores[selectindex()][1],
                                scores[selectindex()][1],
                                probswap=crossrate
                            ),
                        pc,
                        probchange=mutationrate
                    ))
            else:
                # 加入新的随机程序
                newpop.append(makerandomtree(pc))
        population = newpop
    scores[0][1].display()
    return scores[0][1]

if __name__ == '__main__':
    pass