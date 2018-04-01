# -*- coding:utf-8 -*-
from math import sqrt
# 嵌套字典表示偏好
critics = {'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
                         'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
                         'The Night Listener': 3.0},
           'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
                            'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 3.5},
           'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
                                'Superman Returns': 3.5, 'The Night Listener': 4.0},
           'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                            'The Night Listener': 4.5, 'Superman Returns': 4.0,
                            'You, Me and Dupree': 2.5},
           'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                            'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 2.0},
           'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                             'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
           'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0, 'Superman Returns': 4.0}}

#欧几里德距离计算相似度
def euclideanDistanceScore(critics, person1, person2):
    si = {}
    #搜集两人共同评价过的电影
    for item in critics[person1]:
        if item in critics[person2]:
            si[item] = 1

    if len(si) == 0:
        return 0

    #计算两人的欧几里德距离,和书上的例子相比，修改了item的索引方式，直接利用了已经获得的共同评价过的电影的字典
    distance = sqrt(sum(pow(critics[person1][item] - critics[person2][item], 2) for item in si))
    sim = 1/(1+distance)
    return sim

#皮尔逊相关度评价
def pearsonCorrelationScore(critics, person1, person2):
    si = {}
    for item in critics[person1]:
        if item in critics[person2]:
            si[item] = 1

    n = len(si)
    #书上是返回1，但是1不就是正相关了吗？所以我选择返回0
    if n == 0:
        return 0

    #书上没有说明皮尔逊系数的数学表达，我按照数学表达进行计算
    #计算两者的协方差
    cov = sum(critics[person1][item] * critics[person2][item] for item in si)\
          - (sum(critics[person1][item] for item in si) * sum(critics[person2][item] for item in si) / n)
    #计算两者的方差
    variance1 = sqrt(sum(pow(critics[person1][item], 2) for item in si)\
                     - pow(sum(critics[person1][item] for item in si), 2) / n)
    variance2 = sqrt(sum(pow(critics[person2][item], 2) for item in si)\
                     - pow(sum(critics[person2][item] for item in si), 2) / n)
    variance = variance1 * variance2
    if variance == 0:
        return 0

    #皮尔逊相关度 = 两者协方差 / 两者方差的积
    pearson = cov / variance
    return pearson

#基于固定数目的邻居
def topMatches(critics, person, n, similarity):
    #从字典中计算每一个与指定目标的相似度，并存入列表中。
    #n为指定相似度的前n个人，similarity是选择的相似度评价准则
    scores = [(similarity(critics, person, other), other) for other in critics if other != person]

    scores.sort()
    scores.reverse()
    return scores[:n]

#基于相似度门槛的邻居
def thresholdMatches(critics, person, threshold, similarity):
    #threshold是设定的相关度门限
    #因为下面需要索引相似度值，所以将()改为内嵌的列表
    scores = [[similarity(critics, person, other), other] for other in critics if other != person]

    scores.sort()
    scores.reverse()

    thresholdScores = []
    for i in range(len(scores)):
        if scores[i][0] >= threshold:
            thresholdScores.append(scores[i])

    return thresholdScores

#推荐物品
def getRecommendations(critics, person, similarity):
    totals = {}
    simSum = {}

    for other in critics:
        if other != person:
            sim = similarity(critics, person, other)

        #忽略评价值为0或者小于零的情况
        if sim <= 0:
            continue

        for item in critics[other]:

            #只选择指定目标未看过的电影
            if item not in critics[person] or critics[person][item] == 0:
                totals.setdefault(item, 0)
                #计算加权评价值之和，加权评价值 = 评价值*相似度
                totals[item] += critics[other][item] * sim

                #计算相似度之和
                simSum.setdefault(item, 0)
                simSum[item] += sim

    #建立归一化的列表
    rankings = [(total / simSum[item], item) for item, total in totals.items()]

    rankings.sort()
    rankings.reverse()
    return rankings

def transformPrefs(critics):
    result = {}
    #统计有多少个物品
    for person in critics:
        for item in critics[person]:
            result.setdefault(item, {})
            #将物品和人员对调
            result[item][person] = critics[person][item]
    return result

#用来加载下载的数据
def loadMoviesLens(path = './moviesdata'):

    #获取影片的标题
    movies = {}
    #Python2 和 Python3差别很大，书上的原程序读文件显示错误，可能是文件中含特殊的中文或者无法识别的文字，必须改变编码形式忽略错误编码
    for line in open(path + '/u.item', 'r', encoding='gb18030', errors='ignore'):
        (id, title) = line.split('|')[0:2]
        movies[id] = title

    #加载数据
    prefs = {}
    for line in open(path + '/u.data'):
        (user, movieid, rating, ts) = line.split('\t')
        prefs.setdefault(user, {})
        prefs[user][movies[movieid]] = float(rating)
    return prefs

prefs = loadMoviesLens()
print(prefs['87'])
print(getRecommendations(prefs, '87', pearsonCorrelationScore)[0:30])
# print(euclideanDistanceScore(critics, 'Lisa Rose', 'Gene Seymour'))
#
# print(pearsonCorrelationScore(critics, 'Lisa Rose', 'Gene Seymour'))
#
# print(topMatches(critics, 'Lisa Rose', 5, pearsonCorrelationScore))
#
# print(thresholdMatches(critics, 'Lisa Rose', 0.5, pearsonCorrelationScore))
#
# print(getRecommendations(critics, 'Toby', pearsonCorrelationScore))
#
# print(transformPrefs(critics))
#
# moives = transformPrefs(critics)
# print(topMatches(moives, 'You, Me and Dupree', 5, pearsonCorrelationScore))
#
# print(getRecommendations(moives, 'Superman Returns', pearsonCorrelationScore))