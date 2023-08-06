# -*- coding: utf-8 -*-

__author__ = 'Johannes Ahlmann'
__email__ = 'johannes@fluquid.com'
__version__ = '0.4.0'

"""
audit whether spam bots are able to extract your email addresses from your
    websites

TODO:
* match emails across newlines (re.M) and unicode?
"""

import re
import logging
from six.moves.urllib.parse import unquote

from html_to_etree import parse_html_unicode, parse_html_bytes
from html_text import extract_text
import js2py
from lxml import etree

import six
if six.PY2:
    from HTMLParser import HTMLParser
else:
    from html.parser import HTMLParser

logging.basicConfig(level=logging.INFO)
HTML_PARSER = HTMLParser()

"""
sources:
- http://stackoverflow.com/a/38787343
- http://stackoverflow.com/a/2049510
"""
EMAIL_RE = re.compile(
    r"""[\w!#$%&\'*+\-/=?^_`{|}~\.]
        {1,}
        @
        [\w\-\.]
        {1,}
        \.
        \w{2,}
    """,
    flags=re.UNICODE | re.VERBOSE)

MAILTO_RE = re.compile(
    r'^mailto:(.*)', flags=re.U)

AT_PATTERN = r'\bat\b|\[at\]|\(at\)|\(@\)|@'
AT_RE = re.compile(r' ?(?:%s) ?' % (AT_PATTERN, ), flags=re.I)
SPACE_RE = re.compile(r'\s', flags=re.I)
DOT_PATTERN = r'\bdot\b|\[dot\]|\(dot\)|\.'
DOT_RE = re.compile(r' ?(?:%s) ?' % (DOT_PATTERN, ), flags=re.I)
AT_DOT_RE = re.compile(
    r"""
    [\w!#$%&\'*+\-/=?^_`{|}~\.]{1,}
    \ ?
    (?:""" + AT_PATTERN + r""")
    \ ?
    [\w\-\.]{1,}
    \ ?
    (?:""" + DOT_PATTERN + r""")
    \ ?
    [\w\.]{2,}
    """,
    flags=re.UNICODE | re.VERBOSE | re.I)
IS_HEX = re.compile(r'^[0-9a-f]+$', flags=re.I)

X_A_HREF = etree.XPath('//a[@href]')
CF_EMAIL = etree.XPath('//*[@data-cfemail]')
ITEMPROP = etree.XPath('//*[@itemprop="email"]')

# taken directly from cloudflare enabled sites and wrapped as a function
# TODO: with minimal DOM simulation, could use script as is...
# NOTE: added ">0" in loop condition to prevent infinite loop
# FIXME: need to fuzz "cflare" function to prevent loops, or timeout!
cflare = js2py.eval_js(
    'function(a) {'

    """for(e='',r='0x'+a.substr(0,2)|0,n=2;a.length-n>0;n+=2)
         e+='%'+('0'+('0x'+a.substr(n,2)^r).toString(16)).slice(-2);"""

    'return e }'
)


def audit_text(text):
    """ look for email addresses in plain unicode text """
    # FIXME: performance? counter-indications?
    text = HTML_PARSER.unescape(unquote(text))

    for match in EMAIL_RE.finditer(text):
        logging.debug('audit_text EMAIL_RE yielding "%s"', match.group(0))
        yield match.group(0)

    for match in AT_DOT_RE.finditer(text):
        res = match.group(0)
        # FIXME: better way in regex?
        # FIXME: why?
        if not EMAIL_RE.match(res) and 'at the dot' not in res:
            mail = AT_RE.sub('@', DOT_RE.sub('.', res))
            logging.debug('AT_DOT_RE "%s"', mail)
            if EMAIL_RE.match(mail):
                logging.debug('audit_text AT_DOT_RE yielding "%s"', mail)
                yield mail


def audit_etree(tree):
    """
    look for email addresses in html DOM as well as text generated from DOM
    """
    # FIXME: pre-compile xpath queries
    logging.debug('audit_etree')

    logging.debug('ITEMPROP')
    for tag in ITEMPROP(tree):
        content = tag.get('content')
        if content:
            logging.debug('etree ITEMPROP yielding "%s"', content)
            yield content

    logging.debug('CF_EMAIL')
    for tag in CF_EMAIL(tree):
        cfemail = tag.get('data-cfemail')
        if cfemail and IS_HEX.match(cfemail) and len(cfemail) % 2 == 0:
            val = unquote(cflare(cfemail)).strip()
            if val:
                logging.debug('etree CF_EMAIL yielding "%s"', val)
                yield val

    logging.debug('X_A_HREF')
    for a_tag in X_A_HREF(tree):
        href = a_tag.get('href')
        unesc = HTML_PARSER.unescape(unquote(href))
        match = MAILTO_RE.search(unesc)
        if match:
            logging.debug('etree CF_EMAIL yielding "%s"', match.group(1))
            yield match.group(1)

        cfemail = a_tag.get('data-cfemail')
        if cfemail and IS_HEX.match(cfemail) and len(cfemail) % 2 == 0:
            val = unquote(cflare(cfemail))
            logging.debug('etree CF_EMAIL yielding "%s"', val)
            yield val

    logging.debug('extract_text')
    text = extract_text(tree)
    for item in audit_text(text):
        yield item


def audit_html_unicode(body):
    """ audit html with given unicode html body """
    logging.debug('parse_html_unicode')
    tree = parse_html_unicode(body)
    return audit_etree(tree)


def audit_html_bytes(body, content_type=''):
    """ audit html with given bytestring body and header content_type """
    logging.debug('parse_html_bytes')
    tree = parse_html_bytes(body, content_type)
    return audit_etree(tree)
