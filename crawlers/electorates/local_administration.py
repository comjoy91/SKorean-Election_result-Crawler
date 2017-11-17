#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from crawlers.electorates.base_provincePage import *
from utils import sanitize, InvalidCrawlerError

def Crawler(nth, election_name, localType_int, target):
	if target == 'local_eduAdministration':
		if nth == 1:
			raise NotImplementedError('Educational Superintendent Election was not held in 1995.')
		elif nth == 2:
			raise NotImplementedError('Educational Superintendent Election was not held in 1998.')
		elif nth == 3:
			raise NotImplementedError('Educational Superintendent Election was not held in 2002.')
		elif nth == 4:
			raise NotImplementedError('Educational Superintendent Election was not held in 2006.')
	if 1 <= nth <= 3:
		crawler = Elector_Crawler_GuOld(int(nth), election_name, localType_int, target)
	elif 4 <= nth <= 6:
		crawler = Elector_Crawler_Old(int(nth), election_name, localType_int, target)
	elif nth == 7:
		raise InvalidCrawlerError('townCode', nth, election_name, localType_int, target)
		#"최근선거"로 들어갈 때의 code: crawler = Elector_Crawler_Recent(int(nth), election_name, localType_int, target)
	else:
		raise InvalidCrawlerError('townCode', nth, election_name, localType_int, target)
	return crawler



class LocalDivision_ElectorCrawler_GuOld(MultiCityCrawler_province):

	def __init__(self, nth, _election_name, _localType_int, _target):
		self.nth = nth
		self.localType_int = _localType_int
		self.target = _target
		self.elemType = 'local_division'
		self.isRecent = False
		# 여기서 크롤링된 데이터는 행정구역(시군구, 행정구 포함) 단위로 분류됨.
		# n:1~2 - 여기서 크롤링된 데이터가 국회의원 지역구 단위로 분류되어, 같은 시군구에서도 갑/을로 분구된 것이 따로따로 표기됨. 단, 선거구가 합구된 곳은 시군구별로 다 명기됨.
		# n:3 - 여기서 크롤링된 데이터는 시군구 단위로 분류됨.

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_GuOld.json'
		self.urlParam_city_codes = dict(electionId='0000000000', \
										electionCode=_election_name, subElectionCode =_localType_int)

		self.urlPath_town_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_town_list = dict(electionId='0000000000', electionName=_election_name,\
									requestURI='/WEB-INF/jsp/electioninfo/0000000000/bi/bipb02.jsp',\
									statementId='BIPB92_#1',\
									oldElectionType=1, electionType=4, electionCode=-1,\
									searchType=2, townCode=-1, sggCityCode=-1)


class LocalDivision_ElectorCrawler_Old(MultiCityCrawler_province):

	def __init__(self, nth, _election_name, _localType_int, _target):
		self.nth = nth
		self.localType_int = _localType_int
		self.target = _target
		self.elemType = 'local_division'
		self.isRecent = False
		# 여기서 크롤링된 데이터는 행정구역(시군구, 행정구 포함) 단위로 분류됨.

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'
		self.urlParam_city_codes = dict(electionId='0000000000', \
										electionCode=_election_name, subElectionCode =_localType_int)

		self.urlPath_town_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_town_list = dict(electionId='0000000000', electionName=_election_name,\
									requestURI='/WEB-INF/jsp/electioninfo/0000000000/bi/bipb02.jsp',\
									statementId='BIPB02_#2',\
									oldElectionType=1, electionType=4, electionCode=-1,\
									searchType=2, townCode=-1, sggCityCode=-1)


class LocalDivision_ElectorCrawler_Recent(MultiCityCrawler_province):

	def __init__(self, nth, _election_name, _localType_int, _target):
		self.nth = nth
		self.localType_int = _localType_int
		self.target = _target
		self.elemType = 'local_division'
		self.isRecent = True
		# 여기서 크롤링된 데이터는 행정구역(시군구, 행정구 포함) 단위로 분류됨.

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'
		self.urlParam_city_codes = dict(electionId=_election_name, electionCode=_localType_int)

		self.urlPath_town_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_town_list = dict(electionId=_election_name, statementId='BIPB02_#2',\
									requestURI='/WEB-INF/jsp/electioninfo/'+_election_name+'/bi/bipb02.jsp',
									electionCode=-1, searchType=2, townCode=-1)
