#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

from . import counting_vote
from . import counting_vote_dong
#from . import electorates
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
					'19871216', '19921218', '19971218', '20021219', '20071219', '20121219', '20170509']}

localTarget_dict = {'pa':'local-pa', \
                    'ma':'local-ma', \
                    'pp':'local-pp', \
                    'mp':'local-mp', \
                    'ep':'local-ep', \
                    'ea':'local-ea'}

electionDayType_dict = {'president':1, 'assembly':2, 'local':4, 'by_election':0, 'local-ea':11}
# electionType: 1-대통령선거, 2-국회의원선거, 4-전국동시지방선거, 0-재보궐선거, 11-교육감선거

electionCode_dict = {'president':1, 'assembly':2, \
                    'local-pa':3, 'local-ma':4, \
                    'local-pp':5, 'local-mp':6, \
                    'assembly_PR':7, \
                    'local-pp_PR':8, 'local-mp_PR':9, \
                    'local-ep':10, 'local-ea':11}

electionType_eng_dict = {'president':'president', \
                        'assembly':'assembly', \
                        'assembly_PR':'assembly_PR', \
                        'local-pa':'local_provincal_administration', \
                        'local-ma':'local_municipal_administration', \
                        'local-pp':'local_provincal_parliament', \
                        'local-pp_PR':'local_provincal_parliament_PR', \
                        'local-mp':'local_municipal_parliament', \
                        'local-mp_PR':'local_municipal_parliament_PR', \
                        'local-ea':'local-eduAdministration', \
                        'local-ep':'local_eduParliament'}

electionType_kor_dict = {'president':'대통령', \
                        'assembly':'국회의원', \
                        'assembly_PR':'국회의원 비례대표', \
                        'local-pa':'시·도지사', \
                        'local-ma':'구·시·군의 장', \
                        'local-pp':'시·도의회 의원', \
                        'local-pp_PR':'시·도의회 의원 비례대표', \
                        'local-mp':'구·시·군의회 의원', \
                        'local-mp_PR':'구·시·군의회 의원 비례대표', \
                        'local-ea':'교육감', \
                        'local-ep':'시·도의회 교육의원'}

def Crawler(_target, _dataType, nth, _localType):

    election_name = _election_names[_target][int(nth)]
    target = _target
    if target == 'local':
        target = localTarget_dict[_localType]
    electionType = electionCode_dict[target]
    electionType_eng = electionType_eng_dict[target]
    electionType_kor = electionType_kor_dict[target]

    if _dataType == 'electorates':
        raise NotImplementedError("Electorates module is not implemented yet.")
        # 각 지역구/시군구별 선거인수 수집.
    elif _dataType == 'counting_vote':
        return counting_vote.Crawler(target, nth, election_name, electionType, electionType_eng, electionType_kor)
        # 각 지역구별 지역구 득표수 / 시군구별 비례대표 득표수 수집.
    elif _dataType == 'counting_vote_dong':
        raise NotImplementedError("Counting_vote_dong module is not implemented yet.")
        # 각 읍면동별 득표수 수집.
    elif _dataType == 'townCode':
        return townCode.Crawler(target, nth, election_name, electionType, electionType_eng, electionType_kor)
        # 각 지역구/시군구 인식코드 수집.
    elif _dataType == 'partyCode':
        return partyCode.Crawler(target, nth, election_name, electionType, electionType_eng, electionType_kor)
        # 각 정당 인식코드 수집.
    else:
        raise InvalidCrawlerError(target, _dataType, nth, election_name, electionType_eng, electionType)
