#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

from .provincePage import *
from .municipalPage import *
from utils import InvalidCrawlerError

def Crawler(target, nth, election_name, electionType, electionType_kor):

    if target == 'local_eduParliament' or \
        target == 'assembly'or \
        target == 'local_provincal_administration' or \
        target == 'local_municipal_administration' or \
        target == 'local_eduAdministration' or \
        target == 'president':
        return provincePage.Crawler(nth, election_name, electionType, target, electionType_kor)

    elif target == 'local_provincal_parliament' or \
        target == 'local_municipal_parliament':
        return municipalPage.Crawler(nth, election_name, electionType, target, electionType_kor)

    else:
        raise InvalidCrawlerError('townCode', target, nth, election_name, electionType)
