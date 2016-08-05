#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from crawlers.partyCode.base import *
from utils import sanitize

def Crawler(nth):
	if 1 <= nth <= 19:
		crawler = CodeCrawler_1_19(int(nth))
	elif nth == 20:
		crawler = CodeCrawler20(int(nth))
	else:
		raise InvalidCrawlerError('assembly', 'townCode', nth)
	return crawler



class CodeCrawler_1_19(MultiCityCrawler):
	_election_names = [None, '19480510', '19500530', '19540520', '19580502', '19600729',\
					'19631126', '19670608', '19710525', '19730227', '19781212', '19810325', '19850212',\
					'19880426', '19920324', '19960411', '20000413', '20040415',\
					'20080409', '20120411']

	url_list_base = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getJdCodeJson_Old.json'

	param_url_list = dict(electionId='0000000000')

	@property
	def election_name(self):
		return self._election_names[self.nth]

	def parse_consti(self, consti, city_name=None):
		consti = super(CodeCrawler_1_19, self).parse_consti(consti, city_name)
		return consti

	def __init__(self, nth):
		self.nth = nth
		self.param_url_list['electionCode'] = self.election_name



class CodeCrawler20(MultiCityCrawler):
	url_list_base = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getJdCodeJson_Old.json'

	param_url_list = dict(electionId='0020160413', electionCode=2)

	def parse_consti(self, consti, city_name=None):
		consti = super(CodeCrawler20, self).parse_consti(consti, city_name)
		self.parse_consti_pledge(consti)
		return consti

	def parse_consti_pledge(self, consti):
		pass # TODO: implement

	def __init__(self, nth):
		self.nth = nth
