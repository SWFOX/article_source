# -*- coding:utf-8 -*-
# python2.7
# 井字棋

import gp

from random import random

def printRule():
    print '每步对于关系如下,若走相同相当于输'
    print '第一个玩家为 X，第二个为 O，X先走'
    print '-----------'
    print ' 7 | 8 | 9 '
    print '-----------'
    print ' 4 | 5 | 6 '
    print '-----------'
    print ' 1 | 2 | 3'
    print '-----------'
    print '\n'

# 两个player进行对战，showBroad表示要不要显示棋盘
# 返回0表示0号玩家赢，1表示1号赢，-1表示平局
def startGame(players,showBroad=False):
    broad = [-1] * 10
    for i in range(9):
        # 0、1轮流替换
        player = i%2
        broad[0] = player
        next_step = players[player].evaluate(broad) % 9
        next_step = next_step+1

        if showBroad:
            print 'player%d next_step is %d' % (player, next_step)

        if broad[next_step] != -1:
            if showBroad:drawBroad(broad)
            return 1-player

        broad[next_step] = player
        if showBroad:drawBroad(broad)

        if isWin(broad, player):
            return player
    return -1

def getBroad(broad, index):
    if broad[index] == 0:
        return 'X'
    elif broad[index] == 1:
        return 'O'
    else:
        return ' '

def drawBroad(broad):
    print '-----------'
    print ' '+getBroad(broad, 7)+' | '+getBroad(broad, 8)+' | '+getBroad(broad, 9)
    print '-----------'
    print ' '+getBroad(broad, 4)+' | '+getBroad(broad, 5)+' | '+getBroad(broad, 6)
    print '-----------'
    print ' '+getBroad(broad, 1)+' | '+getBroad(broad, 2)+' | '+getBroad(broad, 3)
    print '-----------'
    print 

def isWin(broad,player):
    if ((broad[1] ==player and broad[2] ==player and broad[3] ==player )
    or (broad[4] ==player and broad[5] ==player and broad[6] ==player )
    or (broad[7] ==player and broad[8] ==player and broad[9] ==player )
     
    or (broad[1] ==player and broad[4] ==player and broad[7] ==player )
    or (broad[2] ==player and broad[5] ==player and broad[8] ==player )
    or (broad[3] ==player and broad[6] ==player and broad[9] ==player )
     
    or (broad[7] ==player and broad[5] ==player and broad[3] ==player )
    or (broad[1] ==player and broad[5] ==player and broad[9] ==player )
    ):
        return True
    else:
        return False

# 用来进行优劣排序的的函数，对应rankfunction
def playWithEachOthers(players):
    losses = [0 for p in players]

    for i in range(len(players)):
        for j in range(len(players)):
            if i == j: continue

            winner = startGame([players[i], players[j]])

            if winner == 0:
                losses[j] += 2
            elif winner == 1:
                losses[i] += 2
            elif winner == -1:
                losses[i] += 1
                losses[j] += 1

    z = zip(losses, players)
    z.sort()

    return z

# 玩家和电脑对战入口
def play(players):
    printRule()
    winner = startGame(players,True)
    if winner == 0:
        print 'player0 win'
    elif winner == 1:
        print 'player1 win'
    else:
        print 'no winner'

class HumanPlayer:
    def evaluate(self, broad):
        print 'Enter next_step: ',
        next_step = int(raw_input())-1
        return next_step

if __name__ == '__main__':
    pass