#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

from .crawler_type import *
from utils import InvalidCrawlerError

def Crawler(target, nth, election_name, electionType, electionType_kor):
    if target == 'assembly' or \
        target == 'local_provincal_parliament' or \
        target == 'local_municipal_parliament' or \
        target == 'local_eduParliament' or \
        target == 'president' or \
        target == 'local_provincal_administration' or \
        target == 'local_municipal_administration' or \
        target == 'local_eduAdministration':
        return crawler_type.Crawler(nth, election_name, electionType, target, electionType_kor)
    else:
        raise InvalidCrawlerError('electorates', nth, election_name, electionType, target, electionType_kor)
