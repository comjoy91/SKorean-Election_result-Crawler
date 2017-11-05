#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from crawlers.electorates.base import *
from utils import sanitize

def Crawler(nth, _election_name):
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
		crawler = ElectorCrawler_GuOld(int(nth), _election_name)
	elif 17 <= nth <= 18:
		crawler = ElectorCrawler_Old(int(nth), _election_name)
	elif nth == 19:
		crawler = ElectorCrawler_Recent(int(nth), _election_name)
	else:
		raise InvalidCrawlerError('president', 'electorates', nth)
	return crawler



class ElectorCrawler_GuOld(MultiCityCrawler):
	is_constituency = False

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_GuOld.json'
	param_city_codes_json = dict(electionId='0000000000')

	url_list_base = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
	param_url_list = dict(electionId='0000000000',\
							requestURI='/WEB-INF/jsp/electioninfo/0000000000/bi/bipb02.jsp',\
							statementId='BIPB92_#1',\
							oldElectionType=0, electionType=1, electionCode=-1,\
							searchType=2, townCode=-1, sggCityCode=-1)

	def parse_consti(self, consti, city_name=None):
		consti = super(ElectorCrawler_GuOld, self).parse_consti(consti, city_name)
		return consti

	def __init__(self, nth, _election_name):
		self.nth = nth
		self.param_city_codes_json['electionCode'] = _election_name
		self.param_url_list['electionName'] = _election_name


class ElectorCrawler_Old(MultiCityCrawler):
	is_constituency = False

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'
	param_city_codes_json = dict(electionId='0000000000',\
									subElectionCode=1)

	url_list_base = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
	param_url_list = dict(electionId='0000000000',\
							requestURI='/WEB-INF/jsp/electioninfo/0000000000/bi/bipb02.jsp',\
							statementId='BIPB02_#2',\
							oldElectionType=1, electionType=1, electionCode=-1,\
							searchType=2, townCode=-1, sggCityCode=-1)

	def parse_consti(self, consti, city_name=None):
		consti = super(ElectorCrawler_Old, self).parse_consti(consti, city_name)
		return consti

	def __init__(self, nth, _election_name):
		self.nth = nth
		self.param_city_codes_json['electionCode'] = _election_name
		self.param_url_list['electionName'] = _election_name


class ElectorCrawler_Recent(MultiCityCrawler):
	is_constituency = False
	election_name = ''

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'
	param_city_codes_json = dict(electionCode=1)

	url_list_base = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
	param_url_list = dict(statementId='BIPB02_#2',\
							electionCode=-1, searchType=2, townCode=-1)

	def parse_consti(self, consti, city_name=None):
		consti = super(ElectorCrawler_Recent, self).parse_consti(consti, city_name)
		return consti

	def __init__(self, nth, _election_name):
		self.nth = nth
		self.election_name = _election_name
		self.param_city_codes_json['electionId'] = _election_name
		self.param_url_list['electionId'] = _election_name
		self.param_url_list['requestURI'] = '/WEB-INF/jsp/electioninfo/'+_election_name+'/bi/bipb02.jsp'
