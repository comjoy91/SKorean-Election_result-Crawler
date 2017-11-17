#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from crawlers.townCode.base_provincePage import *
from utils import sanitize, InvalidCrawlerError

def Crawler(nth, election_name, localType_int, target):
	if nth == 1:
		raise NotImplementedError('Educational Parliament Election was not held in 1995.')
	elif nth == 2:
		raise NotImplementedError('Educational Parliament Election was not held in 1998.')
	elif nth == 3:
		raise NotImplementedError('Educational Parliament Election was not held in 2002.')
	elif 4 <= nth <= 6:
		crawler = LocalDivision_CodeCrawler_Old(int(nth), election_name, localType_int, target)
	elif nth == 7:
		raise InvalidCrawlerError('townCode', nth, election_name, localType_int, target)
		#"최근선거"로 들어갈 때의 code: crawler = LocalDivision_CodeCrawler_Recent(int(nth), election_name, localType_int, target)
	else:
		raise InvalidCrawlerError('townCode', nth, election_name, localType_int, target)
	return crawler



class LocalDivision_CodeCrawler_Old(JSONCrawler_province):

	def __init__(self, nth, _election_name, _localType_int, _target):
		self.nth = nth
		self.localType_int = _localType_int
		self.target = _target
		self.elemType = 'local_division'
		# 여기서 크롤링된 데이터는 행정구역(시군구, 행정구 포함) 단위로 분류됨.

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'
		self.urlParam_city_codes = dict(electionId='0000000000', \
										electionCode=_election_name, subElectionCode =_localType_int)

		self.urlPath_town_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeBySgJson_Old.json'
		self.urlParam_town_list = dict(electionId='0000000000', \
										electionCode=_election_name, subElectionCode =_localType_int)

		self.next_crawler = Constituency_CodeCrawler_Old(_election_name, _localType_int, _target)
		self.next_crawler.nth = nth


class LocalDivision_CodeCrawler_Recent(JSONCrawler_province):

	def __init__(self, nth, _election_name, _localType_int, _target):
		self.nth = nth
		self.localType_int = _localType_int
		self.target = _target
		self.elemType = 'local_division'
		# 여기서 크롤링된 데이터는 행정구역(시군구, 행정구 포함) 단위로 분류됨.

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'
		self.urlParam_city_codes = dict(electionCode=_localType_int, electionId=_election_name)

		self.urlPath_town_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeJson.json'
		self.urlParam_town_list = dict(electionCode=_localType_int, electionId=_election_name)

		self.next_crawler = Constituency_CodeCrawler_Recent(_election_name, _localType_int, _target)
		self.next_crawler.nth = nth



class Constituency_CodeCrawler_Old(JSONCrawler_province):

	def __init__(self, _election_name, _localType_int, _target):
		self.localType_int = _localType_int
		self.target = _target
		self.elemType = 'constituency_in_province'
		# 여기서 크롤링된 데이터는 광역자치단체별 교육의원 지역 선거구 단위로 분류됨.

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'
		self.urlParam_city_codes = dict(electionId='0000000000', \
										electionCode=_election_name, subElectionCode =_localType_int)

		self.urlPath_sgg_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getSggCityCodeJson_Old.json'
		self.urlParam_sgg_list = dict(electionId='0000000000', \
										electionName=_election_name, electionCode =_localType_int)


class Constituency_CodeCrawler_Recent(JSONCrawler_province):

	def __init__(self, _election_name, _localType_int, _target):
		self.localType_int = _localType_int
		self.target = _target
		self.elemType = 'constituency_in_province'
		# 여기서 크롤링된 데이터는 광역자치단체별 교육의원 지역 선거구 단위로 분류됨.

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'
		self.urlParam_city_codes = dict(electionCode=_localType_int, electionId=_election_name)

		self.urlPath_sgg_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getSggCityCodeJson.json'
		self.urlParam_sgg_list = dict(electionCode=_localType_int, electionId=_election_name)
