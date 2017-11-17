#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from crawlers.partyCode.base import *
from utils import sanitize

def Crawler(nth, _election_name):
	target = 'assembly'
	if 1 <= nth <= 20:
		crawler = Party_CodeCrawler_Old(int(nth), _election_name, target)
	elif nth == 21:
		raise InvalidCrawlerError('partyCode', nth, _election_name, target)
		#"최근선거"로 들어갈 때의 code: crawler = Party_CodeCrawler_Recent(int(nth), _election_name, target)
	else:
		raise InvalidCrawlerError('partyCode', nth, _election_name, target)
	return crawler



class Party_CodeCrawler_Old(JSONCrawler):

	def __init__(self, nth, _election_name, _target):
		self.nth = nth
		self.target = _target

		self.url_list_base = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getJdCodeJson_Old.json'
		self.param_url_list = dict(electionId='0000000000', electionCode=_election_name)



class Party_CodeCrawler_Recent(JSONCrawler):

	def __init__(self, nth, _election_name, _target):
		self.nth = nth
		self.target = _target
		
		self.url_list_base = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getJdCodeJson_Old.json'
		self.param_url_list = dict(electionCode=2, electionId=_election_name)
