# -*- coding: utf-8 -*-
#
# @Author: lijiancheng0614
# @Date:   2020-03-06
#
"""Community parser.
"""
import codecs
import json
import logging
import os
import re
import time
import traceback

import model
from utils import get_soup, get_total_pages


def get_mobile_link(link, city):
    """Get mobile link.

    Args:
        link: str, link.
        city: str, city.

    Returns:
        str, mobile link.
    """
    link = link.split('/')
    link[1] = '/' + link[2].replace(city, 'm')
    link[2] = city
    link = '/'.join(link)
    return link


def get_community_by_region(city='bj',
                            region_name='chaoyang',
                            output_dir=None):
    """Get community by region.

    Args:
        city: str, city.
        region_name: str, region name.
    """
    url = 'https://{}.ke.com/xiaoqu/{}/'.format(city, region_name)
    soup = get_soup(url)
    if not soup:
        return
    total_pages = get_total_pages(url)
    if not total_pages:
        logging.error('Finish at %s', model.Community.select().count())
        return
    for page in range(total_pages):
        if page > 0:
            url_page = '{}pg{}/'.format(url, page)
            soup = get_soup(url_page)
            if not soup:
                return
        name_list = soup.find_all('li', {'class': 'clear'})
        logging.info('%s %d / %d', region_name, page + 1, total_pages)
        for name in name_list:
            info = dict()
            try:
                item = name.find('div', {'class': 'title'})
                link = item.a.get('href')
                title = item.get_text().strip('\n')
                logging.info('%s', title)
                info['title'] = title
                link = get_mobile_link(link, city)
                info['link'] = link
                info['community_id'] = name.get('data-housecode')
                item = name.find('a', {'class': 'district'})
                if item:
                    info['district'] = item.get_text()
                item = name.find('a', {'class': 'bizcircle'})
                if item:
                    info['bizcircle'] = item.get_text()
                item = name.find('div', {'class': 'tagList'})
                if item:
                    info['tags'] = item.get_text().strip('\n')
                item = name.find('a', {'class': 'totalSellCount'})
                if item:
                    info['onsale'] = item.span.get_text().strip('\n')
                item = name.find('a', {'title': title + u'租房'})
                if item:
                    info['onrent'] = item.get_text().strip('\n').split(u'套')[0]
                item = name.find('div', {'class': 'totalPrice'})
                if item:
                    info['average_unit_price'] = item.span.get_text().strip(
                        '\n')
                output_path = os.path.join(output_dir,
                                           u'{}.json'.format(title))
                community_info = get_community_info_by_url(link, output_path)
                for key, value in community_info.items():
                    info[key] = value
            except Exception as expection:
                logging.error(expection)
                logging.error(traceback.format_exc())
                continue
            model.Community.replace(**info).execute()
        time.sleep(1)


def get_community_info_by_url(url, output_path=None):
    """Get community info by url.

    Args:
        url: str, url.

    Returns:
        dict, results.
    """
    results = dict()
    soup = get_soup(url)
    if not soup:
        logging.warn('Cannot parse %s', url)
        return results
    pattern = re.compile('window.__PRELOADED_STATE__ = (.*);',
                         re.MULTILINE | re.DOTALL)
    items = soup.find('script', {'type': 'text/javascript'}, text=pattern)
    if items:
        items = pattern.search(items.text).group(1)
        items = json.loads(items)
        if output_path:
            json.dump(items,
                      codecs.open(output_path, 'w', 'utf-8'),
                      indent=4,
                      sort_keys=True,
                      ensure_ascii=False)
        items = items['xiaoquDetail']['survey']
        if isinstance(items, dict):
            items = items.values()
        for item in items:
            name = item['name']
            name = model.Community.NAME_DICT[name]
            value = unicode(item['value'])
            results[name] = value
    # gonglueV2.html
    url += 'gonglueV2.html'
    soup = get_soup(url)
    if not soup:
        logging.warn('Cannot parse %s', url)
        return results
    items = soup.find_all('span', {'class': 'txt_gray'})
    if items:
        for item in items:
            name = item.get_text().strip(u'：')
            name = model.Community.NAME_DICT[name]
            if name in results:
                continue
            value = unicode(item.next_sibling)
            results[name] = value
    # intro
    item = soup.find('div', {'class': 'cpt_content_section'})
    if item:
        results['intro'] = item.get_text().strip('\n')
    # score
    item = soup.find('div', {'class': 'review_score'})
    if item:
        value = float(item.next_element)
        results['score'] = value
    item = soup.find('ul', {'class': 'review_list'})
    if item:
        items = item.find_all('li')
        if items:
            for item in items:
                name = item.get_text().replace('\n', '').split()
                value = float(name[1].strip(u'分'))
                name = model.Community.NAME_DICT[name[0]]
                if name in results:
                    continue
                results[name] = value
    # review
    item = soup.find('div', {'id': 'review_good'})
    if item:
        value = item.get_text().strip('\n').strip(u'小区优点').strip('\n')
        results['good_point'] = value
    item = soup.find('div', {'id': 'review_bad'})
    if item:
        value = item.get_text().strip('\n').strip(u'小区弱点').strip('\n')
        results['bad_point'] = value
    # sheshi_cell
    items = soup.find_all('div', {'class': 'sheshi_cell'})
    if items:
        for item in items:
            name = item.p.get_text()
            name = model.Community.NAME_DICT[name]
            value = item.img['src'].split('/')[-1].split('.')[0].split('_')[-1]
            value = value[0] != 'n'
            results[name] = value
    return results
