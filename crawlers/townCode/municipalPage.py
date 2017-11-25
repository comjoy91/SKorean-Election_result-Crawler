#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from crawlers.townCode.base_municipalPage import *
from utils import sanitize, InvalidCrawlerError

def Crawler(nth, election_name, electionType, target, target_kor):
	if 1 <= nth <= 3:
		crawler = Municipal_townCodeCrawler_GuOld(int(nth), election_name, electionType)
	elif 4 <= nth <= 6:
		crawler = Municipal_townCodeCrawler_Old(int(nth), election_name, electionType)
	elif nth == 7:
		raise InvalidCrawlerError('townCode', nth, election_name, electionType)
		#"최근선거"로 들어갈 때의 code: crawler = Municipal_townCodeCrawler_Recent(int(nth), election_name, electionType)
	else:
		raise InvalidCrawlerError('townCode', nth, election_name, electionType)

	crawler.nth = nth
	crawler.target = target
	crawler.target_kor = target_kor

	return crawler



class Municipal_townCodeCrawler_GuOld(JSONCrawler_municipal):

	def __init__(self, nth, _election_name, _election_type):
		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_GuOld.json'
		self.urlParam_city_codes = dict(electionId='0000000000', electionCode=_election_name, subElectionCode =_election_type)

		# 여기서 크롤링된 데이터는 행정구역(시군구, 행정구 포함) 단위로 분류됨.
		# n:1~2 - 여기서의 행정구역은 국회의원 지역구 단위로 분류되어, 같은 시군구에서도 갑/을로 분구된 것이 따로따로 표기됨. 단, 선거구가 합구된 곳은 시군구별로 다 명기됨.
		self.urlPath_town_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeBySgJson_GuOld.json'
		self.urlParam_town_list = dict(electionId='0000000000', electionCode=_election_name, subElectionCode =_election_type)

		# 여기서 크롤링된 데이터는 선거구 단위로 분류됨.
		self.urlPath_sgg_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getSggTownCodeJson_GuOld.json'
		self.urlParam_sgg_list = dict(electionId='0000000000', electionName=_election_name, electionCode =_election_type)



class Municipal_townCodeCrawler_Old(JSONCrawler_municipal):

	def __init__(self, nth, _election_name, _election_type):
		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'
		self.urlParam_city_codes = dict(electionId='0000000000', electionCode=_election_name, subElectionCode =_election_type)

		# 여기서 크롤링된 데이터는 행정구역(시군구, 행정구 포함) 단위로 분류됨.
		self.urlPath_town_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeBySgJson_Old.json'
		self.urlParam_town_list = dict(electionId='0000000000', electionCode=_election_name, subElectionCode =_election_type)

		# 여기서 크롤링된 데이터는 선거구 단위로 분류됨.
		self.urlPath_sgg_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getSggTownCodeJson_Old.json'
		self.urlParam_sgg_list = dict(electionId='0000000000', electionName=_election_name, electionCode =_election_type)


class Municipal_townCodeCrawler_Recent(JSONCrawler_municipal):

	def __init__(self, nth, _election_name, _election_type):
		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'
		self.urlParam_city_codes = dict(electionId=_election_name, electionCode=_election_type)

		# 여기서 크롤링된 데이터는 행정구역(시군구, 행정구 포함) 단위로 분류됨.
		self.urlPath_town_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeJson.json'
		self.urlParam_town_list = dict(electionId=_election_name, electionCode=_election_type)

		# 여기서 크롤링된 데이터는 선거구 단위로 분류됨.
		self.urlPath_sgg_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getSggTownCodeJson.json'
		self.urlParam_sgg_list = dict(electionId=_election_name, electionCode=_election_type)
