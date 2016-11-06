# -*- coding:utf-8 -*-

class BitMap:
    # maxval        最大值
    # bitsperword   一个int数的位数
    # shift         能表示 bitsperword 需要的位数
    # mask          能表示 bitsperword 需要的位数，用 16 进制表示
    def __init__(self, maxval, bitsperword=32, shift=5, mask=0x1F):
        self.bitsperword = bitsperword
        self.shift = shift
        self.mask = mask
        # 初始化位图，相当于函数1
        self.x = [0 for i in range(1+int(maxval/bitsperword))]

    def set(self, i):
        # i>>self.shift 操作等同于 i 除于 self.shift
        # i & self.mask 操作等同于 i 对 self.mask 求余
        self.x[i>>self.shift] |= (1<<(i & self.mask))

    def test(self, i):
        return self.x[i>>self.shift] & (1<<(i & self.mask))

def bitSort(lists, maxval):
    sortLists = []
    bit = BitMap(maxval)
    for val in lists:
        bit.set(val)
    for i in range(maxval):
        if bit.test(i):
            sortLists.append(i)
    return sortLists

if __name__ == '__main__':
    lists = [5,2,6,8,10,22,25,44,29,36,40,3,4,1,20,27,37]
    print (bitSort(lists, max(lists)))