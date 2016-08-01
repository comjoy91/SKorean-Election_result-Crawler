#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

from .assembly import *
from utils import InvalidCrawlerError

def Crawler(target, nth):
    if target == 'assembly':
        #raise NotImplementedError('Local election vote counting crawler')
        return assembly.Crawler(nth)
    elif target == 'local':
        raise NotImplementedError('Local election vote counting crawler')
    elif target == 'president':
        raise NotImplementedError('Presidential election vote counting crawler')
    else:
        raise InvalidCrawlerError(target, 'electorates', nth)
