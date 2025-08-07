# -*- coding: utf-8 -*-
#
# @Author: lijiancheng0614
# @Date:   2020-03-06
#
"""Zhujianwei parser.
"""
import argparse
import json
import logging
import re

from utils import get_soup

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    level=logging.INFO)


def get_args():
    """Get arguments.

    Returns:
        Namespace: arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--urls',
        type=dict,
        default={
            u'1#地下车库':
            'http://bjjs.zjw.beijing.gov.cn/eportal/ui?pageId=320833&systemId=2&categoryId=1&salePermitId=7240988&buildingId=508627'
            # u'6#住宅及商业楼':
            # 'http://bjjs.zjw.beijing.gov.cn/eportal/ui?pageId=320833&systemId=2&categoryId=1&salePermitId=7240988&buildingId=508626',
            # u'7#住宅楼':
            # 'http://bjjs.zjw.beijing.gov.cn/eportal/ui?pageId=320833&systemId=2&categoryId=1&salePermitId=7240988&buildingId=508605'
        },
        help='Urls.')
    parser.add_argument('--output_path',
                        default='house_info/house_info-1.json',
                        help='Output path.')
    args = parser.parse_args()
    return args


def get_house_info(url):
    """Get house info.

    Args:
        url (str): url.

    Returns:
        dict: results.
    """
    results = dict()
    soup = get_soup(url)
    if not soup:
        logging.warning('Cannot parse %s', url)
        return results
    items = soup.find_all('td', {'id': 'desc'})
    for item in items[::2]:
        key = re.sub('[ \r\n\t]', '', item.text)
        value = re.sub('[ \r\n\t]', '', item.next_sibling.next_sibling.text)
        results[key] = value
    return results


def get_building_info(url):
    """Get building info.

    Args:
        url (str): url.

    Returns:
        dict: results.
    """
    results = list()
    soup = get_soup(url)
    if not soup:
        logging.warning('Cannot parse %s', url)
        return list()
    # items = soup.find_all('span', {'class': 'f12a6'})
    items = soup.find_all(
        'div', {
            'style':
            'width:130px;background:#33CC00;float:left;border: 1px solid white;margin: 1px 1px 0 0;'
        })
    if items:
        for item in items:
            # item = item.next_sibling.next_sibling
            item = list(item.children)[1]
            url = 'http://bjjs.zjw.beijing.gov.cn' + item.get('href')
            house_info = get_house_info(url)
            house_info['url'] = url
            results.append(house_info)
    return results


def show_building_info(building_info):
    """Show building info.

    Args:
        building_info (list): building info.
    """
    # 戊类仓储用房：25723.30元/平
    unit_price2 = 25723.30
    floor_info = dict()
    for house_info in building_info:
        floor_id = int(house_info[u'房间号'].split('-')[-1][:-2])
        if floor_id not in floor_info:
            floor_info[floor_id] = list()
        unit_price = ''
        if u'按建筑面积拟售单价' in house_info:
            unit_price = house_info[u'按建筑面积拟售单价']
        elif u'住宅按建筑面积拟售单价' in house_info:
            unit_price = house_info[u'住宅按建筑面积拟售单价']
        unit_price = unit_price.replace(u'元/平方米', '')
        area = ''
        if u'建筑面积' in house_info:
            area = house_info[u'建筑面积']
        elif u'住宅建筑面积' in house_info:
            area = house_info[u'住宅建筑面积']
            if u'戊类仓储用房建筑面积' in house_info:
                area += '+' + house_info[u'戊类仓储用房建筑面积']
        area = area.replace(u'平方米', '')
        total_price = 0
        if '+' in area:
            area1, area2 = map(float, area.split('+'))
            total_price = area1 * float(unit_price) + area2 * unit_price2
        elif area != '':
            total_price = float(area) * float(unit_price)
        floor_info[floor_id].append(
            [house_info[u'房间号'], unit_price, area, total_price])
    print(u'单价')
    list_floor_id = sorted(list(floor_info.keys()), reverse=True)
    for floor_id in list_floor_id:
        floor = sorted(floor_info[floor_id], reverse=True)
        print(' '.join([
            '{}({})'.format(house_info[0], house_info[1])
            for house_info in floor
        ]))
    print(u'面积')
    for floor_id in list_floor_id:
        floor = sorted(floor_info[floor_id], reverse=True)
        print(' '.join([
            '{}({})'.format(house_info[0], house_info[2])
            for house_info in floor
        ]))
    print(u'总价(万)')
    for floor_id in list_floor_id:
        floor = sorted(floor_info[floor_id], reverse=True)
        print(' '.join([
            '{}({:.2f})'.format(house_info[0], house_info[3] / 10000)
            for house_info in floor
        ]))
    print(u'总价')
    for floor_id in list_floor_id:
        floor = sorted(floor_info[floor_id], reverse=True)
        print(' '.join([
            '{}({:.2f})'.format(house_info[0], house_info[3])
            for house_info in floor
        ]))


def get_data(urls, output_path):
    """Get data.

    Args:
        urls (list): urls.
        output_path (str): output path.
    """
    results = dict()
    for name, url in urls.items():
        building_info = get_building_info(url)
        results[name] = building_info
    # output
    fid = open(output_path, 'w')
    json.dump(results, fid, indent=4, sort_keys=True, ensure_ascii=False)
    fid.close()


def main():
    """main.
    """
    args = get_args()
    # get_data(args.urls, args.output_path)
    results = json.load(open(args.output_path))
    # show
    for name, building_info in results.items():
        if name.endswith('地下车库'):
            continue
        print(name)
        show_building_info(building_info)
        print('\n')


if __name__ == "__main__":
    main()
