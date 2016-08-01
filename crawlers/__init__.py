#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

from . import counting_vote
from . import electorates
from utils import InvalidCrawlerError

def Crawler(target, _type, nth, level):
    if _type == 'electorates':
        return electorates.Crawler(target, nth)
        # return electorates.Crawler(target, nth)
    elif _type == 'counting_vote':
        return counting_vote.Crawler(target, nth)
    else:
        raise InvalidCrawlerError(target, _type, nth)
