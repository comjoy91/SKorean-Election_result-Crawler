#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

from .provincePage import *
from .municipalPage import *
from utils import InvalidCrawlerError

def Crawler(target, nth, election_name, electionType, electionType_eng, electionType_kor):

    if target == 'local-ep' or \
        target == 'assembly'or \
        target == 'local-pa' or \
        target == 'local-ma' or \
        target == 'local-ea' or \
        target == 'president':
        return provincePage.Crawler(nth, election_name, electionType, target, electionType_eng, electionType_kor)

    elif target == 'local-pp' or \
        target == 'local-mp':
        #return municipalPage.Crawler(nth, election_name, electionType, target, electionType_eng, electionType_kor)
        return provincePage.Crawler(nth, election_name, electionType, target, electionType_eng, electionType_kor)


    else:
        raise InvalidCrawlerError('townCode', target, nth, election_name, electionType, electionType_eng, electionType_kor)
