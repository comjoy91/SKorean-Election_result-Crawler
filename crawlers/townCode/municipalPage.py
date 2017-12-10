#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from crawlers.townCode.base_municipalPage import *
from utils import sanitize, InvalidCrawlerError

def Crawler(nth, election_name, electionType, target, target_eng, target_kor):
	if target == 'local-pp' :
		if 1 <= nth <= 3:
			crawler = Province_townCodeCrawler_GuOld(int(nth), election_name, electionType)
			if nth == 3:
				crawler.urlParam_PR_sgg_list = dict(electionId='0000000000', electionName=election_name, electionCode=7)
				crawler.urlParam_PR_elector_list = dict(electionId='0000000000', electionName=election_name,\
														requestURI='/WEB-INF/jsp/electioninfo/0000000000/ep/epei01.jsp',\
														statementId='EPEI01_#91',\
														oldElectionType=0, electionType=2, electionCode=8,\
														townCode=-1)
		elif 4 <= nth <= 6:
			crawler = Province_townCodeCrawler_Old(int(nth), election_name, electionType)
			crawler.urlParam_PR_sgg_list = dict(electionId='0000000000', electionName=election_name, electionCode=8)
			crawler.urlParam_PR_elector_list = dict(electionId='0000000000', electionName=election_name,\
													requestURI='/WEB-INF/jsp/electioninfo/0000000000/ep/epei01.jsp',\
													statementId='EPEI01_#1',\
													oldElectionType=1, electionType=2, electionCode=8,\
													townCode=-1)
		elif nth == 7:
			raise InvalidCrawlerError('townCode', nth, election_name, electionType)
			#"최근선거"로 들어갈 때의 code: crawler = Province_townCodeCrawler_Recent(int(nth), election_name, electionType)
		else:
			raise InvalidCrawlerError('townCode', nth, election_name, electionType)


	elif target == 'local-mp' :
		if 1 <= nth <= 3:
			crawler = Province_townCodeCrawler_GuOld(int(nth), election_name, electionType)
		elif 4 <= nth <= 6:
			crawler = Province_townCodeCrawler_Old(int(nth), election_name, electionType)
			crawler.urlParam_PR_sgg_list = dict(electionId='0000000000', electionName=election_name, electionCode=9)
			crawler.urlParam_PR_elector_list = dict(electionId='0000000000', electionName=election_name,\
													requestURI='/WEB-INF/jsp/electioninfo/0000000000/ep/epei01.jsp',\
													statementId='EPEI01_#1',\
													oldElectionType=1, electionType=2, electionCode=9,\
													townCode=-1)
	crawler.nth = nth
	crawler.target = target
	crawler.target_eng = target_eng
	crawler.target_kor = target_kor

	return crawler



class Province_townCodeCrawler_GuOld(JSONCrawler_municipal):

	def __init__(self, nth, _election_name, _election_type):
		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_GuOld.json'
		self.urlParam_city_codes = dict(electionId='0000000000', electionCode=_election_name, subElectionCode=_election_type)

		# 여기서 크롤링된 데이터는 행정구역(시군구, 행정구 포함) 단위로 분류됨.
		self.urlPath_town_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeBySgJson_GuOld.json'
		self.urlParam_town_list = dict(electionId='0000000000', electionCode=_election_name, subElectionCode=_election_type)

		# 여기서 크롤링된 데이터는 선거구 단위로 분류됨.
		self.urlPath_sgg_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getSggCityCodeJson_GuOld.json'
		self.urlParam_sgg_list = dict(electionId='0000000000', electionName=_election_name, electionCode=_election_type)

		# 여기서 크롤링된 데이터는 선거구 단위로 분류됨.
		self.urlPath_sggTown_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getSggTownCodeJson_GuOld.json'
		self.urlParam_sggTown_list = dict(electionId='0000000000', electionName=_election_name, electionCode=_election_type)

		self.urlPath_elector_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_elector_list = dict(electionId='0000000000', electionName=_election_name,\
										requestURI='/WEB-INF/jsp/electioninfo/0000000000/ep/epei01.jsp',\
										statementId='EPEI01_#91',\
										oldElectionType=0, electionType=2, electionCode=_election_type,\
										townCode=-1)


class Province_townCodeCrawler_Old(JSONCrawler_municipal):

	def __init__(self, nth, _election_name, _election_type):
		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'
		self.urlParam_city_codes = dict(electionId='0000000000', electionCode=_election_name, subElectionCode=_election_type)

		# 여기서 크롤링된 데이터는 행정구역(시군구, 행정구 포함) 단위로 분류됨.
		self.urlPath_town_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeBySgJson_Old.json'
		self.urlParam_town_list = dict(electionId='0000000000', electionCode=_election_name, subElectionCode=_election_type)

		# 여기서 크롤링된 데이터는 선거구 단위로 분류됨.
		self.urlPath_sgg_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getSggCityCodeJson_Old.json'
		self.urlParam_sgg_list = dict(electionId='0000000000', electionName=_election_name, electionCode=_election_type)

		# 여기서 크롤링된 데이터는 선거구 단위로 분류됨.
		self.urlPath_sggTown_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getSggTownCodeJson_Old.json'
		self.urlParam_sggTown_list = dict(electionId='0000000000', electionName=_election_name, electionCode=_election_type)

		self.urlPath_elector_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_elector_list = dict(electionId='0000000000', electionName=_election_name,\
										requestURI='/WEB-INF/jsp/electioninfo/0000000000/ep/epei01.jsp',\
										statementId='EPEI01_#1',\
										oldElectionType=1, electionType=2, electionCode=_election_type,\
										townCode=-1)


class Province_townCodeCrawler_Recent(JSONCrawler_municipal):

	def __init__(self, nth, _election_name, _election_type):
		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'
		self.urlParam_city_codes = dict(electionId=_election_name, electionCode=_election_type)

		# 여기서 크롤링된 데이터는 행정구역(시군구, 행정구 포함) 단위로 분류됨.
		self.urlPath_town_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeJson.json'
		self.urlParam_town_list = dict(electionId=_election_name, electionCode=_election_type)

		# 여기서 크롤링된 데이터는 선거구 단위로 분류됨.
		self.urlPath_sgg_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getSggCityCodeJson.json'
		self.urlParam_sgg_list = dict(electionId=_election_name, electionCode=_election_type)

		# 여기서 크롤링된 데이터는 선거구 단위로 분류됨.
		self.urlPath_sggTown_list = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getSggTownCodeJson_GuOld.json'
		self.urlParam_sggTown_list = dict(electionId=_election_name, electionCode=_election_type)
