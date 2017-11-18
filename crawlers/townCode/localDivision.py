#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from crawlers.townCode.base_provincePage import *
from utils import sanitize, InvalidCrawlerError

def Crawler(nth, election_name, electionType, target):

	if target == 'president':
		if nth == 1 or 8 <= nth <= 12:
			raise NotImplementedError('The %d-th presidential election(in %s) was held as indirect election: We cannot crawl the data.' % (int(nth), election_name))
		elif 1 <= nth <= 16:
			crawler = LocalDivision_CodeCrawler_GuOld(int(nth), election_name, electionType, target)
		elif 17 <= nth <= 18:
			crawler = LocalDivision_CodeCrawler_Old(int(nth), election_name, electionType, target)
		elif nth == 19:
			crawler = LocalDivision_CodeCrawler_Recent(int(nth), election_name, electionType, target)
		else:
			raise InvalidCrawlerError('townCode', nth, election_name, electionType, target)

	elif target == 'local_provincal_administration' or \
        target == 'local_municipal_administration':
		if 1 <= nth <= 3:
			crawler = LocalDivision_CodeCrawler_GuOld(int(nth), election_name, electionType, target)
		elif 4 <= nth <= 6:
			crawler = LocalDivision_CodeCrawler_Old(int(nth), election_name, electionType, target)
		elif nth == 7:
			raise InvalidCrawlerError('townCode', nth, election_name, electionType, target)
			#"최근선거"로 들어갈 때의 code: crawler = LocalDivision_CodeCrawler_Recent(int(nth), election_name, electionType, target)
		else:
			raise InvalidCrawlerError('townCode', nth, election_name, electionType, target)

	elif target == 'local_eduAdministration':
		if 1 <= nth <= 4:
			raise NotImplementedError('Educational Superintendent Election was not held in %s.' % election_name)
		elif 5 <= nth <= 6:
			crawler = LocalDivision_CodeCrawler_Old(int(nth), election_name, electionType, target)
		elif nth == 7:
			raise InvalidCrawlerError('townCode', nth, election_name, electionType, target)
			#"최근선거"로 들어갈 때의 code: crawler = LocalDivision_CodeCrawler_Recent(int(nth), election_name, electionType, target)
		else:
			raise InvalidCrawlerError('townCode', nth, election_name, electionType, target)

	else:
		raise InvalidCrawlerError('townCode', nth, election_name, target)

	return crawler



class LocalDivision_CodeCrawler_GuOld(JSONCrawler_province):

	def __init__(self, nth, _election_name, _election_type, _target):
		self.nth = nth
		self.target = _target
		self.elemType = 'local_division'
		# 여기서 크롤링된 데이터는 행정구역(시군구, 행정구 포함) 단위로 분류됨.

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_GuOld.json'
		self.urlParam_city_codes = dict(electionId='0000000000', electionCode=_election_name, subElectionCode=_election_type)

		self.urlPath_town_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeBySgJson_GuOld.json'
		self.urlParam_town_list = dict(electionId='0000000000', electionCode=_election_name, subElectionCode=_election_type)


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


class LocalDivision_CodeCrawler_Recent(JSONCrawler_province):

	def __init__(self, nth, _election_name, _election_type, _target):
		self.nth = nth
		self.target = _target
		self.elemType = 'local_division'
		# 여기서 크롤링된 데이터는 행정구역(시군구, 행정구 포함) 단위로 분류됨.

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'
		self.urlParam_city_codes = dict(electionCode=_election_type, electionId=_election_name)

		self.urlPath_town_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeJson.json'
		self.urlParam_town_list = dict(electionCode=_election_type, electionId=_election_name)
