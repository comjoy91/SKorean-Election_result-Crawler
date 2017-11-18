#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

from .constituency_in_province import *
from .localDivision import *
from .constituency_in_municipal import *
from utils import InvalidCrawlerError

def Crawler(target, nth, election_name, electionType):

    if target == 'local_eduParliament' or \
        target == 'assembly':
        return constituency_in_province.Crawler(nth, election_name, electionType, target)

    elif target == 'local_provincal_administration' or \
        target == 'local_municipal_administration' or \
        target == 'local_eduAdministration' or \
        target == 'president':
        return localDivision.Crawler(nth, election_name, electionType, target)

    elif target == 'local_provincal_parliament' or \
        target == 'local_municipal_parliament':
        return constituency_in_municipal.Crawler(nth, election_name, electionType, target)

    else:
        raise InvalidCrawlerError('townCode', target, nth, election_name, electionType)
