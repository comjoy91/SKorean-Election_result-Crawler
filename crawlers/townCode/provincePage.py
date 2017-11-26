#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from crawlers.townCode.base_provincePage import *
from utils import sanitize, InvalidCrawlerError

def Crawler(nth, election_name, electionType, target, target_eng, target_kor):

	if target == 'president':
		if nth == 1 or 8 <= nth <= 12:
			raise NotImplementedError('The %d-th presidential election(in %s) was held as indirect election: We cannot crawl the data.' % (int(nth), election_name))
		elif 1 <= nth <= 16:
			crawler = Province_townCodeCrawler_GuOld(int(nth), election_name, electionType)
		elif 17 <= nth <= 18:
			crawler = Province_townCodeCrawler_Old(int(nth), election_name, electionType)
		elif nth == 19:
			crawler = Province_townCodeCrawler_Recent(int(nth), election_name, electionType)
		else:
			raise InvalidCrawlerError('townCode', nth, election_name, electionType)

	elif target == 'local-pa' or \
		target == 'local-ma' or \
		target == 'local-pp' or \
        target == 'local-mp' :
		if 1 <= nth <= 3:
			crawler = Province_townCodeCrawler_GuOld(int(nth), election_name, electionType)
		elif 4 <= nth <= 6:
			crawler = Province_townCodeCrawler_Old(int(nth), election_name, electionType)
		elif nth == 7:
			raise InvalidCrawlerError('townCode', nth, election_name, electionType)
			#"최근선거"로 들어갈 때의 code: crawler = Province_townCodeCrawler_Recent(int(nth), election_name, electionType)
		else:
			raise InvalidCrawlerError('townCode', nth, election_name, electionType)

	elif target == 'local-ea':
		if 1 <= nth <= 4:
			raise NotImplementedError('Educational Superintendent Election was not held in %s.' % election_name)
		elif 5 <= nth <= 6:
			crawler = Province_townCodeCrawler_Old(int(nth), election_name, electionType)
		elif nth == 7:
			raise InvalidCrawlerError('townCode', nth, election_name, electionType)
			#"최근선거"로 들어갈 때의 code: crawler = Province_townCodeCrawler_Recent(int(nth), election_name, electionType)
		else:
			raise InvalidCrawlerError('townCode', nth, election_name, electionType)

	elif target == 'assembly':
		if 1 <= nth <= 17:
			# assembly, n:1~15 - 여기서 행정구역이 선거구 단위로 분류되어, 같은 시군구에서도 갑/을로 분구된 것이 따로따로 표기됨. 단, 선거구가 합구된 곳은 시군구별로 다 명기됨.
			# assembly, n:3~5 - 지역구 지역명 미명기. "XX도 제X선거구" 방식으로 표기. 그러나 시군구당 최소 1개 지역구를 배치하던 선거제도 특성상, 행정구역명이 곧 지역구의 지역명과 동일.
			# assembly, n:6~8 - 일부 지역에서 지역구 지역명 미명기. "XX도 제X선거구" 방식으로 표기.
			# assembly, n:9,10 - 지역구 지역명 미명기. "XX도 제X선거구" 방식으로 표기.
			crawler = Province_townCodeCrawler_GuOld(int(nth), election_name, electionType)
			if nth==17:
				crawler.urlPath_sgg_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getSggCityCodeJson_Old.json'
		elif 18 <= nth <= 20:
			crawler = Province_townCodeCrawler_Old(int(nth), election_name, electionType)
		#if 1 <= nth <= 20:
		#	crawler = Province_townCodeCrawler_Old(int(nth), election_name, electionType)
		elif nth == 21:
			raise InvalidCrawlerError('townCode', nth, election_name, electionType)
			#"최근선거"로 들어갈 때의 code: crawler = Province_townCodeCrawler_Recent(int(nth), election_name, electionType)
		else:
			raise InvalidCrawlerError('townCode', nth, election_name, electionType)

	elif target == 'local-ep':
		if 1 <= nth <= 3:
			raise NotImplementedError('Educational Parliament Election was not held in %s.' % election_name)
		elif 4 <= nth <= 6:
			crawler = Province_townCodeCrawler_Old(int(nth), election_name, electionType)
		elif nth == 7:
			raise InvalidCrawlerError('townCode', nth, election_name, electionType)
			#"최근선거"로 들어갈 때의 code: crawler = Province_townCodeCrawler_Recent(int(nth), election_name, electionType)
		else:
			raise InvalidCrawlerError('townCode', nth, election_name, electionType)

	else:
		raise InvalidCrawlerError('townCode', nth, election_name, electionType)

	crawler.nth = nth
	crawler.target = target
	crawler.target_eng = target_eng
	crawler.target_kor = target_kor

	return crawler



class Province_townCodeCrawler_GuOld(JSONCrawler_province):

	def __init__(self, nth, _election_name, _election_type):
		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_GuOld.json'
		self.urlParam_city_codes = dict(electionId='0000000000', electionCode=_election_name, subElectionCode=_election_type)

		# 여기서 크롤링된 데이터는 행정구역(시군구, 행정구 포함) 단위로 분류됨.
		self.urlPath_town_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeBySgJson_GuOld.json'
		self.urlParam_town_list = dict(electionId='0000000000', electionCode=_election_name, subElectionCode=_election_type)

		# 여기서 크롤링된 데이터는 선거구 단위로 분류됨.
		self.urlPath_sgg_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getSggCityCodeJson_GuOld.json'
		self.urlParam_sgg_list = dict(electionId='0000000000', electionName=_election_name, electionCode=_election_type)


class Province_townCodeCrawler_Old(JSONCrawler_province):

	def __init__(self, nth, _election_name, _election_type):
		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'
		self.urlParam_city_codes = dict(electionId='0000000000', electionCode=_election_name, subElectionCode=_election_type)

		# 여기서 크롤링된 데이터는 행정구역(시군구, 행정구 포함) 단위로 분류됨.
		self.urlPath_town_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeBySgJson_Old.json'
		self.urlParam_town_list = dict(electionId='0000000000', electionCode=_election_name, subElectionCode=_election_type)

		# 여기서 크롤링된 데이터는 선거구 단위로 분류됨.
		self.urlPath_sgg_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getSggCityCodeJson_Old.json'
		self.urlParam_sgg_list = dict(electionId='0000000000', electionName=_election_name, electionCode=_election_type)


class Province_townCodeCrawler_Recent(JSONCrawler_province):

	def __init__(self, nth, _election_name, _election_type):
		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'
		self.urlParam_city_codes = dict(electionId=_election_name, electionCode=_election_type)

		# 여기서 크롤링된 데이터는 행정구역(시군구, 행정구 포함) 단위로 분류됨.
		self.urlPath_town_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeJson.json'
		self.urlParam_town_list = dict(electionId=_election_name, electionCode=_election_type)

		# 여기서 크롤링된 데이터는 선거구 단위로 분류됨.
		self.urlPath_sgg_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getSggCityCodeJson.json'
		self.urlParam_sgg_list = dict(electionId=_election_name, electionCode=_election_type)
