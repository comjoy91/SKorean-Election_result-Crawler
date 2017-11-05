#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from crawlers.partyCode.base import *
from utils import sanitize

def Crawler(nth, _election_name):
	if 1 <= nth <= 6:
		crawler = Party_CodeCrawler_Old(int(nth), _election_name)
	elif nth == 7:
		raise InvalidCrawlerError('local', 'partyCode', nth)
		#"최근선거"로 들어갈 때의 code: crawler = Party_CodeCrawler_Recent(int(nth), _election_name)
	else:
		raise InvalidCrawlerError('president', 'partyCode', nth)
	return crawler



class Party_CodeCrawler_Old(JSONCrawler):

	url_list_base = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getJdCodeJson_Old.json'
	param_url_list = dict(electionId='0000000000')

	def __init__(self, nth, _election_name):
		self.nth = nth
		self.param_url_list['electionCode'] = _election_name



class Party_CodeCrawler_Recent(JSONCrawler):
	url_list_base = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getJdCodeJson_Old.json'
	param_url_list = dict(electionCode=1)

	def __init__(self, nth, _election_name):
		self.nth = nth
		self.param_url_list['electionId'] = _election_name
