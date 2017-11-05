#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

from . import counting_vote
from . import counting_vote_dong
from . import electorates
from . import townCode
from . import partyCode
from utils import InvalidCrawlerError

def Crawler(target, _type, nth, level):
    if _type == 'electorates':
        return electorates.Crawler(target, nth)
        # 각 지역구/시군구별 선거인수 수집.
    elif _type == 'counting_vote':
        return counting_vote.Crawler(target, nth)
        # 각 지역구별 지역구 득표수 / 시군구별 비례대표 득표수 수집.
    elif _type == 'counting_vote_dong':
        return counting_vote_dong.Crawler(target, nth)
        # 각 읍면동별 득표수 수집.
    elif _type == 'townCode':
        return townCode.Crawler(target, nth)
        # 각 지역구/시군구 인식코드 수집.
    elif _type == 'partyCode':
        return partyCode.Crawler(target, nth)
        # 각 정당 인식코드 수집.
    else:
        raise InvalidCrawlerError(target, _type, nth)
