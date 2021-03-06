#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from crawlers.electorates.base_provincePage import *
from utils import sanitize

def Crawler(nth, election_name, electionType):
	target = 'assembly'
	if 1 <= nth <= 17:
		raise NotImplementedError('Korean National Election Committee does not have any data about electorates in each constituencies of the 1st~17th general election.')
		# 지역구별 선거인수가 나오지 않고, 기초자치단체별 선거인수만 나옴.
		# 선거인수를 받기 위해서는, 결국 개표 결과에 나오는 선거인수를 받아야 함.
	elif 18 <= nth <= 20:
		crawler = Constituency_ElectorCrawler_Old(int(nth), election_name, electionType, target)
	elif nth == 21:
		raise InvalidCrawlerError('electorates', nth, election_name, electionType, target)
		#"최근선거"로 들어갈 때의 code: crawler = ElectorCrawler_Recent(int(nth), election_name, target)
	else:
		raise InvalidCrawlerError('electorates', nth, election_name, electionType, target)
	return crawler



class Constituency_ElectorCrawler_GuOld(MultiCityCrawler_province):

#	def parse_tr_xhtml(self, consti, city_name=None):
#		consti = super(ElectorCrawler_GuOld, self).parse_tr_xhtml(consti, city_name)
#		return consti

	def __init__(self, nth, _election_name, _election_type, _target):
		self.nth = nth
		self.target = _target
		self.elemType = 'constituency_in_province'
		self.isRecent = False

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_GuOld.json'
		self.urlParam_city_codes = dict(electionId='0000000000', electionCode=_election_name)

		self.urlPath_sgg_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_sgg_list = dict(electionId='0000000000', electionName=_election_name,\
										requestURI='/WEB-INF/jsp/electioninfo/0000000000/vc/vccp09.jsp',\
										statementId='VCCP09_#90',\
										oldElectionType=1, electionType=2, electionCode=2,\
										townCode=-1, sggCityCode=-1)


class Constituency_ElectorCrawler_Old(MultiCityCrawler_province):

#	def parse_tr_xhtml(self, consti, city_name=None):
#		consti = super(ElectorCrawler_Old, self).parse_tr_xhtml(consti, city_name)
#		return consti

	def __init__(self, nth, _election_name, _election_type, _target):
		self.nth = nth
		self.target = _target
		self.elemType = 'constituency_in_province'
		self.isRecent = False

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'
		self.urlParam_city_codes = dict(electionId='0000000000', electionCode=_election_name,\
										subElectionCode=2)

		self.urlPath_sgg_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_sgg_list = dict(electionId='0000000000', electionName=_election_name,\
									requestURI='/WEB-INF/jsp/electioninfo/0000000000/bi/bipb02.jsp',\
									statementId='BIPB02_#3_2',\
									oldElectionType=1, electionType=2, electionCode=2,\
									searchType=3, townCode=-1, sggCityCode=-1)
		self.urlParam_sgg_list['statementId'] = 'BIPB02_#3_2_1' if nth==20 else 'BIPB02_#3_2' #왜 얘만 다른지는 모르겠습니다.

		# 재외국민선거 도입으로 지역구 선거인수와 비례대표 선거인수가 달라짐.
		# 비례대표 선거인수는 시군구 단위를 따름.
		if nth == 18: # 18대 총선(2008)은 재외국민선거 도입 이전: 지역구 선거인수와 비례대표 선거인수가 같음. 따라서 지역구 선거인수만 크롤링함.
			pass
		else:
			self.next_crawler = LocalDivision_ElectorCrawler_Old(nth, _election_name, _election_type, _target)


class Constituency_ElectorCrawler_Recent(MultiCityCrawler_province):

#	def parse_tr_xhtml(self, consti, city_name=None):
#		consti = super(ElectorCrawler_Recent, self).parse_tr_xhtml(consti, city_name)
#		return consti

	def __init__(self, nth, _election_name, _election_type, _target):
		self.nth = nth
		self.target = _target
		self.election_name = _election_name
		self.elemType = 'constituency_in_province'
		self.isRecent = True

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'
		self.urlParam_city_codes = dict(electionId=_election_name, electionCode=2)

		self.urlPath_sgg_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_sgg_list = dict(electionId=_election_name, \
									requestURI='/WEB-INF/jsp/electioninfo/'+election_name+'/bi/bipb02.jsp',\
									statementId='BIPB02_#3_2',\
									electionCode=_election_type, searchType=3, townCode=-1)

		self.next_crawler = LocalDivision_ElectorCrawler_Recent(nth, _election_name, _election_type, _target)






class LocalDivision_ElectorCrawler_Old(MultiCityCrawler_province):

#	def parse_tr_xhtml(self, consti, city_name=None):
#		consti = super(LocalDivision_ElectorCrawler_Old, self).parse_tr_xhtml(consti, city_name)
#		return consti

	def __init__(self, nth, _election_name, _election_type, _target):
		self.nth = nth
		self.target = _target
		self.elemType = 'local_division'
		self.isRecent = False

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'
		self.urlParam_city_codes = dict(electionId='0000000000', electionCode=_election_name,\
										subElectionCode=2)

		self.urlPath_town_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_town_list = dict(electionId='0000000000', electionName=_election_name,\
									requestURI='/WEB-INF/jsp/electioninfo/0000000000/bi/bipb02.jsp',\
									statementId='BIPB02_#2_1',\
									oldElectionType=1, electionType=2, electionCode=2,\
									searchType=2, townCode=-1, sggCityCode=-1)
		self.urlParam_town_list['statementId'] = 'BIPB02_#2_1' if nth==20 else 'BIPB02_#2' #왜 얘만 다른지는 모르겠습니다.

class LocalDivision_ElectorCrawler_Recent(MultiCityCrawler_province):
	# TODO: 이 곳의 electionCode는 2(지역구)가 아니라 7(비례대표).

#	def parse_tr_xhtml(self, consti, city_name=None):
#		consti = super(LocalDivision_ElectorCrawler_Recent, self).parse_tr_xhtml(consti, city_name)
#		return consti

	def __init__(self, nth, _election_name, _election_type, _target):
		self.nth = nth
		self.target = _target
		self.election_name = _election_name
		self.elemType = 'local_division'
		self.isRecent = True

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'
		self.urlParam_city_codes = dict(electionId=_election_name, electionCode=7)

		self.urlPath_town_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_town_list = dict(electionId=_election_name,\
									requestURI='/WEB-INF/jsp/electioninfo/'+election_name+'/bi/bipb02.jsp',\
									statementId='BIPB02_#3_7',\
									electionCode=7, searchType=3, townCode=-1)
