#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from crawlers.townCode.base_provincePage import *
from utils import sanitize, InvalidCrawlerError

def Crawler(nth, election_name, electionType, target):
	if target == 'assembly':
		if 1 <= nth <= 17:
			crawler = LocalDivision_CodeCrawler_GuOld(int(nth), election_name, electionType, target)
		elif 18 <= nth <= 20:
			crawler = LocalDivision_CodeCrawler_Old(int(nth), election_name, electionType, target)
		elif nth == 21:
			raise InvalidCrawlerError('townCode', nth, election_name, electionType, target)
			#"최근선거"로 들어갈 때의 code: crawler = LocalDivision_CodeCrawler_Recent(int(nth), election_name, electionType, target)
		else:
			raise InvalidCrawlerError('townCode', nth, election_name, electionType, target)

	elif target == 'local-ep':
		if 1 <= nth <= 3:
			raise NotImplementedError('Educational Parliament Election was not held in %s.' % election_name)
		elif 4 <= nth <= 6:
			crawler = LocalDivision_CodeCrawler_Old(int(nth), election_name, electionType, target)
		elif nth == 7:
			raise InvalidCrawlerError('townCode', nth, election_name, electionType, target)
			#"최근선거"로 들어갈 때의 code: crawler = LocalDivision_CodeCrawler_Recent(int(nth), election_name, electionType, target)
		else:
			raise InvalidCrawlerError('townCode', nth, election_name, electionType, target)
	else:
		raise InvalidCrawlerError('townCode', nth, election_name, electionType, target)

	return crawler



class LocalDivision_CodeCrawler_GuOld(JSONCrawler_province):

	def __init__(self, nth, _election_name, _election_type, _target):
		self.nth = nth
		self.target = _target
		self.elemType = 'local_division'
		# 여기서 크롤링된 데이터는 행정구역(시군구, 행정구 포함) 단위로 분류됨.
		# assembly, n:1~15 - 여기서 크롤링된 데이터가 지역구 단위로 분류되어, 같은 시군구에서도 갑/을로 분구된 것이 따로따로 표기됨. 단, 선거구가 합구된 곳은 시군구별로 다 명기됨.
		# assembly, n:16~17 - 여기서 크롤링된 데이터는 시군구 단위로 분류됨.

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_GuOld.json'
		self.urlParam_city_codes = dict(electionId='0000000000', electionCode=_election_name)

		self.urlPath_town_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeBySgJson_GuOld.json'
		self.urlParam_town_list = dict(electionId='0000000000', electionCode=_election_name, subElectionCode=_election_type)

		if nth == 17: # n:17 - 이것만 지역구 크롤링을 GuOld가 아니라 그냥 Old에서 진행.
			self.next_crawler = Constituency_CodeCrawler_Old(nth, _election_name, _election_type, _target)
		else:
			self.next_crawler = Constituency_CodeCrawler_GuOld(nth, _election_name, _election_type, _target)



class LocalDivision_CodeCrawler_Old(JSONCrawler_province):

	def __init__(self, nth, _election_name, _election_type, _target):
		self.nth = nth
		self.target = _target
		self.elemType = 'local_division'
		# 여기서 크롤링된 데이터는 행정구역(시군구, 행정구 포함) 단위로 분류됨.

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'
		self.urlParam_city_codes = dict(electionId='0000000000', electionCode=_election_name, subElectionCode=_election_type)

		self.urlPath_town_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeBySgJson_Old.json'
		self.urlParam_town_list = dict(electionId='0000000000', electionCode=_election_name, subElectionCode=_election_type)

		self.next_crawler = Constituency_CodeCrawler_Old(nth, _election_name, _election_type, _target)


class LocalDivision_CodeCrawler_Recent(JSONCrawler_province):

	def __init__(self, nth, _election_name, _election_type, _target):
		self.nth = nth
		self.target = _target
		self.elemType = 'local_division'
		# 여기서 크롤링된 데이터는 행정구역(시군구, 행정구 포함) 단위로 분류됨.

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'
		self.urlParam_city_codes = dict(electionCode=_election_type)

		self.urlPath_town_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeJson.json'
		self.urlParam_town_list = dict(electionCode=_election_type)

		self.next_crawler = Constituency_CodeCrawler_Recent(nth, _election_name, _election_type, _target)




class Constituency_CodeCrawler_GuOld(JSONCrawler_province):

	def __init__(self, nth, _election_name, _election_type, _target):
		self.nth = nth
		self.target = _target
		self.elemType = 'constituency_in_province'
		# 여기서 크롤링된 데이터는 국회의원 지역 선거구 단위로 분류됨.
		# assembly, n:3~5 - 지역구 지역명 미명기. "XX도 제X선거구" 방식으로 표기. 그러나 시군구당 최소 1개 지역구를 배치하던 선거제도 특성상, LocalDivision_CodeCrawler_GuOld의 지역명이 곧 지역구의 지역명과 동일.
		# assembly, n:6~8 - 일부 지역에서 지역구 지역명 미명기. "XX도 제X선거구" 방식으로 표기.
		# assembly, n:9,10 - 지역구 지역명 미명기. "XX도 제X선거구" 방식으로 표기.
		# assembly, n:17 - 이것만 지역구 크롤링을 GuOld가 아니라 그냥 Old에서 진행.

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_GuOld.json'
		self.urlParam_city_codes = dict(electionId='0000000000', electionCode=_election_name, subElectionCode=_election_type)

		self.urlPath_sgg_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getSggCityCodeJson_GuOld.json'
		self.urlParam_sgg_list = dict(electionId='0000000000', electionName=_election_name, electionCode=_election_type)



class Constituency_CodeCrawler_Old(JSONCrawler_province):

	def __init__(self, nth, _election_name, _election_type, _target):
		self.nth = nth
		self.target = _target
		self.elemType = 'constituency_in_province'
		# 여기서 크롤링된 데이터는 국회의원 지역 선거구 단위로 분류됨.

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'
		self.urlParam_city_codes = dict(electionId='0000000000', electionCode=_election_name, subElectionCode=_election_type)

		self.urlPath_sgg_list  = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getSggCityCodeJson_Old.json'
		self.urlParam_sgg_list = dict(electionId='0000000000', electionName=_election_name, electionCode=_election_type)



class Constituency_CodeCrawler_Recent(JSONCrawler_province):

	def __init__(self, nth, _election_name, _election_type, _target):
		self.nth = nth
		self.target = _target
		self.elemType = 'constituency_in_province'
		# 여기서 크롤링된 데이터는 국회의원 지역 선거구 단위로 분류됨.

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'
		self.urlParam_city_codes = dict(electionCode=_election_type, electionId=_election_name)

		self.urlPath_sgg_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getSggCityCodeJson.json'
		self.urlParam_sgg_list = dict(electionCode=_election_type, electionId=_election_name)
