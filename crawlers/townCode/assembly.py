#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from crawlers.townCode.base import *
from utils import sanitize

def Crawler(nth):
	if 1 <= nth <= 17:
		crawler = CodeCrawler_1_17(int(nth))
	elif 18 <= nth <= 19:
		crawler = CodeCrawler1819(int(nth))
	elif nth == 20:
		crawler = CodeCrawler20(int(nth))
	else:
		raise InvalidCrawlerError('assembly', 'townCode', nth)
	return crawler



class CodeCrawler_1_17(MultiCityCrawler):
	is_constituency = False
	"""
	n:1~15: 여기서 크롤링된 데이터에서는, 갑/을로 분구된 것이 그대로 표시되어 있음. 단, 선거구가 합구된 곳은 시군구별로 다 명기됨.
	"""

	_election_names = [None, '19480510', '19500530', '19540520', '19580502', '19600729',\
					'19631126', '19670608', '19710525', '19730227', '19781212', '19810325', '19850212',\
					'19880426', '19920324', '19960411', '20000413', '20040415']

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_GuOld.json'

	param_city_codes_json = dict(electionId='0000000000', subElectionCode=2)

	url_list_base = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeBySgJson_GuOld.json'

	param_url_list = dict(electionId='0000000000', subElectionCode=2)

	@property
	def election_name(self):
		return self._election_names[self.nth]

	def parse_consti(self, consti, city_name=None):
		consti = super(CodeCrawler_1_17, self).parse_consti(consti, city_name)
		return consti

	def __init__(self, nth):
		self.nth = nth
		self.param_city_codes_json['electionCode'] = self.election_name
		self.param_url_list['electionCode'] = self.election_name

		self.prop_crawler = CodeCrawler_1_17Constituency(self.election_name)
		self.prop_crawler.nth = nth



class CodeCrawler1819(MultiCityCrawler):
	is_constituency = False

	_election_names = ['20080409', '20120411']

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'

	param_city_codes_json = dict(electionId='0000000000', subElectionCode=2)

	url_list_base = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeBySgJson_Old.json'

	param_url_list = dict(electionId='0000000000', subElectionCode=2)

	@property
	def election_name(self):
		return self._election_names[self.nth-18]

	def parse_consti(self, consti, city_name=None):
		consti = super(CodeCrawler1819, self).parse_consti(consti, city_name)
		return consti

	def __init__(self, nth):
		self.nth = nth
		self.param_city_codes_json['electionCode'] = self.election_name
		self.param_url_list['electionCode'] = self.election_name

		self.prop_crawler = CodeCrawler1819Constituency(self.election_name)
		self.prop_crawler.nth = nth


class CodeCrawler20(MultiCityCrawler):
	is_constituency = False

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'

	param_city_codes_json = dict(electionCode=2, electionId='0020160413')

	url_list_base = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_townCodeJson.json'

	param_url_list = dict(electionId='0020160413', electionCode=2)

	def parse_consti(self, consti, city_name=None):
		consti = super(CodeCrawler20, self).parse_consti(consti, city_name)
		self.parse_consti_pledge(consti)
		return consti

	def parse_consti_pledge(self, consti):
		pass # TODO: implement

	def __init__(self, nth):
		self.nth = nth
		self.prop_crawler = CodeCrawler20Constituency()
		self.prop_crawler.nth = nth




class CodeCrawler_1_17Constituency(MultiCityCrawler):
	is_constituency = True
	"""
	n:3~5: 지역구 지역명 미명기. "제X선거구". 그러나 선거구 구획제도 특성상, CodeCrawler_1_17의 지역명이 곧 지역구의 지역명과 동일.
	n:6~8: 일부 지역에서 지역구 지역명 미명기. "제X선거구".
	n:9, 10: 지역구 지역명 미명기. "제X선거구".
	n:17: 지역구 크롤링이 안되야...
	"""

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_GuOld.json'

	param_city_codes_json = dict(electionId='0000000000', subElectionCode=2)

	url_list_base = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getSggCityCodeJson_GuOld.json'

	param_url_list = dict(electionId='0000000000', electionCode=2)

	def parse_consti(self, consti, city_name=None):
		consti = super(CodeCrawler_1_17Constituency, self).parse_consti(consti, city_name)
		self.parse_consti_party(consti)
		return consti

	def __init__(self, _election_name):
		self.param_city_codes_json['electionCode'] = _election_name
		self.param_url_list['electionName'] = _election_name



class CodeCrawler1819Constituency(MultiCityCrawler):
	is_constituency = True

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'

	param_city_codes_json = dict(electionId='0000000000', subElectionCode=2)

	url_list_base = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getSggCityCodeJson_Old.json'

	param_url_list = dict(electionId='0000000000', electionCode=2)

	def parse_consti(self, consti, city_name=None):
		consti = super(CodeCrawler1819Constituency, self).parse_consti(consti, city_name)
		self.parse_consti_party(consti)
		return consti

	def __init__(self, _election_name):
		self.param_city_codes_json['electionCode'] = _election_name
		self.param_url_list['electionName'] = _election_name



class CodeCrawler20Constituency(MultiCityCrawler):
	is_constituency = True

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'

	param_city_codes_json = dict(electionCode=2, electionId='0020160413')

	url_list_base = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getSggCityCodeJson.json'

	param_url_list = dict(electionId='0020160413', electionCode=2)

	def parse_consti(self, consti, city_name=None):
		consti = super(CodeCrawler20Proportional, self).parse_consti(consti, city_name)
		self.parse_consti_party(consti)
		return consti

	def parse_consti_party(self, consti):
		pass # TODO: implement
		#consti['party'] = sanitize(consti['party'][0])
