#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from crawlers.townCode.base_provincePage import *
from crawlers.townCode.base_municipalPage import *
from utils import sanitize, InvalidCrawlerError

def Crawler(nth, election_name, localType_int, target):
	if 1 <= nth <= 3:
		crawler = LocalDivision_CodeCrawler_GuOld(int(nth), election_name, localType_int, target)
	elif 4 <= nth <= 6:
		crawler = LocalDivision_CodeCrawler_Old(int(nth), election_name, localType_int, target)
	elif nth == 7:
		raise InvalidCrawlerError('townCode', nth, election_name, localType_int, target)
		#"최근선거"로 들어갈 때의 code: crawler = LocalDivision_CodeCrawler_Recent(int(nth), election_name, localType_int, target)
	else:
		raise InvalidCrawlerError('townCode', nth, election_name, localType_int, target)
	return crawler



class LocalDivision_CodeCrawler_GuOld(JSONCrawler_province):

	def __init__(self, nth, _election_name, _localType_int, _target):
		self.nth = nth
		self.localType_int = _localType_int
		self.target = _target
		self.elemType = 'local_division'
		# 여기서 크롤링된 데이터는 행정구역(시군구, 행정구 포함) 단위로 분류됨.
		# n:1~2 - 여기서 크롤링된 데이터가 국회의원 지역구 단위로 분류되어, 같은 시군구에서도 갑/을로 분구된 것이 따로따로 표기됨. 단, 선거구가 합구된 곳은 시군구별로 다 명기됨.
		# n:3 - 여기서 크롤링된 데이터는 시군구 단위로 분류됨.

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_GuOld.json'
		self.urlParam_city_codes = dict(electionId='0000000000', \
										electionCode=_election_name, subElectionCode =_localType_int)

		self.urlPath_town_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeBySgJson_GuOld.json'
		self.urlParam_town_list = dict(electionId='0000000000', \
										electionCode=_election_name, subElectionCode =_localType_int)

		self.next_crawler = Constituency_CodeCrawler_GuOld(nth, _election_name, _localType_int, _target)



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

		self.next_crawler = Constituency_CodeCrawler_Old(nth, _election_name, _localType_int, _target)


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

		self.next_crawler = Constituency_CodeCrawler_Recent(nth, _election_name, _localType_int, _target)




class Constituency_CodeCrawler_GuOld(JSONCrawler_municipal):

	def __init__(self, nth, _election_name, _localType_int, _target):
		self.nth = nth
		self.localType_int = _localType_int
		self.target = _target
		self.elemType = 'constituency_in_municipal_division'
		# 여기서 크롤링된 데이터는 광역/기초자치의회 지역 선거구 단위로 분류됨.

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_GuOld.json'
		self.urlParam_city_codes = dict(electionId='0000000000', \
										electionCode=_election_name, subElectionCode =_localType_int)

		self.urlPath_town_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeBySgJson_GuOld.json'
		self.urlParam_town_codes = dict(electionId='0000000000', \
										electionCode=_election_name, subElectionCode =_localType_int)

		self.urlPath_sgg_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getSggTownCodeJson_GuOld.json'
		self.urlParam_sgg_list = dict(electionId='0000000000', \
										electionName=_election_name, electionCode =_localType_int)



class Constituency_CodeCrawler_Old(JSONCrawler_municipal):

	def __init__(self, nth, _election_name, _localType_int, _target):
		self.nth = nth
		self.localType_int = _localType_int
		self.target = _target
		self.elemType = 'constituency_in_municipal_division'
		# 여기서 크롤링된 데이터는 국회의원 지역 선거구 단위로 분류됨.

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'
		self.urlParam_city_codes = dict(electionId='0000000000', \
										electionCode=_election_name, subElectionCode =_localType_int)

		self.urlPath_town_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeBySgJson_Old.json'
		self.urlParam_town_codes = dict(electionId='0000000000', \
										electionCode=_election_name, subElectionCode =_localType_int)

		self.urlPath_sgg_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getSggTownCodeJson_Old.json'
		self.urlParam_sgg_list = dict(electionId='0000000000', \
										electionName=_election_name, electionCode =_localType_int)


class Constituency_CodeCrawler_Recent(JSONCrawler_municipal):

	def __init__(self, nth, _election_name, _localType_int, _target):
		self.nth = nth
		self.localType_int = _localType_int
		self.target = _target
		self.elemType = 'constituency_in_municipal_division'
		# 여기서 크롤링된 데이터는 국회의원 지역 선거구 단위로 분류됨.

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'
		self.urlParam_city_codes = dict(electionId=_election_name, electionCode=_localType_int)

		self.urlPath_town_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeBySgJson.json'
		self.urlParam_town_codes = dict(electionId=_election_name, electionCode=_localType_int)

		self.urlPath_sgg_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getSggTownCodeJson.json'
		self.urlParam_sgg_list = dict(electionId=_election_name, electionCode=_localType_int)
