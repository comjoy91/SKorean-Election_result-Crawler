#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from crawlers.townCode.base_provincePage import *
from utils import sanitize, InvalidCrawlerError

def Crawler(nth, election_name, _localType):
	localType_dict = {'pg':3, 'mg':4, 'pm':5, 'mm':6, 'em':10, 'eg':11}
	localType_int = localType_dict[_localType]
	target_dict = \
		{'pg':'local_provincal_administration', \
		'mg':'local_municipal_administration', \
		'pm':'local_provincal_parliament', \
		'mm':'local_municipal_parliament', \
		'em':'local_eduParliament', \
		'eg':'local_eduAdministration'}
	target = target_dict[_localType]

	if _localType=='em' and nth == 1:
		raise NotImplementedError('Educational Governer Election was not held in 1995.')
	elif _localType=='em' and nth == 2:
		raise NotImplementedError('Educational Governer Election was not held in 1998.')
	elif _localType=='em' and nth == 3:
		raise NotImplementedError('Educational Governer Election was not held in 2002.')
	elif 4 <= nth <= 6:
		crawler = LocalDivision_CodeCrawler_Old(int(nth), election_name, localType_int, target)
	elif nth == 7:
		raise InvalidCrawlerError('local', 'townCode', nth)
		#"최근선거"로 들어갈 때의 code: crawler = LocalDivision_CodeCrawler_Recent(int(nth), election_name, localType_int, target)
	else:
		raise InvalidCrawlerError('local', 'townCode', nth)
	return crawler



class LocalDivision_CodeCrawler_Old(JSONCrawler_province):
	elemType = 'local_division'
	# 여기서 크롤링된 데이터는 행정구역(시군구, 행정구 포함) 단위로 분류됨.

	urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'
	urlParam_city_codes = dict(electionId='0000000000')

	urlPath_town_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeBySgJson_Old.json'
	urlParam_town_list = dict(electionId='0000000000')

	def __init__(self, nth, _election_name, _localType_int, _target):
		self.nth = nth
		self.localType_int = _localType_int
		self.target = _target
		self.urlParam_city_codes['electionCode'] = _election_name
		self.urlParam_city_codes['subElectionCode'] = _localType_int
		self.urlParam_town_list['electionCode'] = _election_name
		self.urlParam_town_list['subElectionCode'] = _localType_int

		self.next_crawler = Constituency_CodeCrawler_Old(_election_name, _localType_int, _target)
		self.next_crawler.nth = nth


class LocalDivision_CodeCrawler_Recent(JSONCrawler_province):
	elemType = 'local_division'
	# 여기서 크롤링된 데이터는 행정구역(시군구, 행정구 포함) 단위로 분류됨.

	urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'
	urlParam_city_codes = dict()

	urlPath_town_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeJson.json'
	urlParam_town_list = dict()

	def __init__(self, nth, _election_name, _localType_int, _target):
		self.nth = nth
		self.localType_int = _localType_int
		self.target = _target
		self.urlParam_city_codes['electionCode'] = _localType_int
		self.urlParam_town_list['electionCode'] = _localType_int

		self.next_crawler = Constituency_CodeCrawler_Recent(_election_name, _localType_int, _target)
		self.next_crawler.nth = nth



class Constituency_CodeCrawler_Old(JSONCrawler_province):
	elemType = 'constituency_in_province'
	# 여기서 크롤링된 데이터는 광역자치단체별 교육의원 지역 선거구 단위로 분류됨.

	urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'
	urlParam_city_codes = dict(electionId='0000000000')

	urlPath_sgg_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getSggCityCodeJson_Old.json'
	urlParam_sgg_list = dict(electionId='0000000000')

	def __init__(self, _election_name, _localType_int, _target):
		self.localType_int = _localType_int
		self.target = _target
		self.urlParam_city_codes['electionCode'] = _election_name
		self.urlParam_city_codes['subElectionCode'] = _localType_int
		self.urlParam_sgg_list['electionName'] = _election_name
		self.urlParam_sgg_list['electionCode'] = _localType_int



class Constituency_CodeCrawler_Recent(JSONCrawler_province):
	elemType = 'constituency_in_province'
	# 여기서 크롤링된 데이터는 광역자치단체별 교육의원 지역 선거구 단위로 분류됨.

	urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'
	urlParam_city_codes = dict()

	urlPath_sgg_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getSggCityCodeJson.json'
	urlParam_sgg_list = dict()

	def __init__(self, _election_name, _localType_int, _target):
		self.localType_int = _localType_int
		self.target = _target
		self.urlParam_city_codes['electionCode'] = _localType_int
		self.urlParam_sgg_list['electionCode'] = _localType_int
