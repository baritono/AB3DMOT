# Author: Xinshuo Weng
# Email: xinshuo.weng@gmail.com

import time

from xinshuo_miscellaneous.type_check import islistoflist


def get_timestring():
    return time.strftime('%Y%m%d_%Hh%Mm%Ss')


def merge_listoflist(listoflist, unique=False, debug=True):
    '''
    merge a list of list

    parameters:
        unique: 	boolean

    outputs:
        if unique false:	a combination of lists in original order
        if unique true:		a combination of lists with only unique items, the resulting list is not in original order
    '''
    if debug:
        assert islistoflist(listoflist), 'the input is not a list of list'
    merged = list()
    for individual in listoflist:
        merged = merged + individual

    if unique:
        merged = list(set(merged))
        merged.sort()

    return merged
