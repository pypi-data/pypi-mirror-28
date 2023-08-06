# -*- coding: utf-8 -*-
# Python2 compat
from __future__ import unicode_literals, print_function, division
try:
    input = raw_input
except NameError:  # python3
    pass

# Local imports
from .definitions import bcolors, journalAbbrevs

import ads
import argparse
import re
import sh
import os
import configparser

from appdirs import user_config_dir


def getConfig():
    config_file = os.path.join(user_config_dir('adsquery'), 'adsqueryrc')
    config = configparser.ConfigParser()
    config['adsquery'] = {
        'data_dir': '~/ADS',
        'pdf_viewer': 'evince'
    }
    config.read(config_file)
    return config


class BuildQuery:

    def __init__(self):
        "Creates a build object query"
        self.query = dict()
        return

    def setKey(self, key, val):
        '''Set the key to val in the query'''
        if val is not None:
            self.query[key] = val

    def execute(self):
        try:
            return ads.SearchQuery(**self.query)
        except AssertionError:
            return []


def createQueryParser(parser):
    parser.description = """Example:

    adsquery query --first-author Einstein relativity
    adsquery query "Gravitational wave" --year 2015
    """
    query_param = parser.add_argument_group('Query parameters')

    query_param.add_argument(metavar='query', dest='q', type=str, nargs='*',
                             help=('The search query. Can be either fielded '
                                   '(field:value) or unfielded (value).'))
    query_param.add_argument('--rows', type=int, default=50,
                             help="number of results to return.")
    query_param.add_argument('--start', type=int, default=1,
                             help=("starting point for returned results (for"
                                   " pagination)."))
    query_param.add_argument('--fl', nargs='*',
                             help=("Fields list: specify the fields contained"
                                   " each returned document. Value should be a"
                                   " comma-separated list of field names."))
    query_param.add_argument('--fq',
                             help=("Filter query: filter your results using"
                                   " in a particular field:value condition."
                                   " This parameter is repeatable."))
    query_param.add_argument('--sort', type=str, help='Sort using this field')

    fields = parser.add_argument_group('Fields')
    fields.add_argument('--abstract',
                        help='the abstract of the record')
    fields.add_argument('--ack',
                        help='the acknowledgements section of an article')
    fields.add_argument('--aff',
                        help='an array of the authors affiliations')
    fields.add_argument('--alternate_bibcode',
                        help='list of alternate bibcodes for a single record')
    fields.add_argument('--alternate_title',
                        help=('list of alternate titles for a single record '
                              '(usually if they are in multiple languages)'))
    fields.add_argument('--arxiv_class',
                        help='the arXiv class the pre-print was submitted to')
    fields.add_argument('--author',
                        help=('an array of the author names associated with'
                              ' the record'))
    fields.add_argument('--bibcode',
                        help=('the canonical ADS bibcode identifier for this'
                              ' record'))
    fields.add_argument('--bibgroup',
                        help=('the bibliographic groups that the bibcode has'
                              ' been associated with'))
    fields.add_argument('--bibstem',
                        help=('the abbreviated name of the journal or,'
                              ' publication e.g., ApJ.'))
    fields.add_argument('--body',
                        help='the full text content of the article')
    fields.add_argument('--citation_count',
                        help='number of citations the item has received')
    fields.add_argument('--copyright',
                        help='the copyright applied to the article')
    fields.add_argument('--data',
                        help=('the list of sources that have data related to'
                              ' this bibcode'))
    fields.add_argument('--database',
                        help='Which database the record is associated with.')
    fields.add_argument('--doi',
                        help='the digital object identifier of the article')
    fields.add_argument('--doctype',
                        help=('the type of document it is (see here for a list'
                              ' of doctypes)'))
    fields.add_argument('--first-author',
                        help='the first author of the article')
    fields.add_argument('--grant',
                        help=('the list of grant IDs and agencies noted within'
                              ' an article'))
    fields.add_argument('--id',
                        help=('a (non-persistent) unique integer for this'
                              ' record, used for fast look-up of a document'))
    fields.add_argument('--identifier',
                        help=('an array of alternative identifiers for the'
                              ' record. May contain alternative bibcodes, DOIs'
                              ' and/or arxiv ids.'))
    fields.add_argument('--indexstamp',
                        help='time at which the document was (last) indexed')
    fields.add_argument('--issue',
                        help='issue the record appeared in')
    fields.add_argument('--keyword',
                        help=('an array of normalized and un-normalized'
                              ' keyword values associated with the record'))
    fields.add_argument('--lang*',
                        help='the language of the article s title')
    fields.add_argument('--orcid-pub',
                        help='ORCiD iDs supplied by publishers')
    fields.add_argument('--orcid-user',
                        help='ORCiD iDs supplied by knonwn users in the ADS')
    fields.add_argument('--orcid-other',
                        help=('ORCiD iDs supplied by anonymous users in the'
                              ' ADS'))
    fields.add_argument('--page',
                        help='starting page')
    fields.add_argument('--property',
                        help=('an array of miscellaneous flags associated with'
                              ' the record (see here for a list of '
                              'properties'))
    fields.add_argument('--pub',
                        help=('the canonical name of the publication the'
                              ' record appeared in'))
    fields.add_argument('--pubdate',
                        help=('publication date in the form YYYY-MM-DD (DD '
                              'value will always be "00")'))
    fields.add_argument('--read-count',
                        help=('number of times the record has been viewed '
                              'within in a 90-day windows (ads and arxiv)'))
    fields.add_argument('--title',
                        help='the title of the record')
    fields.add_argument('--vizier',
                        help='the subject tags given to the article by VizieR')
    fields.add_argument('--volume',
                        help='volume the record appeared in')
    fields.add_argument('--year',
                        help='the year the article was published')


def createGetParser(parser):
    """

    """
    parser.add_argument('--bibcode',
                        help=('the canonical ADS bibcode identifier for '
                              'this record'))
    return


def createBibParser(parser):
    """

    """
    return


def printResults(results):
    for i, res in enumerate(results):

        # Format author
        if res.author is not None and len(res.author) > 3:
            authors = res.author[0] + \
                ' et al. ({} more)'.format(len(res.author[1:]))
        elif res.author is None:
            authors = 'No author'
        else:
            authors = ', '.join(res.author)

        # Format journal
        pub = res.pub
        if pub in journalAbbrevs:
            pub = journalAbbrevs[pub]

        if pub is None:
            pub = '?'

        # Format year journal
        print('{c.HEADER}[{i}]: {c.OKGREEN}{year}, {pub} — {c.OKBLUE}'
              '{author}{c.ENDC}, {title}'.format(
                  i=i, year=res.year, title=res.title[0], author=authors,
                  c=bcolors, pub=pub))


def doQuery(args, config, **kwargs):
    query = BuildQuery()

    query.setKey('sort', 'citation_count')
    for key in vars(args):
        if key not in ['interactive', 'func']:
            query.setKey(key, vars(args)[key])
    for key in kwargs:
        if key not in ['interactive', 'func']:
            query.setKey(key, kwargs[key])

    fl = ['abstract', 'first_author', 'author', 'year', 'pub',
          'title', 'bibcode']
    query.setKey('fl', fl)

    # get results
    results = query.execute()

    res_as_array = []

    # loop over results
    try:  # sometimes, the ads script gets an IndexError, hide this
        res_as_array = [res for res in results]
    except IndexError:
        res_ar_array = []
    printResults(res_as_array)

    if len(res_as_array) == 0:
        print('No results')
        return

    if args.interactive or ('interactive' in kwargs and kwargs['interactive']):
        print('')
        inp = input(
            'Comma separated articles to download [e.g. 1-3, 4], [m] for more'
            ' [q] to quit or'
            ' add more parameters to request [e.g. year:2016]: ')

        # Match quit request
        if inp == 'q':
            return

        # Match requests for more articles
        # match any string like "5m", "10 more", …
        grp = re.match('(\d+) ?[mM](ore)?', inp)
        if grp is not None:
            nmore = int(grp.group(1))

            # load more
            if 'rows' in kwargs:
                kwargs['rows'] += nmore
            else:
                kwargs['rows'] = 50 + nmore

            print('Loading {} more!'.format(nmore))
            doQuery(args, **kwargs)
            return

        # Match selection
        mask = parseAsList(inp)
        if len(mask) > 0:
            papers = [r for i, r in enumerate(res_as_array) if i in mask]
            print('Selected:')
            printResults(papers)

            action = getInput(
                'Download [d], bibtex[b], quit[q]? ', lambda e: e.lower())

            # Download selected articles
            if 'd' in action:
                for paper in papers:
                    print('Downloading "{}"'.format(paper.title[0]))
                    downloadPaper(paper, config)

            # Get bibtex reference
            if 'b' in action:
                try:
                    import pyperclip
                    clip = True
                except ModuleNotFoundError:
                    clip = False

                print('Downloading bibtex entries')
                # Get the list of bibcodes
                bibcodes = [p.bibcode for p in papers]
                eq = ads.ExportQuery(bibcodes)
                bib = eq.execute()
                print(bib)
                if clip:
                    print('Copied to clipboard!')
                    pyperclip.copy(bib)

            return papers

        else:  # match more request
            if args.q is not None:
                args.q = args.q + ' ' + inp
            elif 'q' in kwargs:
                kwargs['q'] += ' ' + inp
            else:
                kwargs['q'] = inp
            doQuery(args, **kwargs)
            return
    else:
        return res_ar_array


def downloadPaper(paper, config):
    '''Download the paper.

    Params
    ------
    :arg paper
        A `Paper` instance result given by the ads'''

    def open_file(fname):
        sh.Command(config['adsquery']['pdf_viewer'])(fname, _bg=True)

    def process_output(line):
        print(line, end='')

    if paper.pub == 'ArXiv e-prints':
        # Get the ArXiv name
        _id = paper.bibcode.split('arXiv')[1][:-1]
        _id = _id[:4] + '.' + _id[4:]
        url = 'https://arxiv.org/pdf/{id}'.format(id=_id)
    else:
        url = ("http://adsabs.harvard.edu/cgi-bin/nph-data_query?"
               "bibcode={paper.bibcode}&link_type=ARTICLE".format(
                   paper=paper))

    print(f'Downloading {url}')

    fname = '{paper.bibcode}_{author}.pdf'.format(
        paper=paper,
        author=paper.first_author.split(',')[0])

    filesDir = os.path.join(os.path.expanduser('~'), 'ADS')
    # create the directory of not existing
    if not os.path.isdir(filesDir):
        os.path.mkdir(filesDir)

    fname = os.path.join(filesDir, fname)

    if os.path.isfile(fname):
        ans = getInput('File already exists on disk. Overwrite [Y/n]?',
                       lambda e: e.lower() if e.lower() in ['y', 'n', '']
                       else None)
        if ans == 'n':
            open_file(fname)
            return

    sh.wget(url,
            header="User-Agent: Mozilla/5.0 (Windows NT 5.1; rv:23.0) Gecko/20100101 Firefox/23.0",
            O=fname,
            _out=process_output)
    print('Downloaded into %s' % fname)
    open_file(fname)



def getInput(help_string, parse_fun):
    valid = False
    while not valid:
        try:
            ret = input(help_string)
            ret_parsed = parse_fun(ret)
            valid = ret_parsed is not None
        except ValueError:
            valid = False

    return ret_parsed


def parseAsList(string):
    '''Parse the input as a list

    :param string
    the string to parse

    :return
    a list containing the input from the user
    '''
    # prompt for article to download
    dl_input = string

    # split around commas (with blanks)
    dl_input = re.split('\s?,\s?', dl_input)
    mask = []
    regexp = re.compile('(\d+)(-(\d+))?')
    for inp in dl_input:
        match = regexp.match(inp)
        if match is None:
            return []

        beg, end = match.group(1, 3)
        if end is None:
            mask.append(int(beg))
        else:
            mask += range(int(beg), int(end) + 1)
    return mask


def doGet(args, config):
    raise NotImplementedError

def doBib(args, config):
    raise NotImplementedError


def interactive():
    config = getConfig()
    parser = argparse.ArgumentParser(description='Get papers from the ADS')
    parser.add_argument('--no-interactive', help='Deactivate interaction',
                        dest='interactive', action='store_false')
    parser.add_argument('--token', type=str,
                        help=('Your ADS token. Leave empty to use the value '
                              'from ~/.ads/dev_key or from the environment '
                              'variable ADS_DEV_KEY.'),
                        default=None)

    subparsers = parser.add_subparsers()
    query_parser = subparsers.add_parser('query', description='Query the ADS')
    createQueryParser(query_parser)
    query_parser.set_defaults(func=doQuery)

    get_parser = subparsers.add_parser(
        'get', description='Get a paper from the ADS')
    createGetParser(get_parser)
    get_parser.set_defaults(func=doGet)

    bib_parser = subparsers.add_parser(
        'bib', description='Get bib data from the ADS')
    createBibParser(bib_parser)
    bib_parser.set_defaults(func=doBib)

    args = parser.parse_args()
    if 'q' in vars(args):
        args.q = ' '.join(args.q)

    try:
        return args.func(args, config)
    except AttributeError:  # func not in namespace
        parser.print_help()
        return


def main():
    '''A simple wrapper that's catching C-c'''
    try:
        interactive()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
