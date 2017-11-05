#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

from argparse import ArgumentParser, RawTextHelpFormatter
import codecs
import gevent
from gevent import monkey
import json
from datetime import datetime
from threading import Timer, Thread
import sched, time

from crawlers import Crawler
from utils import check_dir

def print_json(filename, encoding, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=(encoding=='unicode'))

def print_csv(filename, encoding, data):

    raise NotImplementedError('Printing csv file is not implemented.')
    """
    def transform(txt):
        if isinstance(txt, int):
            txt = str(txt)
        if isinstance(txt, list):
            txt = '||'.join(txt)
        txt = txt.replace(',', '|')
        if encoding=='utf8' and isinstance(txt, str) :
            txt = txt.encode('utf8')
        return txt

    attrs = ['assembly_no', 'time', 'election_type', 'grand_district', 'district',
             'electorates', 'counted_vote', 'cand_no',
             'party', 'name_kr', 'votes',
             'valid_vote', 'undervote', 'blank_ballot']

    with open(filename, 'w') as f:
        f.write(codecs.BOM_UTF8)
        f.write(','.join(attrs))
        f.write('\n')
        for cand in data:
            values = (cand[attr] if attr in cand else '' for attr in attrs)
            values = (transform(value) for value in values)
            f.write(','.join(values))
            f.write('\n')
    """

def crawl(target, _type, nth, printer, filename, encoding, level=None):
    crawler = Crawler(target, _type, nth, level)
    cand_list = crawler.crawl()
    printer(filename, encoding, cand_list)

def create_parser():
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('target', choices=['assembly', 'local', 'president'],\
            help="name of target election")
    parser.add_argument('type', choices=['townCode', 'electorates', 'partyCode', 'counting_vote', 'counting_vote_dong'],\
            help="type of collecting data\n"
                "- We DO NOT RECOMMAND to crawl TOWNCODE data: \n"
                "- KEC categorize townCode data by some rude standard, so we re-classify all the data by hand.") #'turnout'
    parser.add_argument('start', help="starting election id", type=int)
    parser.add_argument('end', help="ending election id", type=int,\
            nargs='?', default=None)

    parser.add_argument('-time', dest='filename_time', action='store_true',\
            help="Descript the crawling moment time info in filename.")
    parser.add_argument('-interval', dest='interval_time',\
                help="number of interval seconds.\n"
                "- if you type integer number, the program will automatically crawl data in every 'interval' seconds.\n"
                "- if you type 0 or do not type anything, the program will crawl only once.",\
                type=int, default=None)
    parser.add_argument('-e', dest='encoding', choices=['unicode', 'utf8'], default='utf8',\
            help="Korean Hangul encoding.\n"
                "- utf8 for default.")
    parser.add_argument('-csv', dest='test', action='store_true',
            help="Assign datatype to csv instead of json.\n"
                "- We DO NOT RECOMMAND to select -csv type: it is still not be implemented.")
    parser.add_argument('-d', dest='directory', help="Specify data directory.")

    # TODO: change to subparser
    parser.add_argument('-l', choices=['pg', 'pm', 'pp', 'mg', 'mm', 'mp', 'eg', 'em'],
            dest="level",
            help="Specify level for local elections.\n"
                "- 1st char: {p:province, m:municipality, e:education},\n"
                "- 2nd char: {g: governor, m: member}")

    return parser

def print_file(arg_namespace):
    _arg = arg_namespace

    printer = print_csv if _arg.test else print_json
    encoding = _arg.encoding

    datadir = _arg.directory if _arg.directory \
                else './crawled_data/%s/%s' % (_arg.target, _arg.type)
    target = _arg.target
    electionType = _arg.type
    start = _arg.start
    end = _arg.end if _arg.end else start
    filename_time = _arg.filename_time
    filetype = 'csv' if _arg.test else 'json'

    interval_time = _arg.interval_time
    if target=='local':
        level = get_election_type_name(_arg.level)
    else:
        level = None

    time_string = datetime.today().strftime("%Y%m%d%H%M%S")
    check_dir(datadir)

    jobs = []
    if target=='local':
        if filename_time:
            for n in range(start, end+1):
                filename = '%s/%s-%s-%s-%d-%s.%s'\
                    % (datadir, target, level, electionType, n, time_string, filetype)
                job = gevent.spawn(crawl, target=target, level=level,\
                    _type=_electionType, nth=n, filename=filename, encoding=_encoding, printer=printer)
                jobs.append(job)
        else:
            for n in range(start, end+1):
                filename = '%s/%s-%s-%s-%d.%s'\
                    % (datadir, target, level, electionType, n, filetype)
                job = gevent.spawn(crawl, target=_target, level=level,\
                    _type=_electionType, nth=n, filename=filename, encoding=_encoding, printer=printer)
                jobs.append(job)

    else:
        if filename_time:
            for n in range(start, end+1):
                filename = '%s/%s-%s-%d-%s.%s'\
                        % (datadir, target, electionType, n, time_string, filetype)
                job = gevent.spawn(crawl, target=target, _type=electionType, nth=n,\
                        filename=filename, encoding=encoding, printer=printer)
                jobs.append(job)
        else:
            for n in range(start, end+1):
                filename = '%s/%s-%s-%d.%s'\
                        % (datadir, target, electionType, n, filetype)
                job = gevent.spawn(crawl, target=target, _type=electionType, nth=n,\
                        filename=filename, encoding=encoding, printer=printer)
                jobs.append(job)

    gevent.joinall(jobs)
    print('Data written to %s' % filename)

    if interval_time!=0 and interval_time!=None:
        s = sched.scheduler(time.time, time.sleep)
        print('The program will crawl the next data within %d seconds.' % interval_time)
        s.enter(interval_time, 1, print_file, kwargs=dict(arg_namespace=_arg))
        s.run()


def main(args):
    print_file(args)

if __name__ == '__main__':
    monkey.patch_all()
    parser = create_parser()
    args = parser.parse_args()
    main(args)
