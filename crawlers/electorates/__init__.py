#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

from .province_division import *
from .local_administration import *
from .local_eduParliament import *
from .local_parliament import *
from .president import *
from utils import InvalidCrawlerError

def Crawler(target, nth, election_name, electionType, electionType_kor):
    if target == 'assembly':
        return assembly.Crawler(nth, election_name, electionType, target, electionType_kor)

    elif target == 'president' or \
        target == 'local_provincal_administration' or \
        target == 'local_municipal_administration' or \
        target == 'local_eduAdministration':
        return province_division.Crawler(nth, election_name, electionType, target, electionType_kor)

    elif target == 'local_provincal_parliament' or \
        target == 'local_municipal_parliament':
        return local_parliament.Crawler(nth, election_name, electionType, target, electionType_kor)

    elif target == 'local_eduParliament':
        return local_eduParliament.Crawler(nth, election_name, electionType, target, electionType_kor)
    else:
        raise InvalidCrawlerError('electorates', nth, election_name, electionType, target, electionType_kor)
