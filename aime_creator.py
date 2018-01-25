"""
Download AIME tests from internet and generate a random AIME test for practice.

Args:
    folder(string): the filder to keep the files.
    csv(string)   : the csv file name
    html(string)  : the html file name for the generated AIME test.

Usage:
    Please refer to the test code.
"""
import os
import re
import pdb
import pickle
import random

from aime_parser import AIME_Parser

class AIME_Creator(object):
    def __init__(self, folder=None, csv=None, html=None, maxn=15):
        # set default parameters
        self._csv    = None
        self._folder = None
        self._html   = None

        # update self._csv 
        csv = 'AIME_Lib.csv'
        if csv and isinstance(csv, basestring):
            self._csv = csv

        # update self._folder
        if folder and isinstance(folder, basestring) and os.path.isdir(folder):
            self._folder = folder

        # update self._html for the html output file
        if html and isinstance(html, basestring):
            self._html = html

        # set the number of problems to be generated
        self._max = 15
        if isinstance(maxn, int) and maxn>0:
            self._max = maxn

    def _write_csv(self, data=None, csv=None):
        # update csv
        if csv is None:
            csv = self._csv

        # write data
        if csv and data and isinstance(csv, basestring) and isinstance(data,(list, tuple)):
            data0 = []

            # check if csv already exists
            if os.path.exists(csv):
                with open(csv, 'rb') as fd:
                    data0 = pickle.load(fd)

            # append the data and write to the csv file
            data0.extend(data)
            with open(csv, 'wb') as fd:
                pickle.dump(data0, fd)

    # Download AIME tests from internet and create a csv file for all tests.
    # Args:
    #   folder[string]: optional. It's the place to keep csv file.
    def create_csv(self, folder=None):
        # update folder
        if not (folder and isinstance(folder, basestring) and os.path.isdir(folder)):
            folder = self._folder
        else:
            self._folder = folder

        if folder is None: folder = '.'

        # walk thorough and parse aime txt files and keep the data
        for root, dirs, files in os.walk(folder, topdown=False):
            for name in files:
                if re.search('AIME.*.txt', name):
                    aime = AIME_Parser(os.path.join(root, name))
                    data = aime()
                    self._write_csv(data)

    # Create the actual AIME test in html format.
    # Args:
    #   html[string]: the actual generated html file name.
    #   maxn(int):    the number of problems in the test.
    def create_html(self, html=None, maxn=15):
        # update html
        if html is None:
            html = self._html

        # validate html
        if not (html and isinstance(html, basestring) and 'html' in html.lower()):
            print 'Invalid html'
            return

        while os.path.exists(html):
            num = re.search('\D*(\d*)\D*',html).group(1)
            if not num:
                tmp = list(os.path.splitext(html))
                tmp[0] += '0'
                html = ''.join(tmp)
            else:
                num1 = str(int(num) + 1)
                html = re.sub(num, num1, html)

        if isinstance(maxn, int) and maxn>0:
            self._max = maxn
        else:
            maxn = self._max

        # validate the csv file
        if not os.path.exists(self._csv):
            print 'No AIME library found.'
            return

        # load the AIME problems
        data = []
        with open(csv, 'rb') as fd:
            data = pickle.load(fd)

        # select problems randomly if the number of problems is greater than 15
        ndata = len(data)
        if ndata <= maxn:
            nproblems = range(ndata)
        else:
            nproblems = [random.randint(0,ndata-1) for p in range(0,maxn)]

        # generate the html file
        with open(html, 'w') as fp:
            for kk, vv in enumerate(nproblems):
                line   = data[vv]
                line0  = "<h2><span class=\"mw-headline\" id="
                line0 +="\"%s\">%d: %s</span></h2>"%(line[0], kk+1, line[0])
                fp.write(line0)
                fp.write(line[1])
                fp.write(line[2])
                fp.write("<p> </p>")
 
# test code
if __name__ == "__main__":
    csv = 'AIME_Lib.csv'
    aa = AIME_Creator(folder='.', html='aime_test.html', csv=csv)
    if not os.path.exists(csv):
        aa.create_csv()
    aa.create_html()