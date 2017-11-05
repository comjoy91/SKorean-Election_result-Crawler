#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from crawlers.townCode.base import *
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



class LocalDivision_CodeCrawler_GuOld(JSONCrawler):
	is_constituency = False
	# 여기서 크롤링된 데이터는 시군구 단위로 분류됨.

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_GuOld.json'
	param_city_codes_json = dict(electionId='0000000000')

	url_list_base = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeBySgJson_GuOld.json'
	param_url_list = dict(electionId='0000000000', subElectionCode=1)

	def __init__(self, nth, _election_name):
		self.nth = nth
		self.param_city_codes_json['electionCode'] = _election_name
		self.param_url_list['electionCode'] = _election_name


class LocalDivision_CodeCrawler_Old(JSONCrawler):
	# 여기서 크롤링된 데이터는 시군구 단위로 분류됨.
	is_constituency = False

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'
	param_city_codes_json = dict(electionId='0000000000', subElectionCode=1)

	url_list_base = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeBySgJson_Old.json'
	param_url_list = dict(electionId='0000000000', subElectionCode=1)

	def __init__(self, nth, _election_name):
		self.nth = nth
		self.param_city_codes_json['electionCode'] = _election_name
		self.param_url_list['electionCode'] = _election_name



class LocalDivision_CodeCrawler_Recent(JSONCrawler):
	# 여기서 크롤링된 데이터는 시군구 단위로 분류됨.
	is_constituency = False

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'
	param_city_codes_json = dict(electionCode=1)

	url_list_base = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeJson.json'
	param_url_list = dict(electionCode=1)

	def __init__(self, nth, _election_name):
		self.nth = nth
		self.param_city_codes_json['electionId'] = _election_name
		self.param_url_list['electionId'] = _election_name
