def bytes2human(n):
    """
    >>> bytes2human(10000)
    9K
    >>> bytes2human(100001221)
    95M
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10

    for s in reversed(symbols):
        if n >= prefix[s]:
            value = (float(n) / prefix[s])
            return '%.2f%s' % (value, s)
    return '%sB' % n
