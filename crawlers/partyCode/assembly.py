#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from crawlers.partyCode.base import *
from utils import sanitize

def Crawler(nth, _election_name):
	if 1 <= nth <= 20:
		crawler = Party_CodeCrawler_Old(int(nth), _election_name)
	elif nth == 21:
		raise InvalidCrawlerError('assembly', 'townCode', nth)
		#crawler = Party_CodeCrawler_Recent(int(nth), _election_name)
	else:
		raise InvalidCrawlerError('assembly', 'partyCode', nth)
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
