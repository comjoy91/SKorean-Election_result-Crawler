#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from crawlers.electorates.base import *
from utils import sanitize

def Crawler(nth):
	if 1 <= nth <= 17:
		raise NotImplementedError('Assembly election (nth: 1~17) electorates crawler')
		# crawler = ElectorCrawler_1_17(int(nth))
	elif 18 <= nth <= 19:
		crawler = ElectorCrawler1819(int(nth))
	elif nth == 20:
		crawler = ElectorCrawler20(int(nth))
	else:
		raise InvalidCrawlerError('assembly', 'electorates', nth)
	return crawler



class ElectorCrawler_1_17(MultiCityCrawler):
	is_proportional = False

	_election_names = [None, '19480510', '19500530', '19540520', '19580502', '19600729',\
					'19631126', '19670608', '19710525', '19730227', '19781212', '19810325', '19850212',\
					'19880426', '19920324', '19960411', '20000413', '20040415']

	"""
	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_GuOld.json'

	param_city_codes_json = dict(electionId='0000000000',\
									subElectionCode=2)

	url_list_base = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'

	param_url_list = dict(electionId='0000000000',\
							requestURI='/WEB-INF/jsp/electioninfo/0000000000/vc/vccp09.jsp',\
							statementId='VCCP09_#90',\
							oldElectionType=1, electionType=2, electionCode=2,\
							townCode=-1, sggCityCode=-1)
	"""
	#need to implement nth:1~17.

	@property
	def election_name(self):
		return self._election_names[self.nth]

	def parse_consti(self, consti, city_name=None):
		consti = super(ElectorCrawler_1_17, self).parse_consti(consti, city_name)
		return consti

	def __init__(self, nth):
		self.nth = nth



class ElectorCrawler1819(MultiCityCrawler):
	is_proportional = False

	_election_names = ['20080409', '20120411']

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'

	param_city_codes_json = dict(electionId='0000000000',\
									subElectionCode=2)

	url_list_base = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'

	param_url_list = dict(electionId='0000000000',\
							requestURI='/WEB-INF/jsp/electioninfo/0000000000/bi/bipb02.jsp',\
							statementId='BIPB02_#3_2',\
							oldElectionType=1, electionType=2, electionCode=2,\
							searchType=3, townCode=-1, sggCityCode=-1)

	@property
	def election_name(self):
		return self._election_names[self.nth-18]

	def parse_consti(self, consti, city_name=None):
		consti = super(ElectorCrawler1819, self).parse_consti(consti, city_name)
		return consti

	def __init__(self, nth):
		self.nth = nth
		self.param_city_codes_json['electionCode'] = self.election_name
		self.param_url_list['electionName'] = self.election_name



class ElectorCrawler20(MultiCityCrawler):
	is_proportional = False

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'

	param_city_codes_json = dict(electionCode=2, electionId='0020160413')

	url_list_base = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'

	param_url_list = dict(requestURI='/WEB-INF/jsp/electioninfo/0020160413/bi/bipb02.jsp',\
							statementId='BIPB02_#3_2',\
							electionCode=2, searchType=3, townCode=-1,\
							electionId='0020160413')

	def parse_consti(self, consti, city_name=None):
		consti = super(ElectorCrawler20, self).parse_consti(consti, city_name)
		self.parse_consti_pledge(consti)
		return consti

	def parse_consti_pledge(self, consti):
		pass # TODO: implement

	def __init__(self, nth):
		self.nth = nth
		self.prop_crawler = ElectorCrawler20Proportional()
		self.prop_crawler.nth = nth



class ElectorCrawler20Proportional(MultiCityCrawler):
	is_proportional = True

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'

	param_city_codes_json = dict(electionCode=7, electionId='0020160413')

	url_list_base = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'

	param_url_list = dict(requestURI='/WEB-INF/jsp/electioninfo/0020160413/bi/bipb02.jsp',\
							statementId='BIPB02_#3_7',\
							electionCode=7, searchType=3, townCode=-1,\
							electionId='0020160413')

	def parse_consti(self, consti, city_name=None):
		consti = super(ElectorCrawler20Proportional, self).parse_consti(consti, city_name)
		self.parse_consti_party(consti)
		return consti

	def parse_consti_party(self, consti):
		pass # TODO: implement
		#consti['party'] = sanitize(consti['party'][0])
