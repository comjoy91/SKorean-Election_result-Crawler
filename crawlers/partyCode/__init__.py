#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

from .crawler_type import *
from utils import InvalidCrawlerError

def Crawler(target, nth, election_name, electionType, electionType_eng, electionType_kor):
    if target == 'assembly' or \
        target == 'local-pa' or \
        target == 'local-ma' or \
        target == 'local-ea' or \
        target == 'local-pp' or \
        target == 'local-mp' or \
        target == 'local-ep' or \
        target == 'president':
        return crawler_type.Crawler(nth, election_name, electionType, target, electionType_eng, electionType_kor)
    else:
        raise InvalidCrawlerError(target, 'partyCode', nth)
