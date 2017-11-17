#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from crawlers.electorates.base_provincePage import *
from utils import sanitize, InvalidCrawlerError

def Crawler(nth, election_name, localType_int, target):
	if nth == 1:
		raise NotImplementedError('Educational Parliament Election was not held in 1995.')
	elif nth == 2:
		raise NotImplementedError('Educational Parliament Election was not held in 1998.')
	elif nth == 3:
		raise NotImplementedError('Educational Parliament Election was not held in 2002.')
	elif 4 <= nth <= 6:
		crawler = Constituency_ElectorCrawler_Old(int(nth), election_name, localType_int, target)
	elif nth == 7:
		raise InvalidCrawlerError('townCode', nth, election_name, localType_int, target)
		#"최근선거"로 들어갈 때의 code: crawler = LocalDivision_ElectorCrawler_Recent(int(nth), election_name, localType_int, target)
	else:
		raise InvalidCrawlerError('townCode', nth, election_name, localType_int, target)
	return crawler




class Constituency_ElectorCrawler_Old(MultiCityCrawler_province):

	def __init__(self, nth, _election_name, _localType_int, _target):
		self.nth = nth
		self.localType_int = _localType_int
		self.target = _target
		self.elemType = 'constituency_in_province'
		self.isRecent = False
		# 여기서 크롤링된 데이터는 광역자치단체별 교육의원 지역 선거구 단위로 분류됨.

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'
		self.urlParam_city_codes = dict(electionId='0000000000', \
										electionCode=_election_name, subElectionCode =_localType_int)

		self.urlPath_sgg_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_sgg_list = dict(electionId='0000000000', electionName=_election_name,\
										requestURI='/WEB-INF/jsp/electioninfo/0000000000/bi/bipb02.jsp',\
										statementId='BIPB02_#3_10',\
										oldElectionType=1, electionType=4, electionCode=_localType_int,\
										searchType=3, townCode=-1, sggCityCode=-1)


class Constituency_ElectorCrawler_Recent(MultiCityCrawler_province):

	def __init__(self, nth, _election_name, _localType_int, _target):
		self.nth = nth
		self.localType_int = _localType_int
		self.target = _target
		self.elemType = 'constituency_in_province'
		self.isRecent = True
		# 여기서 크롤링된 데이터는 광역자치단체별 교육의원 지역 선거구 단위로 분류됨.

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'
		self.urlParam_city_codes = dict(electionCode=_localType_int)

		self.urlPath_town_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_town_list = dict(electionId=_election_name, statementId='BIPB02_#3_10',\
									requestURI='/WEB-INF/jsp/electioninfo/'+_election_name+'/bi/bipb02.jsp',
									electionCode=-1, searchType=3, townCode=-1)
