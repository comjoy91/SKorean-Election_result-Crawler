#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from crawlers.electorates.base_provincePage import *
from utils import sanitize

def Crawler(nth, election_name, electionType, target, target_kor):
	if target == 'president':
		if nth == 1 or 8 <= nth <= 12:
			raise NotImplementedError('The %d-th presidential election(in %s) was held as indirect election: We cannot crawl the data.' % (int(nth), election_name))
		elif 1 <= nth <= 15:
			raise NotImplementedError('Korean National Election Committee does not have any data about electorates in each local region of the 1st~15th presidential election.')
		elif nth == 16:
			crawler = Province_ElectorCrawler_GuOld(int(nth), election_name, electionType, target, target_kor)
		elif 17 <= nth <= 18:
			crawler = Province_ElectorCrawler_Old(int(nth), election_name, electionType, target, target_kor)
		elif nth == 19:
			crawler = Province_ElectorCrawler_Recent(int(nth), election_name, electionType, target, target_kor)
		else:
			raise InvalidCrawlerError('electorates', nth, election_name, electionType, target)

	elif target == 'local_provincal_administration' or \
        target == 'local_municipal_administration':
		if 1 <= nth <= 3:
			crawler = Province_ElectorCrawler_GuOld(int(nth), election_name, electionType, target, target_kor)
		elif 4 <= nth <= 6:
			crawler = Province_ElectorCrawler_Old(int(nth), election_name, electionType, target, target_kor)
		elif nth == 7:
			raise InvalidCrawlerError('electorates', nth, election_name, electionType, target, target_kor)
			#"최근선거"로 들어갈 때의 code: crawler = Province_ElectorCrawler_Recent(int(nth), election_name, electionType, target, target_kor)
		else:
			raise InvalidCrawlerError('electorates', nth, election_name, electionType, target, target_kor)

	elif target == 'local_eduAdministration':
		if 1 <= nth <= 4:
			raise NotImplementedError('Educational Superintendent Election was not held in %s.' % election_name)
		elif 5 <= nth <= 6:
			crawler = Province_ElectorCrawler_Old(int(nth), election_name, electionType, target, target_kor)
		elif nth == 7:
			raise InvalidCrawlerError('townCode', nth, election_name, electionType, target, target_kor)
			#"최근선거"로 들어갈 때의 code: crawler = Province_ElectorCrawler_Recent(int(nth), election_name, electionType, target, target_kor)
		else:
			raise InvalidCrawlerError('townCode', nth, election_name, electionType, target, target_kor)

	else:
		raise InvalidCrawlerError('electorates', nth, election_name, electionType, target)

	return crawler



class Province_ElectorCrawler_GuOld(MultiCityCrawler_province):

#	def parse_tr_xhtml(self, consti, city_name=None):
#		consti = super(Province_ElectorCrawler_GuOld, self).parse_tr_xhtml(consti, city_name)
#		return consti

	def __init__(self, nth, _election_name, _target, _target_kor):
		self.nth = nth
		self.target = _target
		self.target_kor = _target_kor
		self.isRecent = False

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_GuOld.json'
		self.urlParam_city_codes = dict(electionId='0000000000', electionCode=_election_name)

		self.urlPath_town_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_town_list = dict(electionId='0000000000', electionName=_election_name,\
										requestURI='/WEB-INF/jsp/electioninfo/0000000000/bi/bipb02.jsp',\
										statementId='BIPB92_#1',\
										oldElectionType=0, electionType=1, searchType=2, electionCode=_election_type)
										# oldElectionType: ('재외국민수', '외국인수') 포함 여부
										# electionType: 1-대통령선거, 2-국회의원선거, 3-?, 4-지방선거, 0-재보궐선거, 11-교육감선거
										# searchType: 1-시도별, 2-구시군별, 3-선거구별, 4-읍면동별, 5-투표구별


class Province_ElectorCrawler_Old(MultiCityCrawler_province):

#	def parse_tr_xhtml(self, consti, city_name=None):
#		consti = super(Province_ElectorCrawler_Old, self).parse_tr_xhtml(consti, city_name)
#		return consti

	def __init__(self, nth, _election_name, _target, _target_kor):
		self.nth = nth
		self.target = _target
		self.target_kor = _target_kor
		self.isRecent = False

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'
		self.urlParam_city_codes = dict(electionId='0000000000', electionCode=_election_name,\
										subElectionCode=1)

		self.urlPath_town_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_town_list = dict(electionId='0000000000', electionName=_election_name,\
										requestURI='/WEB-INF/jsp/electioninfo/0000000000/bi/bipb02.jsp',\
										statementId='BIPB02_#2',\
										oldElectionType=0, electionType=1, searchType=2, electionCode=_election_type)
										# oldElectionType: ('재외국민수', '외국인수') 포함 여부
										# electionType: 1-대통령선거, 2-국회의원선거, 4-지방선거, 0-재보궐선거, 11-교육감선거
										# searchType: 1-시도별, 2-구시군별, 3-선거구별, 4-읍면동별, 5-투표구별


class Province_ElectorCrawler_Recent(MultiCityCrawler_province):

#	def parse_tr_xhtml(self, consti, city_name=None):
#		consti = super(Province_ElectorCrawler_Recent, self).parse_tr_xhtml(consti, city_name)
#		return consti

	def __init__(self, nth, _election_name, _target, _target_kor):
		self.nth = nth
		self.target = _target
		self.target_kor = _target_kor
		self.isRecent = True

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'
		self.urlParam_city_codes = dict(electionCode=_election_type, electionId=_election_name)

		self.urlPath_town_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_town_list = dict(electionId=_election_name, statementId='BIPB02_#2',\
									requestURI='/WEB-INF/jsp/electioninfo/'+_election_name+'/bi/bipb02.jsp',
									electionCode=_election_type, searchType=2)
									# searchType: 1-시도별, 2-구시군별, 3-선거구별, 4-읍면동별, 5-투표구별
