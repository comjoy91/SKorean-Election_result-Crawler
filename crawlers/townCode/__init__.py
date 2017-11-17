#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

from .assembly import *
from .local_administration import *
from .local_eduParliament import *
from .local_parliament import *
from .president import *
from utils import InvalidCrawlerError

def Crawler(target, nth, election_name, localType_int):
    if target == 'assembly':
        return assembly.Crawler(nth, election_name)

    elif target == 'local_provincal_administration' or \
        target == 'local_municipal_administration' or \
        target == 'local_eduAdministration':
        return local_administration.Crawler(nth, election_name, localType_int, target)

    elif target == 'local_provincal_parliament' or \
        target == 'local_municipal_parliament':
        return local_parliament.Crawler(nth, election_name, localType_int, target)

    elif target == 'local_eduParliament':
        return local_eduParliament.Crawler(nth, election_name, localType_int, target)

    elif target == 'president':
        return president.Crawler(nth, election_name)

    else:
        raise InvalidCrawlerError('townCode', target, nth, election_name, localType_int)
