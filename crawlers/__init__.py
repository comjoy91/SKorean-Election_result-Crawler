#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

from . import counting_vote
from . import counting_vote_dong
from . import electorates
from . import townCode
from . import partyCode
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

electionCode_dict = {'president':1, 'assembly':2, \
                    'local_provincal_administration':3, 'local_municipal_administration':4, \
                    'local_provincal_parliament':5, 'local_municipal_parliament':6, \
                    'local_eduParliament':10, 'local_eduAdministration':11}
localType_str_dict = \
	{'pg':'local_provincal_administration', \
	'mg':'local_municipal_administration', \
	'pm':'local_provincal_parliament', \
	'mm':'local_municipal_parliament', \
	'em':'local_eduParliament', \
	'eg':'local_eduAdministration'}

electionType_kor_dict = {'president':'대통령', 'assembly':'국회의원', \
                'local_provincal_administration':'시·도지사', \
                'local_municipal_administration':'구·시·군의 장', \
                'local_provincal_parliament':'시·도의회 의원', \
                'local_municipal_parliament':'구·시·군의회 의원', \
                'local_eduAdministration':'교육감', \
                'local_eduParliament':'시·도의회 교육의원'}

def Crawler(_target, _dataType, nth, _localType):

    election_name = _election_names[_target][int(nth)]
    target = _target
    if target == 'local':
        target = localType_str_dict[_localType]
    electionType = electionCode_dict[target]
    electionType_kor = electionType_kor_dict[target]

    if _dataType == 'electorates':
        return raise NotImplementedError("Electorates module is not implemented yet.")
        # 각 지역구/시군구별 선거인수 수집.
    elif _dataType == 'counting_vote':
        return counting_vote.Crawler(target, nth, election_name, localType)
        # 각 지역구별 지역구 득표수 / 시군구별 비례대표 득표수 수집.
    elif _dataType == 'counting_vote_dong':
        return counting_vote_dong.Crawler(target, nth, election_name, localType)
        # 각 읍면동별 득표수 수집.
    elif _dataType == 'townCode':
        return townCode.Crawler(target, nth, election_name, electionType, electionType_kor)
        # 각 지역구/시군구 인식코드 수집.
    elif _dataType == 'partyCode':
        return partyCode.Crawler(target, nth, election_name)
        # 각 정당 인식코드 수집.
    else:
        raise InvalidCrawlerError(target, _dataType, nth, election_name, electionType)
