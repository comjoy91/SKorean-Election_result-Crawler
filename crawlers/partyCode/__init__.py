#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

from .assembly import *
from .local import *
from .president import *
from utils import InvalidCrawlerError

def Crawler(target, nth, election_name):
    if target == 'assembly':
        return assembly.Crawler(nth, election_name)
    elif target == 'local_provincal_administration' or \
        target == 'local_municipal_administration' or \
        target == 'local_eduAdministration' or \
        target == 'local_provincal_parliament' or \
        target == 'local_municipal_parliament' or \
        target == 'local_eduParliament':
        return local.Crawler(nth, election_name, target)
    elif target == 'president':
        return president.Crawler(nth, election_name)
    else:
        raise InvalidCrawlerError(target, 'partyCode', nth)
