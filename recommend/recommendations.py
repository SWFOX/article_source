# -*- coding:utf-8 -*-
# python 2.7
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

critics={
'小红': 
{'你的名字': 4.5, '最终幻想15：王者之剑': 2.5, '我的少女时代': 3.5, '美人鱼': 3.5, '火星救援': 2.5, '千与千寻': 4.0},
'小倩': 
{'你的名字': 4.0, '最终幻想15：王者之剑': 1.5, '我的少女时代': 3.5, '美人鱼': 5.0, '火星救援': 2.5, '千与千寻': 3.5}, 
'小铭': 
{'你的名字': 3.5, '最终幻想15：王者之剑': 3.0, '美人鱼': 1.5, '千与千寻': 4.0},
'红毛': 
{'最终幻想15：王者之剑': 3.5, '我的少女时代': 1.0, '千与千寻': 4.5, '美人鱼': 2.0,  '火星救援': 3.5},
'爆炸头': 
{'你的名字': 3.0, '最终幻想15：王者之剑': 4.0,  '我的少女时代': 2.0, '美人鱼': 2.5, '千与千寻': 3.0, '火星救援': 5.0}, 
'团长': 
{'你的名字': 5.0, '最终幻想15：王者之剑': 4.0, '千与千寻': 4.0, '美人鱼': 1.0, '火星救援': 1.5},
'敏杰': 
{'最终幻想15：王者之剑':2.5,'火星救援':4.0,'美人鱼':1.0}}

from math import sqrt

# 欧几里得评价距离
def sim_distance(prefs, persion1, persion2):
    # 只有两人都评价的电影才有对比的价值
    # shared_items为两者都评价的电影列表
    shared_items = {}
    for item in prefs[persion1]:
        if item in prefs[persion2]:
            shared_items[item] = 1

    # 如果两人没有共同之处，返回0
    if len(shared_items) == 0:
        return 0

    # 计算所有差值的平方和
    sum_of_squares = 0
    for item in prefs[persion1]:
        if item in prefs[persion2]:
            sum_of_squares += pow(prefs[persion1][item]-prefs[persion2][item], 2)

    # 根据公式，sqrt(sum_of_squares) 越大，表示两人差别越大
    # 通过下面处理，把返回范围限制在 0 ~ 1，并且 1 表示两人有相同兴趣
    return 1/(1+sqrt(sum_of_squares))

# 皮尔逊相关度
def sim_pearson(prefs, persion1, persion2):
    # 只有两人都评价的电影才有对比的价值
    # shared_items为两者都评价的电影列表
    shared_items = {}
    for item in prefs[persion1]:
        if item in prefs[persion2]:
            shared_items[item] = 1

    # 如果两人没有共同之处，返回0
    n = len(shared_items)
    if n == 0 : return 0

    # 对所有偏好求和，即求 ∑X 和 ∑Y
    sum1 = sum([prefs[persion1][item] for item in shared_items])
    sum2 = sum([prefs[persion2][item] for item in shared_items])

    # 求平方和，即求 (∑X)^2 和 (∑Y)^2
    sum1Sq = sum([pow(prefs[persion1][item], 2) for item in shared_items])
    sum2Sq = sum([pow(prefs[persion2][item], 2) for item in shared_items])

    # 求乘积之和，即求 ∑XY
    pSum = sum([prefs[persion1][item] * prefs[persion2][item] for item in shared_items])

    # 计算皮尔逊相关度
    # num 为上底 , den 为下底
    num = pSum - (sum1*sum2/n)
    den = sqrt((sum1Sq-pow(sum1,2)/n) * (sum2Sq-pow(sum2,2)/n))
    if den == 0: return 0

    return num/den

# 求与 person 相似度最高的 n 个人
def topMatches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other)
                for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]

# 利用他人评价值的加权平均，为某人提供建议
def getRecommendations(prefs, person, similarity=sim_pearson):
    totals={}
    simSums={}
    # 遍历每个人
    for other in prefs:
        # 不要和自己比较
        if other==person: continue
        # 计算相似度，相似度看作权重
        sim=similarity(prefs,person,other)

        # 忽略相似度为零或小于零的情况
        if sim<=0: continue
        for item in prefs[other]:
            # 只对自己还没看过的影片进行评价
            if item not in prefs[person] or prefs[person][item]==0:
                # (评分 * 相似度)之和
                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim
                # 相似度之和，也就是权重之和
                simSums.setdefault(item,0)
                simSums[item]+=sim

    # 建立归一化列表，分值除于权重之和
    rankings=[(total/simSums[item],item) for item,total in totals.items()]

    # 返回经过排序的列表
    rankings.sort()
    rankings.reverse()
    return rankings

# 将物品与人调换
# 调换结果如{'你的名字':{'小红':4.5,'小倩':4.0, '小明':3.5}}
def transformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            
            result[item][person] = prefs[person][item]

    return result


# 为每个 item 构造一个 topMatches 字典列表
# 返回结果为{'item1':[(相近度1, 相近物品1),(相近度2, 相近物品1)...],'item2':...}
def calculateSimilarItems(prefs,n=10):
    result = {}
    itemPrefs = transformPrefs(prefs)
    # c用来展示处理了多少条数据
    c = 0
    allItems = len(itemPrefs)
    for item in itemPrefs:
        c+=1
        if c%100==0: print '%d / %d' % (c, allItems)
        scores = topMatches(itemPrefs, item, n=n, similarity=sim_pearson)
        result[item] = scores
    return result

# 获取推荐列表
def getRecommendedItems(prefs, itemMatch, user):
    userRatings=prefs[user]
    scores={}
    totalSim={}
    # 遍历每个用户的电影评分
    for item, rating in userRatings.items():
        # 遍历每个电影的相似列表
        for (similarity, item2) in itemMatch[item]:

            # 如果用户已对物品评价则忽略
            if item2 in userRatings: continue

            # (评分 * 相似度)之和
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating

            # 全部相似度之和
            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity

    rankings = [(score/(totalSim[item]+0.0001), item) for item, score in scores.items()]

    rankings.sort()
    rankings.reverse()
    return rankings

# 加载数据，返回 critics 格式的字典
def loadMovies(path = './data'):
    movies_file = path + '/movies.csv'
    ratings_file = path + '/ratings.csv'

    movies = {}
    c = 0
    with open(movies_file) as file:
        for line in file:
            if c == 0: 
                c += 1
                continue

            line = line.split(',')
            movie_id, movie_title =line[0],line[1]
            movies[movie_id] = movie_title

            if c % 500 == 0: print '%s finished %d' % (movies_file, c)
            c += 1

    prefs = {}
    c = 0
    with open(ratings_file) as file:
        for line in file:
            if c == 0: 
                c += 1
                continue

            line = line.split(',')
            user_id, movie_id, rating = line[0], line[1], float(line[2])
            prefs.setdefault(user_id, {})
            prefs[user_id][movies[movie_id]] = rating

            if c % 500 == 0:
                print '%s finished %d' % (ratings_file, c)
            c += 1
    return prefs

if __name__ == '__main__':
    print '小红和小倩欧几里得距离为：%s' % sim_distance(critics, '小红', '小倩')

    print '小红和小倩皮尔逊相关度为：%s' % sim_pearson(critics, '小红', '小倩')

    print '与敏杰最兴趣最相似的人 : '
    for score,name in topMatches(critics, '敏杰'):
        print score, name

    print '为\'敏杰\'推荐的电影：'
    for score, movie in getRecommendations(critics, '敏杰'):
        print score, movie

    movies = transformPrefs(critics)
    print '与\'你的名字\'最兴趣最相似的电影 : '
    for score,movie in topMatches(movies, '你的名字'):
        print score, movie

    itemsim = calculateSimilarItems(critics)
    print '为\'敏杰\'推荐的电影 : '
    for score, movie in getRecommendedItems(critics, itemsim, '敏杰'):
        print score, movie