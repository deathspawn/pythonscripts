#!/usr/bin/python2.7
#
# Copyright (c) 2016 deathspawn
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#

import sys
from urllib import urlencode
from urllib2 import urlopen

try:
    arguments = sys.argv[1:]
except IndexError:
    exit("Error: Run "+sys.argv[0]+" <text to translate>")

def pirate(jargon):
    phrase = (" ".join(jargon))
    query = urlencode({ 'typing' : phrase.replace('<','{`{') })
    url = "http://postlikeapirate.com/AJAXtranslate.php?" + query
    doc = urlopen(url)
    response = doc.read().decode('utf8', 'ignore')
    response = response.replace('{`{','<').encode('utf8', 'ignore')
    return response

print pirate(arguments)
