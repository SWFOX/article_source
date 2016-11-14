# -*- coding:utf-8 -*-
# python 2.7
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from classifier import naivebayes,getwords

def load_and_train_message(classifier,filename='./message.csv'):
    # n 用于计算处理了多少条数据
    n = 1
    with open(filename) as file:
        for line in  file:
            # 第一行忽略
            if n == 1:
                n += 1 
                continue
            line = line.split(',')
            if int(line[0]) == 1:
                cat = 'good'
            else:
                cat = 'bad'
            classifier.train(line[-1], cat)
            # 每处理 20 条显示一下
            if (n%20) == 0:
                print 'finished %d' % (n)
            n += 1

def test(cl):
    testmessage = [
        ('亲爱的同学，恭喜您通过了笔试环节，现邀请您参加我司面试','good'),
        ('来某里就只剩梦想了吗？你想加入，和大牛们做同事吗？','bad'),
        ('快递到了，请到天桥旁边领取','good'),
        ('一年365天，今天最宜理财','bad'),
        ('程淇铭 您好！欢迎参加在线测评','good'),
        ('欢迎参加xxx宣讲会，与高层领导面对面交流，送精美礼品','bad'),
        ('5元包3G，畅快买买买','bad'),
        ('小铭你好，今天过得怎么样','good'),
        ('今天优惠，快来购买','bad'),
    ]
    for message,expection in testmessage:
        print 'message:%s ; expect:%s ; result:%s' % (message, expection, cl.classify(message))


if __name__ == '__main__':
    classifier = naivebayes(getwords)
    classifier.setthreshold('bad', 3.0)
    # load_and_train_message(classifier)
    # print classifier.cat_count('good')
    # print classifier.cat_count('bad')
    test(classifier)