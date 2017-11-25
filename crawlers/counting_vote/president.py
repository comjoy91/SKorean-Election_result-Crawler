#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from crawlers.counting_vote.base import *
from utils import sanitize

def Crawler(nth, election_name, electionType, target, target_kor):

	if target == 'president':
		if nth == 1 or 8 <= nth <= 12:
			raise NotImplementedError('The %d-th presidential election(in %s) was held as indirect election: We cannot crawl the data.' % (int(nth), election_name))
		elif 1 <= nth <= 16:
			crawler = Province_townCodeCrawler_GuOld(int(nth), election_name, electionType, target, target_kor)
		elif 17 <= nth <= 18:
			crawler = Province_townCodeCrawler_Old(int(nth), election_name, electionType, target, target_kor)
		elif nth == 19:
			crawler = Province_townCodeCrawler_Recent(int(nth), election_name, electionType, target, target_kor)
		else:
			raise InvalidCrawlerError('townCode', nth, election_name, electionType, target, target_kor)

	return crawler



class CountCrawler_GuOld(MultiCityCrawler):
	vote_for_party = False
	is_constituency = False

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_GuOld.json'
	param_city_codes_json = dict(electionId='0000000000')

	url_list_base = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
	param_url_list = dict(electionId='0000000000',\
							requestURI='/WEB-INF/jsp/electioninfo/0000000000/vc/vccp09.jsp',\
							statementId='VCCP09_#90',\
							oldElectionType=0, electionType=1, electionCode=1,\
							townCode=-1, sggCityCode=-1)

	def parse_consti(self, consti, city_name=None):
		consti = super(CountCrawler_GuOld, self).parse_consti(consti, city_name)
		return consti

	def __init__(self, nth, _election_name):
		self.nth = nth
		self.param_city_codes_json['electionCode'] = _election_name
		self.param_url_list['electionName'] = _election_name


class CountCrawler_Old(MultiCityCrawler):
	vote_for_party = False
	is_constituency = False

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'
	param_city_codes_json = dict(electionId='0000000000',\
									subElectionCode=1)

	url_list_base = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
	param_url_list = dict(electionId='0000000000',\
							requestURI='/WEB-INF/jsp/electioninfo/0000000000/vc/vccp09.jsp',\
							statementId='VCCP09_#1',\
							oldElectionType=1, electionType=1, electionCode=1,\
							townCode=-1, sggCityCode=-1)

	def parse_consti(self, consti, city_name=None):
		consti = super(CountCrawler_Old, self).parse_consti(consti, city_name)
		return consti

	def __init__(self, nth, _election_name):
		self.nth = nth
		self.param_city_codes_json['electionCode'] = _election_name
		self.param_url_list['electionName'] = _election_name


class CountCrawler_Recent(MultiCityCrawler):
	vote_for_party = False
	is_constituency = False
	election_name = ''

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'
	param_city_codes_json = dict(electionCode=1)

	url_list_base = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
	param_url_list = dict(statementId='VCCP09_#1',\
							sggCityCode=0, electionCode=1)

	def parse_consti(self, consti, city_name=None):
		consti = super(CountCrawler_Recent, self).parse_consti(consti, city_name)
		self.parse_consti_pledge(consti)
		return consti

	def parse_consti_pledge(self, consti):
		pass # TODO: implement

	def __init__(self, nth, _election_name):
		self.nth = nth
		self.election_name = _election_name
		self.param_city_codes_json['electionId'] = _election_name
		self.param_url_list['electionId'] = _election_name
		self.param_url_list['requestURI'] = '/WEB-INF/jsp/electioninfo/'+_election_name+'/vc/vccp09.jsp'
