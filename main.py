#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

from argparse import ArgumentParser, RawTextHelpFormatter
import codecs
import gevent
from gevent import monkey
import json
from datetime import datetime

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
    parser.add_argument('type', choices=['townCode', 'electorates', 'partyCode', 'counting_vote'],\
            help="type of collecting data\n"
                "- We DO NOT RECOMMAND to crawl TOWNCODE data: \n"
                "- KEC categorize townCode data by some rude standard, so we re-classify all the data by hand.") #'turnout'
    parser.add_argument('start', help="starting election id", type=float)
    parser.add_argument('end', help="ending election id", type=float,\
            nargs='?', default=None)

    parser.add_argument('-time', dest='filename_time', action='store_true',\
            help="Descript the crawling moment time info in filename.")
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

def main(args):
    printer = print_csv if args.test else print_json
    encoding = args.encoding
    filetype = 'csv' if args.test else 'json'
    datadir = args.directory if args.directory \
                else './crawled_data/%s/%s' % (args.target, args.type)
    time_string = datetime.today().strftime("%Y%m%d%H%M%S")
    check_dir(datadir)

    if args.filename_time:
        if args.target=='local':
            if args.end:
                jobs = []
                args.level = get_election_type_name(args.level)
                for n in range(args.start, args.end+1):
                    filename = '%s/%s-%s-%s-%d-%s.%s'\
                        % (datadir, args.target, args.level, args.type, n, time_string, filetype)
                    job = gevent.spawn(crawl, target=args.target, level=args.level,\
                        _type=args.type, nth=n, filename=filename, encoding=encoding, printer=printer)
                    jobs.append(job)
                gevent.joinall(jobs)
            else:
                n = args.start
                args.level = get_election_type_name(args.level)
                filename = '%s/%s-%s-%s-%.01f-%s.%s' %\
                        (datadir, args.target, args.level, args.type, n, time_string, filetype)
                crawl(target=args.target, level=args.level, _type=args.type, nth=n,\
                            filename=filename, encoding=encoding, printer=printer)
        else:
            if args.end:
                jobs = []
                for n in range(args.start, args.end+1):
                    filename = '%s/%s-%s-%d-%s.%s'\
                            % (datadir, args.target, args.type, n, time_string, filetype)
                    job = gevent.spawn(crawl, target=args.target, _type=args.type, nth=n,\
                            filename=filename, encoding=encoding, printer=printer)
                    jobs.append(job)
                gevent.joinall(jobs)
            else:
                n = args.start
                filename = '%s/%s-%s-%.01f-%s.%s' %\
                        (datadir, args.target, args.type, n, time_string, filetype)
                crawl(target=args.target, _type=args.type, nth=n,\
                            filename=filename, encoding=encoding, printer=printer)

    else:
        if args.target=='local':
            if args.end:
                jobs = []
                args.level = get_election_type_name(args.level)
                for n in range(args.start, args.end+1):
                    filename = '%s/%s-%s-%s-%d.%s'\
                        % (datadir, args.target, args.level, args.type, n, filetype)
                    job = gevent.spawn(crawl, target=args.target, level=args.level,\
                        _type=args.type, nth=n, filename=filename, encoding=encoding, printer=printer)
                    jobs.append(job)
                gevent.joinall(jobs)
            else:
                n = args.start
                args.level = get_election_type_name(args.level)
                filename = '%s/%s-%s-%s-%.01f.%s' %\
                        (datadir, args.target, args.level, args.type, n, filetype)
                crawl(target=args.target, level=args.level, _type=args.type, nth=n,\
                            filename=filename, encoding=encoding, printer=printer)
        else:
            if args.end:
                jobs = []
                for n in range(args.start, args.end+1):
                    filename = '%s/%s-%s-%d.%s'\
                            % (datadir, args.target, args.type, n, filetype)
                    job = gevent.spawn(crawl, target=args.target, _type=args.type, nth=n,\
                            filename=filename, encoding=encoding, printer=printer)
                    jobs.append(job)
                gevent.joinall(jobs)
            else:
                n = args.start
                filename = '%s/%s-%s-%.01f.%s' %\
                        (datadir, args.target, args.type, n, filetype)
                crawl(target=args.target, _type=args.type, nth=n,\
                            filename=filename, encoding=encoding, printer=printer)


    print('Data written to %s' % filename)

if __name__ == '__main__':
    monkey.patch_all()
    parser = create_parser()
    args = parser.parse_args()
    main(args)
