#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

from .province_division import *
from .local_administration import *
from .local-ep import *
from .local_parliament import *
from .president import *
from utils import InvalidCrawlerError

def Crawler(target, nth, election_name, electionType, electionType_kor):
    if target == 'assembly':
        return assembly.Crawler(nth, election_name, electionType, target, electionType_kor)

    elif target == 'president' or \
        target == 'local-pa' or \
        target == 'local-ma' or \
        target == 'local-ea':
        return province_division.Crawler(nth, election_name, electionType, target, electionType_kor)

    elif target == 'local-pp' or \
        target == 'local-mp':
        return local_parliament.Crawler(nth, election_name, electionType, target, electionType_kor)

    elif target == 'local-ep':
        return local-ep.Crawler(nth, election_name, electionType, target, electionType_kor)
    else:
        raise InvalidCrawlerError('electorates', nth, election_name, electionType, target, electionType_kor)
