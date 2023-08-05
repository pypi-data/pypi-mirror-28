# -*- coding: utf-8 -*-


class InvalidChinaNumberError(ValueError):
    pass


CN_NUM = {
    '〇': 0,
    '一': 1,
    '二': 2,
    '三': 3,
    '四': 4,
    '五': 5,
    '六': 6,
    '七': 7,
    '八': 8,
    '九': 9,

    '零': 0,
    '壹': 1,
    '贰': 2,
    '叁': 3,
    '肆': 4,
    '伍': 5,
    '陆': 6,
    '柒': 7,
    '捌': 8,
    '玖': 9,

    '貮': 2,
    '两': 2,
}
CN_UNIT = {
    '十': 10,
    '拾': 10,
    '百': 100,
    '佰': 100,
    '千': 1000,
    '仟': 1000,
    '万': 10000,
    '萬': 10000,
    '亿': 100000000,
    '億': 100000000,
    '兆': 1000000000000,
}


def from_china(cn):
    """
    convert chinese numeral to number
    :param cn:
        a chinese numeral
    :return:
        a  number
    """
    lcn = list(cn)
    unit = 0    # 当前的单位
    ldig = []   # 临时数组

    while lcn:
        cndig = lcn.pop()

        if cndig in CN_UNIT:
            unit = CN_UNIT.get(cndig)
            if unit == 10000:
                ldig.append('w')        # 标示万位
                unit = 1
            elif unit == 100000000:
                ldig.append('y')        # 标示亿位
                unit = 1
            elif unit == 1000000000000:     # 标示兆位
                ldig.append('z')
                unit = 1

            continue

        else:
            dig = CN_NUM.get(cndig)

            if dig is None:
                raise InvalidChinaNumberError('Input China number:{} is NOT valid'.format(cn))

            if unit:
                dig = dig*unit
                unit = 0

            ldig.append(dig)

    if unit == 10:    # 处理10-19的数字
        ldig.append(10)

    ret = 0
    tmp = 0

    while ldig:
        x = ldig.pop()

        if x == 'w':
            tmp *= 10000
            ret += tmp
            tmp = 0

        elif x == 'y':
            tmp *= 100000000
            ret += tmp
            tmp = 0

        elif x == 'z':
            tmp *= 1000000000000
            ret += tmp
            tmp = 0

        else:
            tmp += x

    ret += tmp
    return ret


num = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']

k = ['零', '十', '百', '千', '万', '十', '百']

def __turn__(x, y):
    """
    取整取余并连接，返回连接好的字符串和余数
    :param x:
    :param y:
    :return:
    """
    if y >= 1:
        a = x // pow(10, y)
        b = x % pow(10, y)
        c = num[a] + k[y]
        if y > 4 and b < pow(10, 4):
            c += k[4]
        if (len(str(x)) - len(str(b))) >= 2 and b != 0:
            c += k[0]
    else:
        a = x
        b = 0
        c = num[a]

    return (c, b,)


def to_china(num):
    """
    convert integer to Chinese numeral
    TODO: only return '' for now
    :param num:
        a number
    :return:
        a string present Chinese number
    """
    c = __turn__(num, (len(str(num)) - 1))
    a = c[0]
    b = c[1]
    while b != 0:
        a += __turn__(b, (len(str(b)) - 1))[0]
        b = __turn__(b, (len(str(b)) - 1))[1]

    return a

#if __name__ == '__main__':
#    for i in range(0,50):
#        print(to_china(i))