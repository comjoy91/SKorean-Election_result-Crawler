#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from crawlers.electorates.base_provincePage import *
from crawlers.electorates.base_municipalPage import *
from utils import sanitize, InvalidCrawlerError

def Crawler(nth, election_name, electionType, target):
	if 1 <= nth <= 3:
		raise NotImplementedError('Korean National Election Committee does not have any data about electorates in each constituencies of the 1st~3rd local election.')
		# 지역구별 선거인수가 나오지 않고, 기초자치단체별 선거인수만 나옴.
		# 선거인수를 받기 위해서는, 결국 개표 결과에 나오는 선거인수를 받아야 함.
	elif 4 <= nth <= 6:
		crawler = Constituency_CodeCrawler_Old(int(nth), election_name, electionType, target)
	elif nth == 7:
		raise InvalidCrawlerError('townCode', nth, election_name, electionType, target)
		#"최근선거"로 들어갈 때의 code: crawler = LocalDivision_CodeCrawler_Recent(int(nth), election_name, electionType, target)
	else:
		raise InvalidCrawlerError('townCode', nth, election_name, electionType, target)
	return crawler



class Constituency_CodeCrawler_GuOld(MultiCityCrawler_municipal):

	def __init__(self, nth, _election_name, _election_type, _target):
		self.nth = nth
		self.target = _target
		self.elemType = 'constituency_in_municipal_division'
		self.isRecent = False
		# 여기서 크롤링된 데이터는 광역/기초자치의회 지역 선거구 단위로 분류됨.

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_GuOld.json'
		self.urlParam_city_codes = dict(electionId='0000000000', \
										electionCode=_election_name, subElectionCode =_election_type)

		self.urlPath_town_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeBySgJson_GuOld.json'
		self.urlParam_town_codes = dict(electionId='0000000000', \
										electionCode=_election_name, subElectionCode =_election_type)

		self.urlPath_sgg_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_sgg_list = dict(electionId='0000000000', electionName=_election_name,\
										requestURI='/WEB-INF/jsp/electioninfo/0000000000/bi/bipb02.jsp',\
										statementId='BIPB92_#1',\
										oldElectionType=1, electionType=4, electionCode=_election_type,\
										searchType=2, townCode=-1, sggCityCode=-1)

		if _target == 'local-pp' and nth >= 3:
			self.next_crawler = LocalDivision_CodeCrawler_GuOld(nth, _election_name, _election_type, _target)



class Constituency_CodeCrawler_Old(MultiCityCrawler_municipal):

	def __init__(self, nth, _election_name, _election_type, _target):
		self.nth = nth
		self.target = _target
		self.elemType = 'constituency_in_municipal_division'
		self.isRecent = False
		# 여기서 크롤링된 데이터는 국회의원 지역 선거구 단위로 분류됨.

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'
		self.urlParam_city_codes = dict(electionId='0000000000', \
										electionCode=_election_name, subElectionCode =_election_type)

		self.urlPath_town_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeBySgJson_Old.json'
		self.urlParam_town_codes = dict(electionId='0000000000', \
										electionCode=_election_name, subElectionCode =_election_type)

		self.urlPath_sgg_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_sgg_list = dict(electionId='0000000000', electionName=_election_name,\
										requestURI='/WEB-INF/jsp/electioninfo/0000000000/bi/bipb02.jsp',\
										oldElectionType=1, electionType=4, electionCode=_election_type,\
										searchType=3, sggCityCode=-1)
		if _target == 'local-pp':
			self.urlParam_sgg_list['statementId'] = 'BIPB02_#3_5'
		else: #_target == 'local-mp'
			self.urlParam_sgg_list['statementId'] = 'BIPB02_#3_6'

		self.next_crawler = LocalDivision_CodeCrawler_Old(nth, _election_name, _election_type, _target)


class Constituency_CodeCrawler_Recent(MultiCityCrawler_municipal):

	def __init__(self, nth, _election_name, _election_type, _target):
		self.nth = nth
		self.target = _target
		self.elemType = 'constituency_in_municipal_division'
		self.isRecent = True
		# 여기서 크롤링된 데이터는 국회의원 지역 선거구 단위로 분류됨.

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'
		self.urlParam_city_codes = dict(electionCode=_election_type)

		self.urlPath_town_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeBySgJson.json'
		self.urlParam_town_codes = dict(electionCode=_election_type)

# TODO: 이것은 선거 전에 반드시 수정해야 함.
		self.urlPath_sgg_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_town_list = dict(electionId=_election_name,\
									requestURI='/WEB-INF/jsp/electioninfo/'+_election_name+'/bi/bipb02.jsp',
									electionCode=_election_type, searchType=3)

		if _target == 'local-pp':
			self.urlParam_sgg_list['statementId'] = 'BIPB02_#3_5'
		else: #_target == 'local-mp'
			self.urlParam_sgg_list['statementId'] = 'BIPB02_#3_6'

		self.next_crawler = LocalDivision_CodeCrawler_Recent(nth, _election_name, _election_type, _target)



class LocalDivision_CodeCrawler_GuOld(MultiCityCrawler_province):

	def __init__(self, nth, _election_name, _election_type, _target):
		self.nth = nth
		self.target = _target
		self.elemType = 'local_division'
		self.isRecent = False
		# 여기서 크롤링된 데이터는 행정구역(시군구, 행정구 포함) 단위로 분류됨.
		# n:1~2 - 여기서 크롤링된 데이터가 국회의원 지역구 단위로 분류되어, 같은 시군구에서도 갑/을로 분구된 것이 따로따로 표기됨. 단, 선거구가 합구된 곳은 시군구별로 다 명기됨.
		# n:3 - 여기서 크롤링된 데이터는 시군구 단위로 분류됨.

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_GuOld.json'
		self.urlParam_city_codes = dict(electionId='0000000000', \
										electionCode=_election_name, subElectionCode =_election_type)

		self.urlPath_town_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_town_list = dict(electionId='0000000000', electionName=_election_name,\
									requestURI='/WEB-INF/jsp/electioninfo/0000000000/bi/bipb02.jsp',\
									statementId='BIPB92_#1',\
									oldElectionType=1, electionType=4, electionCode=-1,\
									searchType=2, townCode=-1, sggCityCode=-1)


class LocalDivision_CodeCrawler_Old(MultiCityCrawler_province):

	def __init__(self, nth, _election_name, _election_type, _target):
		self.nth = nth
		self.target = _target
		self.elemType = 'local_division'
		self.isRecent = False
		# 여기서 크롤링된 데이터는 행정구역(시군구, 행정구 포함) 단위로 분류됨.

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'
		self.urlParam_city_codes = dict(electionId='0000000000', \
										electionCode=_election_name, subElectionCode =_election_type)

		self.urlPath_town_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_town_list = dict(electionId='0000000000', electionName=_election_name,\
									requestURI='/WEB-INF/jsp/electioninfo/0000000000/bi/bipb02.jsp',\
									statementId='BIPB02_#2',\
									oldElectionType=1, electionType=4, electionCode=-1,\
									searchType=2, townCode=-1, sggCityCode=-1)


class LocalDivision_CodeCrawler_Recent(MultiCityCrawler_province):

	def __init__(self, nth, _election_name, _election_type, _target):
		self.nth = nth
		self.target = _target
		self.elemType = 'local_division'
		self.isRecent = True
		# 여기서 크롤링된 데이터는 행정구역(시군구, 행정구 포함) 단위로 분류됨.

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'
		self.urlParam_city_codes = dict(electionCode=_election_type)

		self.urlPath_town_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_town_list = dict(electionId=_election_name, statementId='BIPB02_#2',\
									requestURI='/WEB-INF/jsp/electioninfo/'+_election_name+'/bi/bipb02.jsp',
									electionCode=-1, searchType=2, townCode=-1)
