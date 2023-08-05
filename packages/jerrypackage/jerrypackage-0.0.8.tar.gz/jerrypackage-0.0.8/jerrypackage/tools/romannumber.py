# -*-coding:utf-8-*-

import re


class OutOfRangeError(ValueError):
    pass


class NotIntegerError(ValueError):
    pass


class InvalidRomanNumeralError(ValueError):
    pass


roman_numeral_map = (
                    ('M', 1000),
                    ('CM', 900),
                    ('D', 500),
                    ('CD', 400),
                    ('C', 100),
                    ('XC', 90),
                    ('L', 50),
                    ('XL', 40),
                    ('X', 10),
                    ('IX', 9),
                    ('V', 5),
                    ('IV', 4),
                    ('I', 1)
                    )


# 使用松散正则表达式，方便代码维护, 使用时候需要加上re.VERBOSE参数
pattern = '''
^                       # beginning of string
M{0,3}                  # thousands - 0 to 3 Ms
(CM|CD|D?C{0,3})        # hundreds - 900(CM), 400(CD), 0-300 (0 to 3 Cs), 500-800(D, followed by 0 to 3 Cs)
(XC|XL|L?X{0,3})        # tens - 90(XC), 40 (XL), 0-30 (0 to 3 Xs), 50-80(L, followed by 0 to 3 Xs)
(IX|IV|V?I{0,3})        # ones - 9(IX), 4(IV), 0-3 (0 to 3 Is), 5-8(V, followed by 0 to 3 Is)
$                       # end of string
'''
roman_numeral_pattern = re.compile(pattern, re.X)


def from_roman(s):
    """ convert roman numeral to integer """
    if not s:
        raise InvalidRomanNumeralError('Input can not be blank')

    if not roman_numeral_pattern.search(s):
        raise InvalidRomanNumeralError('Invalid Roman numeral: {0}'.format(s))

    result = 0
    index = 0
    for numeral, integer in roman_numeral_map:
        while s[index:index + len(numeral)] == numeral:
            result += integer
            index += len(numeral)
            # print('found', numeral, 'of length', len(numeral), ', adding', integer)

    return result


def to_roman(n):
    """
    convert integer to Roman numeral
    :param n:
        a number
    :return:
        a string present roman number
    """
    if not (0 < n < 4000):
        raise OutOfRangeError('number out of range (must be 1..3999)')
    if not isinstance(n, int):
        raise NotIntegerError('non-integers can not be converted')

    result = ''
    for numeral, integer in roman_numeral_map:
        while n >= integer:
            result += numeral
            n -= integer
            # print('subtracting {0} from input, adding {1} to output'.format(integer, numeral))
    return result
