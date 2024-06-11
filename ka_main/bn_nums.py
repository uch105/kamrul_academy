num_dict = {
    '1':'১',
    '2':'২',
    '3':'৩',
    '4':'৪',
    '5':'৫',
    '6':'৬',
    '7':'৭',
    '8':'৮',
    '9':'৯',
    '0':'০',
    '.':'.',
}
bn_dict = {
    '১':'1',
    '২':'2',
    '৩':'3',
    '৪':'4',
    '৫':'5',
    '৬':'6',
    '৭':'7',
    '৮':'8',
    '৯':'9',
    '০':'0',
    '.':'.',
}
def to_bn(ss):
    gen = ""
    for s in ss:
        gen += num_dict.get(s)
    return gen

def to_num(ss):
    gen = ""
    for s in ss:
        gen += bn_dict.get(s)
    return gen