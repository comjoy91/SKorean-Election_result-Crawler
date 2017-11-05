#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from crawlers.townCode.base import *
from utils import sanitize, InvalidCrawlerError

def Crawler(nth, election_name):
	if 1 <= nth <= 17:
		crawler = LocalDivision_CodeCrawler_GuOld(int(nth), election_name)
	elif 18 <= nth <= 20:
		crawler = LocalDivision_CodeCrawler_Old(int(nth), election_name)
	elif nth == 21:
		raise InvalidCrawlerError('assembly', 'townCode', nth)
		#crawler = LocalDivision_CodeCrawler_Recent(int(nth), election_name)
	else:
		raise InvalidCrawlerError('assembly', 'townCode', nth)
	return crawler



class LocalDivision_CodeCrawler_GuOld(JSONCrawler):
	is_constituency = False
	# 여기서 크롤링된 데이터는 시군구 단위로 분류됨.
	# n:1~15 - 여기서 크롤링된 데이터가 지역구 단위로 분류되어, 같은 시군구에서도 갑/을로 분구된 것이 따로따로 표기됨. 단, 선거구가 합구된 곳은 시군구별로 다 명기됨.
	# n:16~17 - 여기서 크롤링된 데이터는 시군구 단위로 분류됨.

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_GuOld.json'
	param_city_codes_json = dict(electionId='0000000000')

	url_list_base = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeBySgJson_GuOld.json'
	param_url_list = dict(electionId='0000000000', subElectionCode=2)

	def __init__(self, nth, _election_name):
		self.nth = nth
		self.param_city_codes_json['electionCode'] = _election_name
		self.param_url_list['electionCode'] = _election_name

		self.consti_crawler = Constituency_CodeCrawler_GuOld(_election_name)
		self.consti_crawler.nth = nth



class LocalDivision_CodeCrawler_Old(JSONCrawler):
	# 여기서 크롤링된 데이터는 시군구 단위로 분류됨.
	is_constituency = False

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'
	param_city_codes_json = dict(electionId='0000000000', subElectionCode=2)

	url_list_base = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeBySgJson_Old.json'
	param_url_list = dict(electionId='0000000000', subElectionCode=2)

	def __init__(self, nth, _election_name):
		self.nth = nth
		self.param_city_codes_json['electionCode'] = _election_name
		self.param_url_list['electionCode'] = _election_name

		self.consti_crawler = Constituency_CodeCrawler_Old(_election_name)
		self.consti_crawler.nth = nth


class LocalDivision_CodeCrawler_Recent(JSONCrawler):
	# 여기서 크롤링된 데이터는 시군구 단위로 분류됨.
	is_constituency = False

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'
	param_city_codes_json = dict(electionCode=2)

	url_list_base = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeJson.json'
	param_url_list = dict(electionCode=2)

	def __init__(self, nth, _election_name):
		self.nth = nth
		self.consti_crawler = Constituency_CodeCrawler_Recent(_election_name)
		self.consti_crawler.nth = nth




class Constituency_CodeCrawler_GuOld(JSONCrawler):
	is_constituency = True
	# 여기서 크롤링된 데이터는 선거구 단위로 분류됨.
	# n:3~5 - 지역구 지역명 미명기. "XX도 제X선거구" 방식으로 표기. 그러나 시군구당 최소 1개 지역구를 배치하던 선거제도 특성상, LocalDivision_CodeCrawler_GuOld의 지역명이 곧 지역구의 지역명과 동일.
	# n:6~8 - 일부 지역에서 지역구 지역명 미명기. "XX도 제X선거구" 방식으로 표기.
	# n:9,10 - 지역구 지역명 미명기. "XX도 제X선거구" 방식으로 표기.
	# n:17 - 지역구 크롤링이 안되야...

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_GuOld.json'
	param_city_codes_json = dict(electionId='0000000000', subElectionCode=2)

	url_list_base = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getSggCityCodeJson_GuOld.json'
	param_url_list = dict(electionId='0000000000', electionCode=2)

	def __init__(self, _election_name):
		self.param_city_codes_json['electionCode'] = _election_name
		self.param_url_list['electionName'] = _election_name



class Constituency_CodeCrawler_Old(JSONCrawler):
	is_constituency = True
	# 여기서 크롤링된 데이터는 선거구 단위로 분류됨.

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'
	param_city_codes_json = dict(electionId='0000000000', subElectionCode=2)

	url_list_base = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getSggCityCodeJson_Old.json'
	param_url_list = dict(electionId='0000000000', electionCode=2)

	def __init__(self, _election_name):
		self.param_city_codes_json['electionCode'] = _election_name
		self.param_url_list['electionName'] = _election_name



class Constituency_CodeCrawler_Recent(JSONCrawler):
	is_constituency = True
	# 여기서 크롤링된 데이터는 선거구 단위로 분류됨.

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'
	param_city_codes_json = dict(electionCode=2)

	url_list_base = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getSggCityCodeJson.json'
	param_url_list = dict(electionCode=2)

	def __init__(self, _election_name):
		self.param_city_codes_json['electionId'] = _election_name
		self.param_url_list['electionId'] = _election_name
