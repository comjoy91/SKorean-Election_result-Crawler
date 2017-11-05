#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from crawlers.counting_vote.base import *
from utils import sanitize

def Crawler(nth, _election_name):
	if 1 <= nth <= 17:
		crawler = CountCrawler_GuOld(int(nth), _election_name)
	elif 18 <= nth <= 20:
		crawler = CountCrawler_Old(int(nth), _election_name)
	elif nth == 21:
		raise InvalidCrawlerError('assembly', 'counting_vote', nth)
		#crawler = CountCrawler_Recent(int(nth), _election_name)
	else:
		raise InvalidCrawlerError('assembly', 'counting_vote', nth)
	return crawler



class CountCrawler_GuOld(MultiCityCrawler):
	vote_for_party = False
	is_constituency = True

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_GuOld.json'
	param_city_codes_json = dict(electionId='0000000000')

	url_list_base = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
	param_url_list = dict(electionId='0000000000',\
							requestURI='/WEB-INF/jsp/electioninfo/0000000000/vc/vccp09.jsp',\
							statementId='VCCP09_#90',\
							oldElectionType=1, electionType=2, electionCode=2,\
							townCode=-1, sggCityCode=-1)

	def parse_consti(self, consti, city_name=None):
		consti = super(CountCrawler_GuOld, self).parse_consti(consti, city_name)
		return consti

	def __init__(self, nth, _election_name):
		self.nth = nth
		self.param_city_codes_json['electionCode'] = _election_name
		self.param_url_list['electionName'] = _election_name

		if nth == 17: #17대 총선(2004)부터 비례대표 정당투표 실시.
			self.prop_crawler = prop_CountCrawler_GuOld(nth, _election_name)
			self.prop_crawler.nth = nth
		else:
			pass


class CountCrawler_Old(MultiCityCrawler):
	vote_for_party = False
	is_constituency = True

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'
	param_city_codes_json = dict(electionId='0000000000',\
									subElectionCode=2)

	url_list_base = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
	param_url_list = dict(electionId='0000000000',\
							requestURI='/WEB-INF/jsp/electioninfo/0000000000/vc/vccp09.jsp',\
							statementId='VCCP09_#2',\
							oldElectionType=1, electionType=2, electionCode=2,\
							townCode=-1, sggCityCode=-1)

	def parse_consti(self, consti, city_name=None):
		consti = super(CountCrawler_Old, self).parse_consti(consti, city_name)
		return consti

	def __init__(self, nth, _election_name):
		self.nth = nth
		self.param_city_codes_json['electionCode'] = _election_name
		self.param_url_list['electionName'] = _election_name

		self.prop_crawler = prop_CountCrawler_Old(nth, _election_name)
		self.prop_crawler.nth = nth


class CountCrawler_Recent(MultiCityCrawler):
	vote_for_party = False
	is_constituency = True

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'
	param_city_codes_json = dict(electionCode=2)

	url_list_base = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
	param_url_list = dict(requestURI='/WEB-INF/jsp/electioninfo/0020160413/vc/vccp09.jsp',\
							statementId='VCCP09_#2',\
							sggCityCode=0, electionCode=2)

	def parse_consti(self, consti, city_name=None):
		consti = super(CountCrawler_Recent, self).parse_consti(consti, city_name)
		self.parse_consti_pledge(consti)
		return consti

	def parse_consti_pledge(self, consti):
		pass # TODO: implement

	def __init__(self, nth, _election_name):
		self.nth = nth
		self.param_city_codes_json['electionId'] = _election_name
		self.param_url_list['electionId'] = _election_name

		self.prop_crawler = prop_CountCrawler_Recent(nth, _election_name)
		self.prop_crawler.nth = nth







class prop_CountCrawler_GuOld(MultiCityCrawler):
	vote_for_party = True
	is_constituency = False

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_GuOld.json'
	param_city_codes_json = dict(electionId='0000000000',\
									subElectionCode=7)

	url_list_base = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
	param_url_list = dict(electionId='0000000000',\
							requestURI='/WEB-INF/jsp/electioninfo/0000000000/vc/vccp09.jsp',\
							statementId='VCCP09_#90',\
							oldElectionType=1, electionType=2, electionCode=7,\
							townCode=-1, sggCityCode=-1)

	def parse_consti(self, consti, city_name=None):
		consti = super(prop_CountCrawler_GuOld, self).parse_consti(consti, city_name)
		return consti

	def __init__(self, nth, _election_name):
		self.nth = nth
		self.param_city_codes_json['electionCode'] = _election_name
		self.param_url_list['electionName'] = _election_name


class prop_CountCrawler_Old(MultiCityCrawler):
	vote_for_party = True
	is_constituency = False

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'
	param_city_codes_json = dict(electionId='0000000000',\
									subElectionCode=7)

	url_list_base = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
	param_url_list = dict(electionId='0000000000',\
							requestURI='/WEB-INF/jsp/electioninfo/0000000000/vc/vccp09.jsp',\
							statementId='VCCP09_#7',\
							oldElectionType=1, electionType=2, electionCode=7,\
							townCode=-1, sggCityCode=-1)

	def parse_consti(self, consti, city_name=None):
		consti = super(prop_CountCrawler_Old, self).parse_consti(consti, city_name)
		return consti

	def __init__(self, nth, _election_name):
		self.nth = nth
		self.param_city_codes_json['electionCode'] = _election_name
		self.param_url_list['electionName'] = _election_name



class prop_CountCrawler_Recent(MultiCityCrawler):
	vote_for_party = True
	is_constituency = False

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'
	param_city_codes_json = dict(electionCode=7, electionId='0020160413')

	url_list_base = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
	param_url_list = dict(requestURI='/WEB-INF/jsp/electioninfo/0020160413/vc/vccp09.jsp',\
							statementId='VCCP09_#7',\
							sggCityCode=0, electionCode=7,\
							electionId='0020160413')

	def parse_consti(self, consti, city_name=None):
		consti = super(prop_CountCrawler_Recent, self).parse_consti(consti, city_name)
		self.parse_consti_party(consti)
		return consti

	def parse_consti_party(self, consti):
		pass # TODO: implement
		#consti['party'] = sanitize(consti['party'][0])

	def __init__(self, nth, _election_name):
		self.nth = nth
		self.param_city_codes_json['electionId'] = _election_name
		self.param_url_list['electionId'] = _election_name
