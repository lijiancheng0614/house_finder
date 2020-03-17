# -*- coding: utf-8 -*-
#
# @Author: lijiancheng0614
# @Date:   2020-03-06
#
"""Utils.
"""
import logging
import random

import requests
from bs4 import BeautifulSoup

# flake8: noqa
HEADERS = [{
    'User-Agent':
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
}, {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'
}, {
    'User-Agent':
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'
}, {
    'User-Agent':
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'
}, {
    'User-Agent':
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'
}, {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'
}, {
    'User-Agent':
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'
}, {
    'User-Agent':
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'
}, {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'
}, {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'
}, {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'
}, {
    'User-Agent':
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'
}, {
    'User-Agent':
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'
}]  # noqa


def get_source_code(url):
    """Get source code.

    Args:
        url: str, url.

    Returns:
        str, source code.
    """
    try:
        result = requests.get(url,
                              headers=HEADERS[random.randint(
                                  0,
                                  len(HEADERS) - 1)])
        source_code = result.content
    except Exception as expection:
        logging.error(expection)
        return
    return source_code


def get_soup(url):
    """Get soup.

    Args:
        url: str, url.

    Returns:
        soup.
    """
    source_code = get_source_code(url)
    soup = BeautifulSoup(source_code, 'lxml')
    if soup.title.string == '414 Request-URI Too Large':
        logging.error('IP blocked, please verify captcha manually')
        return None
    return soup


def get_total_pages(url):
    """Get total pages.

    Args:
        url: str, url.

    Returns:
        int, total pages.
    """
    source_code = get_source_code(url)
    soup = BeautifulSoup(source_code, 'lxml')
    total_pages = 0
    try:
        page_info = soup.find('div', {'class': 'page-box house-lst-page-box'})
    except AttributeError as expection:
        logging.error(expection)
        page_info = None
    if not page_info:
        return 50
    page_info_str = page_info.get('page-data').split(',')[0]
    total_pages = int(page_info_str.split(':')[1])
    return total_pages
