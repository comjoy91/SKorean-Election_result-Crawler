#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from crawlers.partyCode.base import *
from utils import sanitize

def Crawler(nth, election_name, electionType, target, target_eng, target_kor):
	if target == 'assembly':
		if 1 <= nth <= 20:
			crawler = Party_CodeCrawler_Old(election_name)
		else:
			raise InvalidCrawlerError('partyCode', nth, election_name, target, target_eng, target_kor)
		return crawler

	if target == 'president':
		if 1 <= nth <= 19:
			crawler = Party_CodeCrawler_Old(election_name)
		else:
			raise InvalidCrawlerError('partyCode', nth, election_name, target, target_eng, target_kor)
		return crawler

	elif target == 'local-pa' or \
		target == 'local-ma' or \
		target == 'local-pp' or \
        target == 'local-mp' :
		if 1 <= nth <= 6:
			crawler = Party_CodeCrawler_Old(election_name)
		else:
			raise InvalidCrawlerError('partyCode', nth, election_name, target, target_eng, target_kor)

	elif target == 'local-ea':
		if 1 <= nth <= 4:
			raise NotImplementedError('Educational Superintendent Election was not held in %s.' % election_name)
		elif 5 <= nth <= 6:
			crawler = Party_CodeCrawler_Old(election_name)
		else:
			raise InvalidCrawlerError('partyCode', nth, election_name, target, target_eng, target_kor)

	elif target == 'local-ep':
		if 1 <= nth <= 3:
			raise NotImplementedError('Educational Parliament Election was not held in %s.' % election_name)
		elif 4 <= nth <= 6:
			crawler = Party_CodeCrawler_Old(election_name)
		else:
			raise InvalidCrawlerError('partyCode', nth, election_name, target, target_eng, target_kor)

	else:
		raise InvalidCrawlerError('partyCode', nth, election_name, target, target_eng, target_kor)

	crawler.nth = nth
	crawler.target = target
	crawler.target_eng = target_eng
	crawler.target_kor = target_kor


class Party_CodeCrawler_Old(JSONCrawler):

	def __init__(self, nth, _election_name, _target):
		self.urlPath_party_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getJdCodeJson_Old.json'
		self.urlParam_party_codes = dict(electionId='0000000000', electionCode=_election_name)



class Party_CodeCrawler_Recent(JSONCrawler):

	def __init__(self, nth, _election_name, _target):
		self.urlPath_party_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getJdCodeJson_Old.json'
		self.urlParam_party_codes = dict(electionCode=2, electionId=_election_name)
