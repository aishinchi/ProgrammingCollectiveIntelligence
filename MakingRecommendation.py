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
def EuclideanDistanceScore(critics, person1, person2):
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
def PearsonCorrelationScore(critics, person1, person2):
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


print(EuclideanDistanceScore(critics, 'Lisa Rose', 'Gene Seymour'))

print(PearsonCorrelationScore(critics, 'Lisa Rose', 'Gene Seymour'))
