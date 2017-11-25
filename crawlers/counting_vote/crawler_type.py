#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from crawlers.counting_vote.base import *
from utils import sanitize

def Crawler(nth, election_name, electionType, target, target_kor):
	if target == 'assembly':
		if 1 <= nth <= 16:
			crawler = Constituency_CountCrawler_GuOld(int(nth), election_name, electionType)
		elif nth == 17:
			crawler = Constituency_CountCrawler_GuOld(int(nth), election_name, electionType)
			crawler.next_crawler = Proportional_CountCrawler_GuOld(int(nth), election_name, 7)
		elif 18 <= nth <= 20:
			crawler = Constituency_CountCrawler_Old(int(nth), election_name, electionType)
			crawler.next_crawler = Proportional_CountCrawler_Old(int(nth), election_name, 7)
		elif nth == 21:
			raise InvalidCrawlerError('counting_vote', nth, election_name, electionType, target, target_kor)
			#"최근선거"로 들어갈 때의 code:
			#crawler = Constituency_CountCrawler_Recent(int(nth), election_name, electionType)
			#crawler.next_crawler = Proportional_CountCrawler_Recent(int(nth), election_name, electionType)
		else:
			raise InvalidCrawlerError('counting_vote', nth, election_name, electionType, target, target_kor)
		crawler.candidate_type = 'party_candidate'
		if hasattr(crawler, 'next_crawler'):
			crawler.next_crawler.candidate_type = 'party_list'
			crawler.next_crawler.nationalSum = True

	elif target == 'local_provincal_parliament':
		if 1 <= nth <= 2:
			crawler = Constituency_CountCrawler_GuOld(int(nth), election_name, electionType)
		elif nth == 3:
			crawler = Constituency_CountCrawler_GuOld(int(nth), election_name, electionType)
			crawler.next_crawler = Proportional_CountCrawler_GuOld(int(nth), election_name, 8)
		elif 4 <= nth <= 6:
			crawler = Constituency_CountCrawler_Old(int(nth), election_name, electionType)
			crawler.next_crawler = Proportional_CountCrawler_Old(int(nth), election_name, 8)
		elif nth == 7:
			raise InvalidCrawlerError('counting_vote', nth, election_name, electionType, target, target_kor)
			#"최근선거"로 들어갈 때의 code:
			#crawler = Constituency_CountCrawler_Recent(int(nth), election_name, electionType)
			#crawler.next_crawler = Proportional_CountCrawler_Recent(int(nth), election_name, 8)
		else:
			raise InvalidCrawlerError('counting_vote', nth, election_name, electionType, target, target_kor)
		crawler.candidate_type = 'party_candidate'
		if hasattr(crawler, 'next_crawler'):
			crawler.next_crawler.candidate_type = 'party_list'

	elif target == 'local_municipal_parliament':
		if 1 <= nth <= 3:
			crawler = Constituency_CountCrawler_GuOld(int(nth), election_name, electionType)
		elif 4 <= nth <= 6:
			crawler = Constituency_CountCrawler_Old(int(nth), election_name, electionType)
			crawler.next_crawler = Constituency_CountCrawler_Old(int(nth), election_name, 9)
		elif nth == 7:
			raise InvalidCrawlerError('counting_vote', nth, election_name, electionType, target, target_kor)
			#"최근선거"로 들어갈 때의 code:
			#crawler = Constituency_CountCrawler_Recent(int(nth), election_name, electionType)
			#crawler.next_crawler = Constituency_CountCrawler_Recent(int(nth), election_name, 8)
		else:
			raise InvalidCrawlerError('counting_vote', nth, election_name, electionType, target, target_kor)
		crawler.candidate_type = 'party_candidate'
		if hasattr(crawler, 'next_crawler'):
			crawler.next_crawler.candidate_type = 'party_list'

	elif target == 'local_eduParliament':
		if 1 <= nth <= 3:
			raise NotImplementedError('Educational Parliament Election was not held in the %d-th local unified local election(%s).' % (int(nth), election_name))
		elif 4 <= nth <= 6:
			crawler = Constituency_CountCrawler_Old(int(nth), election_name, electionType)
		elif nth == 7:
			raise InvalidCrawlerError('counting_vote', nth, election_name, electionType, target, target_kor)
			#"최근선거"로 들어갈 때의 code: crawler = Constituency_CountCrawler_Recent(int(nth), election_name, electionType)
		else:
			raise InvalidCrawlerError('counting_vote', nth, election_name, electionType, target, target_kor)
		crawler.candidate_type = 'independent_candidate'

	elif target == 'president':
		if nth == 1 or 8 <= nth <= 12:
			raise NotImplementedError('The %d-th presidential election(in %s) was held as indirect election: We cannot crawl the data.' % (int(nth), election_name))
		elif 1 <= nth <= 16:
			crawler = Proportional_CountCrawler_GuOld(int(nth), election_name, electionType)
		elif 17 <= nth <= 18:
			crawler = Proportional_CountCrawler_Old(int(nth), election_name, electionType)
		elif nth == 19:
			crawler = Proportional_CountCrawler_Recent(int(nth), election_name, electionType)
		else:
			raise InvalidCrawlerError('counting_vote', nth, election_name, electionType, target, target_kor)
		crawler.candidate_type = 'party_candidate'
		crawler.nationalSum = True

	elif target == 'local_provincal_administration':
		if 1 <= nth <= 3:
			crawler = Proportional_CountCrawler_GuOld(int(nth), election_name, electionType)
		elif 4 <= nth <= 6:
			crawler = Proportional_CountCrawler_Old(int(nth), election_name, electionType)
		elif nth == 7:
			raise InvalidCrawlerError('counting_vote', nth, election_name, electionType, target, target_kor)
			#"최근선거"로 들어갈 때의 code: crawler = Proportional_CountCrawler_Recent(int(nth), election_name, electionType)
		else:
			raise InvalidCrawlerError('counting_vote', nth, election_name, electionType, target, target_kor)
		crawler.candidate_type = 'party_candidate'

	elif target == 'local_municipal_administration':
		if 1 <= nth <= 3:
			crawler = Constituency_CountCrawler_GuOld(int(nth), election_name, electionType)
		elif 4 <= nth <= 6:
			crawler = Constituency_CountCrawler_Old(int(nth), election_name, electionType)
		elif nth == 7:
			raise InvalidCrawlerError('counting_vote', nth, election_name, electionType, target, target_kor)
			#"최근선거"로 들어갈 때의 code: crawler = Constituency_CountCrawler_Recent(int(nth), election_name, electionType)
		else:
			raise InvalidCrawlerError('counting_vote', nth, election_name, electionType, target, target_kor)
		crawler.candidate_type = 'party_candidate'

	elif target == 'local_eduAdministration':
		if 1 <= nth <= 4:
			raise NotImplementedError('Educational Superintendent Election was not held in the %d-th local unified local election(%s).' % (int(nth), election_name))
		elif 5 <= nth <= 6:
			crawler = Proportional_CountCrawler_Old(int(nth), election_name, electionType)
		elif nth == 7:
			raise InvalidCrawlerError('counting_vote', nth, election_name, electionType, target, target_kor)
			#"최근선거"로 들어갈 때의 code: crawler = Proportional_CountCrawler_Recent(int(nth), election_name, electionType)
		else:
			raise InvalidCrawlerError('counting_vote', nth, election_name, electionType, target, target_kor)
		crawler.candidate_type = 'independent_candidate'

	crawler.nth = nth
	crawler.target = target
	crawler.target_kor = target_kor

	if hasattr(crawler, 'next_crawler'):
		crawler.next_crawler.nth = nth
		crawler.next_crawler.target = target
		crawler.next_crawler.target_kor = target_kor

	return crawler



class Constituency_CountCrawler_GuOld(MultiCityCrawler):

	def parse_consti(self, consti, city_name=None):
		consti = super(Constituency_CountCrawler_GuOld, self).parse_consti(consti, city_name)
		return consti

	def __init__(self, nth, _election_name, _election_type):
		self.nth = nth
		self.constant_candidates = False

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_GuOld.json'
		self.urlParam_city_codes = dict(electionId='0000000000', electionCode=_election_name, subElectionCode=_election_type)

		self.urlPath_result_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_result_list = dict(electionId='0000000000', electionName=_election_name,\
										requestURI='/WEB-INF/jsp/electioninfo/0000000000/vc/vccp09.jsp',\
										statementId='VCCP09_#90',\
										oldElectionType=0, electionType=2, electionCode=_election_type)
										# oldElectionType: ('재외국민수', '외국인수') 포함 여부이자, GuOld(=0)냐 Old(=1)냐 여부.
										# electionType: 1-대통령선거, 2-국회의원선거, 4-전국동시지방선거, 0-재보궐선거, 11-교육감선거


class Constituency_CountCrawler_Old(MultiCityCrawler):

	def parse_consti(self, consti, city_name=None):
		consti = super(Constituency_CountCrawler_Old, self).parse_consti(consti, city_name)
		return consti

	def __init__(self, nth, _election_name, _election_type):
		self.nth = nth
		self.constant_candidates = False

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'
		self.urlParam_city_codes = dict(electionId='0000000000', electionCode=_election_name, subElectionCode=_election_type)

		self.urlPath_result_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_result_list = dict(electionId='0000000000', electionName=_election_name,\
										requestURI='/WEB-INF/jsp/electioninfo/0000000000/vc/vccp09.jsp',\
										statementId='VCCP09_#'+str(_election_type),\
										oldElectionType=1, electionType=2, electionCode=_election_type)
										# oldElectionType: ('재외국민수', '외국인수') 포함 여부이자, GuOld(=0)냐 Old(=1)냐 여부.
										# electionType: 1-대통령선거, 2-국회의원선거, 4-전국동시지방선거, 0-재보궐선거, 11-교육감선거


class Constituency_CountCrawler_Recent(MultiCityCrawler):

	def parse_consti(self, consti, city_name=None):
		consti = super(Constituency_CountCrawler_Recent, self).parse_consti(consti, city_name)
		self.parse_consti_pledge(consti)
		return consti

	def parse_consti_pledge(self, consti):
		pass # TODO: implement

	def __init__(self, nth, _election_name, _election_type):
		self.nth = nth
		self.constant_candidates = False

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'
		self.urlParam_city_codes = dict(electionId=_election_name, electionCode=_election_type)

		self.urlPath_result_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_result_list = dict(electionId=_election_name,\
										requestURI='/WEB-INF/jsp/electioninfo/'+_election_name+'/vc/vccp09.jsp',\
										statementId='VCCP09_#'+str(_election_type), electionCode=_election_type)







class Proportional_CountCrawler_GuOld(MultiCityCrawler):

	#def parse_consti(self, consti, city_name=None):
	#	consti = super(Proportional_CountCrawler_GuOld, self).parse_consti(consti, city_name)
	#	return consti

	def __init__(self, nth, _election_name, _election_type):
		self.nth = nth
		self.constant_candidates = True

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_GuOld.json'
		self.urlParam_city_codes = dict(electionId='0000000000', electionCode=_election_name, subElectionCode=_election_type)

		self.urlPath_result_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_result_list = dict(electionId='0000000000', electionName=_election_name,\
										requestURI='/WEB-INF/jsp/electioninfo/0000000000/vc/vccp09.jsp',\
										statementId='VCCP09_#90',\
										oldElectionType=0, electionType=2, electionCode=_election_type)
										# oldElectionType: ('재외국민수', '외국인수') 포함 여부이자, GuOld(=0)냐 Old(=1)냐 여부.
										# electionType: 1-대통령선거, 2-국회의원선거, 4-전국동시지방선거, 0-재보궐선거, 11-교육감선거


class Proportional_CountCrawler_Old(MultiCityCrawler):

	#def parse_consti(self, consti, city_name=None):
	#	consti = super(Proportional_CountCrawler_Old, self).parse_consti(consti, city_name)
	#	return consti

	def __init__(self, nth, _election_name, _election_type):
		self.nth = nth
		self.constant_candidates = True

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'
		self.urlParam_city_codes = dict(electionId='0000000000', electionCode=_election_name, subElectionCode=_election_type)

		self.urlPath_result_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_result_list = dict(electionId='0000000000', electionName=_election_name,\
										requestURI='/WEB-INF/jsp/electioninfo/0000000000/vc/vccp09.jsp',\
										statementId='VCCP09_#'+str(_election_type),\
										oldElectionType=1, electionType=2, electionCode=_election_type)
										# oldElectionType: ('재외국민수', '외국인수') 포함 여부이자, GuOld(=0)냐 Old(=1)냐 여부.
										# electionType: 1-대통령선거, 2-국회의원선거, 4-전국동시지방선거, 0-재보궐선거, 11-교육감선거



class Proportional_CountCrawler_Recent(MultiCityCrawler):

	#def parse_consti(self, consti, city_name=None):
	#	consti = super(Proportional_CountCrawler_Recent, self).parse_consti(consti, city_name)
	#	self.parse_consti_party(consti)
	#	return consti

	def parse_consti_party(self, consti):
		pass # TODO: implement
		#consti['party'] = sanitize(consti['party'][0])

	def __init__(self, nth, _election_name, _election_type):
		self.nth = nth
		self.constant_candidates = True

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'
		self.urlParam_city_codes = dict(electionId=_election_name, electionCode=_election_type)

		self.urlPath_result_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_result_list = dict(electionId=_election_name,\
										requestURI='/WEB-INF/jsp/electioninfo/'+_election_name+'/vc/vccp09.jsp',\
										statementId='VCCP09_#'+str(_election_type), electionCode=_election_type)
