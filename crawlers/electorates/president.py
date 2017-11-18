#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from crawlers.electorates.base_provincePage import *
from utils import sanitize

def Crawler(nth, election_name, electionType, target):
	if nth == 1:
		raise NotImplementedError('The 1st presidential election(in 1948) was held in National Assembley: We cannot crawl the data.')
	elif 2 <= nth <= 7:
		raise NotImplementedError('Korean National Election Committee does not have any data about electorates in each local regions of the 2nd~7th / 13rd~15th presidential election.')
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
	elif 13 <= nth <= 15:
		raise NotImplementedError('Korean National Election Committee does not have any data about electorates in each local region of the 2nd~7th / 13rd~15th presidential election.')
	elif nth == 16:
		crawler = LocalDivision_ElectorCrawler_GuOld(int(nth), election_name, electionType, target)
	elif 17 <= nth <= 18:
		crawler = LocalDivision_ElectorCrawler_Old(int(nth), election_name, electionType, target)
	elif nth == 19:
		crawler = LocalDivision_ElectorCrawler_Recent(int(nth), election_name, electionType, target)
	else:
		raise InvalidCrawlerError('electorates', nth, election_name, electionType, target)
	return crawler



class LocalDivision_ElectorCrawler_GuOld(MultiCityCrawler_province):

#	def parse_tr_xhtml(self, consti, city_name=None):
#		consti = super(LocalDivision_ElectorCrawler_GuOld, self).parse_tr_xhtml(consti, city_name)
#		return consti

	def __init__(self, nth, _election_name, _target):
		self.nth = nth
		self.target = _target
		self.elemType = 'local_division'
		self.isRecent = False

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_GuOld.json'
		self.urlParam_city_codes = dict(electionId='0000000000', electionCode=_election_name)

		self.urlPath_town_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_town_list = dict(electionId='0000000000', electionName=_election_name,\
										requestURI='/WEB-INF/jsp/electioninfo/0000000000/bi/bipb02.jsp',\
										statementId='BIPB92_#1',\
										oldElectionType=1, electionType=_election_type, electionCode=-1,\
										searchType=2, townCode=-1, sggCityCode=-1)


class LocalDivision_ElectorCrawler_Old(MultiCityCrawler_province):

#	def parse_tr_xhtml(self, consti, city_name=None):
#		consti = super(LocalDivision_ElectorCrawler_Old, self).parse_tr_xhtml(consti, city_name)
#		return consti

	def __init__(self, nth, _election_name, _target):
		self.nth = nth
		self.target = _target
		self.elemType = 'local_division'
		self.isRecent = False

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'
		self.urlParam_city_codes = dict(electionId='0000000000', electionCode=_election_name,\
										subElectionCode=1)

		self.urlPath_town_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_town_list = dict(electionId='0000000000', electionName=_election_name,\
										requestURI='/WEB-INF/jsp/electioninfo/0000000000/bi/bipb02.jsp',\
										statementId='BIPB02_#2',\
										oldElectionType=1, electionType=_election_type, electionCode=-1,\
										searchType=2, townCode=-1, sggCityCode=-1)


class LocalDivision_ElectorCrawler_Recent(MultiCityCrawler_province):

#	def parse_tr_xhtml(self, consti, city_name=None):
#		consti = super(LocalDivision_ElectorCrawler_Recent, self).parse_tr_xhtml(consti, city_name)
#		return consti

	def __init__(self, nth, _election_name, _target):
		self.nth = nth
		self.target = _target
		self.election_name = _election_name
		self.elemType = 'local_division'
		self.isRecent = True

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'
		self.urlParam_city_codes = dict(electionCode=_election_type, electionId=_election_name)

		self.urlPath_town_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_town_list = dict(electionId=_election_name, statementId='BIPB02_#2',\
									requestURI='/WEB-INF/jsp/electioninfo/'+_election_name+'/bi/bipb02.jsp',
									electionCode=-1, searchType=2, townCode=-1)
