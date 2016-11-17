# -*- coding:utf-8 -*-
# python2.7
# 距离计算公式

from math import sqrt

def euclidean(p,q):
    sumSq = 0.0
    # 求差的平方和
    for i in range(len(p)):
        sumSq += (p[i]-q[i])**2
    # 开方
    return (sumSq**0.5)

def pearson(x, y):
    n = len(q)
    vals = range(n)

    # 求 ∑X 和 ∑Y
    sum1 = sum([float(x[i]) for i in vals])
    sum2 = sum([float(y[i]) for i in vals])

    # 求平方和，即求 ∑X^2 和 ∑Y^2
    sum1Sq = sum([x[i]**2 for i in vals])
    sum2Sq = sum([y[i]**2 for i in vals])

    # 求乘积之和，即求 ∑XY
    pSum = sum([x[i] * y[i] for i in vals])

    # 计算皮尔逊相关度
    # num 为上底 , den 为下底
    num = pSum - (sum1*sum2/n)
    den = sqrt((sum1Sq-(sum1**2)/n) * (sum2Sq-(sum2**2)/n))
    if den == 0: return 0

    return num/den

if __name__ == '__main__':
    p = (1,2,3)
    q = (5,5,6)
    print pearson(p,q)