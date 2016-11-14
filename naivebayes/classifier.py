# -*- coding:utf-8 -*-
# python 2.7
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
import json

from sqlite3 import dbapi2 as sqlite

# 分词,返回结果:{'词语1':1,'词语2':1}
def getwords(text):
    url = "http://www.xunsearch.com/scws/api.php"

    payload = "data=%s&respond=json&ignore=yes" % text
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        }

    wordsList = []
    response = requests.request("POST", url, data=payload, headers=headers)
    text = json.loads(response.text)

    for wordmsg in text['words']:
        wordsList.append((wordmsg['word'].encode('utf-8'),1))

    # 返回不重复单词字典
    return dict(wordsList)

# 假设只有 good 和 bad 两种分类
class classifier:
    def __init__(self,getwords,dbname='classifier'):
        self.getwords = getwords
        self.int_db(dbname)

    # 如果表不存在就构建两个表
    # 其中`fc`表表示在某分类(cat)下，某个词语(word)的数量(count)
    # `cc` 表示某个分类 (cat) 的数量
    def int_db(self, dbname):
        self.conn = sqlite.connect(dbname)
        self.conn.execute('create table if not exists `fc`(`word`,`cat`,`count`)')
        self.conn.execute('create table if not exists `cc`(`cat`,`count`)')

    # 增加某个单词在某种分类的数量
    def inc_word(self, word, cat):
        count = self.word_count(word, cat)
        if count == 0:
            self.conn.execute('insert into `fc` values ("%s","%s",1)' % (word,cat))
        else:
            self.conn.execute('update `fc` set `count`=%d where `word` = "%s" and `cat` = "%s"' % (count+1, word, cat)) 


    # 增加某种分类的数量
    def inc_cat_count(self,cat):
        count=self.cat_count(cat)
        if count==0:
            self.conn.execute('insert into `cc` values ("%s",1)' % (cat))
        else:
            self.conn.execute('update `cc` set `count`=%d where `cat`="%s"' % (count+1,cat))

    # 返回某个单词在某种分类下的出现的次数
    def word_count(self, word, cat):
        res=self.conn.execute('select `count` from `fc` where `word`="%s" and `cat`="%s"'%(word,cat)).fetchone()
        if res==None: 
            return 0
        else: 
            return float(res[0])

    # 增加某种分类的出现次数
    def cat_count(self, cat):
        res=self.conn.execute('select `count` from `cc` where `cat`="%s"'%(cat)).fetchone()
        if res==None:
            return 0
        else:
            return float(res[0])

    # 返回训练过的短信的数量，也就是 good 和 bad 的总数
    def total_count(self):
        res=self.conn.execute('select sum(`count`) from `cc`').fetchone();
        if res==None: return 0
        return res[0]

    # 返回分类列表,这里返回['bad','good']
    def cat_list(self):
        cur = self.conn.execute('select `cat` from `cc`')
        return [d[0] for d in cur]

    def train(self, text, cat):
        wordsList = self.getwords(text)
        for word in wordsList:
            # 针对该分类为每个特征增加计数值
            self.inc_word(word, cat)
        # 增加 cat 特征的计数值
        self.inc_cat_count(cat)
        self.conn.commit()

    # 求在某种分类下出现某个单词的概率，也就是P(word|cat)
    def word_prob(self, word, cat):
        if self.cat_count(cat) == 0:return 0
        return self.word_count(word, cat)/self.cat_count(cat)

    # 为了防止数据量少的时候出现极端情况，增加一个阻尼系数
    # 相当于增加一个单词的数据与原数据加权平均
    # weight 表示次数，ap 表示出现概率
    def weighted_prob(self, word, cat, word_prob, weight=1.0, ap=0.5):
        # 计算当前的概率值
        basic_prob = word_prob(word, cat)
        # 统计词语在所有分类中出现的次数
        totals = sum([self.word_count(word, cat) for cat in self.cat_list()])
        # 计算加权平均
        bp = ((weight * ap) + (totals*basic_prob))/(weight+totals)
        return bp

class naivebayes(classifier):
    def __init__(self,getwords):
        classifier.__init__(self,getwords)
        self.thresholds={}

    # 设置阈值
    def setthreshold(self,cat,t):
        self.thresholds[cat]=t
    
    # 获取阈值，如果没设置，默认为 1.0
    def getthreshold(self,cat):
        if cat not in self.thresholds: return 1.0
        return self.thresholds[cat]

    # 计算文档在某个分类的概率，也就是计算P(B|A)
    # 因为我们假设各个词语是独立的，所以总概率等于各个词语概率之和
    def text_prob(self, text, cat):
        words = self.getwords(text)
        p = 1
        for word in words:
            p *= self.weighted_prob(word, cat, self.word_prob)
        return p

    # 计算 P(B|A)*P(A)
    def prob(self, text, cat):
        cat_prob = self.cat_count(cat)/self.total_count()
        text_prob = self.text_prob(text, cat)
        return text_prob*cat_prob

    # 进行分类
    def classify(self, text, default='unknown'):
        probs = {}
        # 寻找概率最大的分类
        max_prob = 0.0
        for cat in self.cat_list():
            probs[cat] = self.prob(text, cat)
            if probs[cat] > max_prob:
                max_prob = probs[cat]
                best = cat

        for cat in probs:
            if cat == best:continue
            # 其他分类乘 best 分类的阈值大于 best 的概率，就返回 default
            if probs[cat]*self.getthreshold(best)>probs[best]:
                return default
            return best

# def sampletrain(cl):
#     cl.train('Nobody owns the water.','good')
#     cl.train('the quick rabbit jumps fences','good')
#     cl.train('buy pharmaceuticals now','bad')
#     cl.train('make quick money at the online casino','bad')
#     cl.train('the quick brown fox jumps','good')

# if __name__ == '__main__':
#     cl = naivebayes(getwords)
#     sampletrain(cl)
#     print cl.weighted_prob('money', 'good', cl.word_prob)
#     sampletrain(cl)
#     print cl.weighted_prob('money', 'good', cl.word_prob)