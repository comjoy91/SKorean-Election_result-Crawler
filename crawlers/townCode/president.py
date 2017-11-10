#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from crawlers.townCode.base_provincePage import *
from utils import sanitize, InvalidCrawlerError

def Crawler(nth, election_name):
	if nth == 1:
		raise NotImplementedError('The 1st presidential election(in 1948) was held in National Assembley: We cannot crawl the data.')
	elif 2 <= nth <= 7:
		crawler = LocalDivision_CodeCrawler_GuOld(int(nth), election_name)
	elif nth == 8:
		raise NotImplementedError('The 8th presidential election(in 1972) was held in 통일주체국민회의: We cannot crawl the data.')
	elif nth == 9:
		raise NotImplementedError('The 9th presidential election(in 1978) was held in 통일주체국민회의: We cannot crawl the data.')
	elif nth == 10:
		raise NotImplementedError('The 10th presidential election(in 1979) was held in 통일주체국민회의: We cannot crawl the data.')
	elif nth == 11:
		raise NotImplementedError('The 11th presidential election(in 1980) was held in 통일주체국민회의: We cannot crawl the data.')
	elif nth == 12:
		raise NotImplementedError('The 12th presidential election(in 1981) was held by a indirect election: We cannot crawl the data.')
	elif 13 <= nth <= 16:
		crawler = LocalDivision_CodeCrawler_GuOld(int(nth), election_name)
	elif 17 <= nth <= 18:
		crawler = LocalDivision_CodeCrawler_Old(int(nth), election_name)
	elif nth == 19:
		crawler = LocalDivision_CodeCrawler_Recent(int(nth), election_name)
	else:
		raise InvalidCrawlerError('president', 'townCode', nth)
	return crawler



class LocalDivision_CodeCrawler_GuOld(JSONCrawler_province):
	target = 'presidential'
	elemType = 'local_division'
	# 여기서 크롤링된 데이터는 행정구역(시군구, 행정구 포함) 단위로 분류됨.

	urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_GuOld.json'
	urlParam_city_codes = dict(electionId='0000000000')

	urlPath_town_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeBySgJson_GuOld.json'
	urlParam_town_list = dict(electionId='0000000000', subElectionCode=1)

	def __init__(self, nth, _election_name):
		self.nth = nth
		self.urlParam_city_codes['electionCode'] = _election_name
		self.urlParam_town_list['electionCode'] = _election_name


class LocalDivision_CodeCrawler_Old(JSONCrawler_province):
	target = 'presidential'
	elemType = 'local_division'
	# 여기서 크롤링된 데이터는 행정구역(시군구, 행정구 포함) 단위로 분류됨.

	urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'
	urlParam_city_codes = dict(electionId='0000000000', subElectionCode=1)

	urlPath_town_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeBySgJson_Old.json'
	urlParam_town_list = dict(electionId='0000000000', subElectionCode=1)

	def __init__(self, nth, _election_name):
		self.nth = nth
		self.urlParam_city_codes['electionCode'] = _election_name
		self.urlParam_town_list['electionCode'] = _election_name



class LocalDivision_CodeCrawler_Recent(JSONCrawler_province):
	target = 'presidential'
	elemType = 'local_division'
	# 여기서 크롤링된 데이터는 행정구역(시군구, 행정구 포함) 단위로 분류됨.

	urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'
	urlParam_city_codes = dict(electionCode=1)

	urlPath_town_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeJson.json'
	urlParam_town_list = dict(electionCode=1)

	def __init__(self, nth, _election_name):
		self.nth = nth
		self.urlParam_city_codes['electionId'] = _election_name
		self.urlParam_town_list['electionId'] = _election_name
