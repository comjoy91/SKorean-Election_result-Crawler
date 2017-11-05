#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

from .assembly import *
from .president import *
from utils import InvalidCrawlerError

_election_names = {\
    'assembly': [None, '19480510', '19500530', '19540520', '19580502', '19600729',\
					'19631126', '19670608', '19710525', '19730227', '19781212', '19810325', '19850212',\
					'19880426', '19920324', '19960411', '20000413', '20040415', '20080409', '20120411', '20160413'],
    'local': [None, '19950627', '19980604', '20020613', '20060531', '20100602', '20140604'],
    'president': [None, '19480720', '19520805', '19560515', '19600315',\
					'19631015', '19670503', '19710427',\
					'19721223', '19780706', '19791206', '19800827', '19810225',\
					'19871216', '19921218', '19971218', '20021219', '20071219', '20121219', '0020170509']}

def Crawler(target, nth, localType):
    if target == 'assembly':
        return assembly.Crawler(nth, _election_names['assembly'][int(nth)])
    elif target == 'local' and (localType=='pg' or localType=='mg' or localType=='eg'):
        #return local_administration.Crawler(nth, _election_names['local'][int(nth)], localType)
        raise NotImplementedError('localLocal')
    elif target == 'local' and (localType=='pm' or localType=='mm'):
        #return local_parliament.Crawler(nth, _election_names['local'][int(nth)], localType)
        raise NotImplementedError('localLocal')
    elif target == 'local' and (localType=='em'):
        #return local_eduParliament.Crawler(nth, _election_names['local'][int(nth)], localType)
        raise NotImplementedError('localLocal')
    elif target == 'president':
        return president.Crawler(nth, _election_names['president'][int(nth)])
    else:
        raise InvalidCrawlerError(target, 'counting_vote', nth, localType)
