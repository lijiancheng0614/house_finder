# -*- coding: utf-8 -*-
#
# @Author: lijiancheng0614
# @Date:   2020-03-06
#
"""main.
"""
import codecs
import json
import logging
import os

from peewee import fn
from src import model
from src.community_parser import get_community_by_region
from src.model import Community
from src.settings import CITY, OUTPUT_DIR, REGIONLIST

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    level=logging.INFO)


def generate_bizcircle_website(data_dir='web/data'):
    """Generate bizcircle website.

    Args:
        data_dir: str, data directory.
    """
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    # get bizcircle
    stats = Community.select(Community.bizcircle, fn.Count(
        Community.bizcircle)).group_by(Community.bizcircle).tuples()
    communities_all = list()
    for bizcircle, _ in stats:
        communities = list(
            Community.select(
                Community.title, Community.link, Community.tags,
                Community.onsale, Community.onrent, Community.building_number,
                Community.house_number, Community.average_unit_price,
                Community.building_finish_year, Community.built_area,
                Community.covered_area, Community.house_type,
                Community.property_right_years, Community.building_type,
                Community.development_company, Community.trading_right,
                Community.property_management_company,
                Community.property_management_cost,
                Community.property_management_phone_number,
                Community.heating_type, Community.heating_cost,
                Community.water_use_type, Community.power_consumption_type,
                Community.parking_place_number, Community.parking_cost,
                Community.gas_cost, Community.volume_ratio,
                Community.green_coverage,
                Community.separation_pedestrian_vehicular, Community.close,
                Community.elevator, Community.nearby_schools, Community.score,
                Community.score_building_quality,
                Community.score_apartment_layout_design,
                Community.score_traffic_condition,
                Community.score_education_quality,
                Community.score_business_environment,
                Community.score_garden_View,
                Community.score_property_management,
                Community.is_swimming_pool, Community.is_community_garden,
                Community.is_sports_ground, Community.is_recreational_facility,
                Community.is_club, Community.is_gym, Community.is_lobby,
                Community.is_activity_center, Community.is_river_system,
                Community.is_playground).where(
                    Community.bizcircle == bizcircle).tuples())
        communities_all += communities
        output_path = os.path.join(data_dir, u'{}.txt'.format(bizcircle))
        json.dump({'data': communities},
                  codecs.open(output_path, 'w', 'utf-8'),
                  indent=4,
                  sort_keys=True,
                  ensure_ascii=False)
    output_path = os.path.join(data_dir, u'bizcircle.txt')
    json.dump({'data': list(stats)},
              codecs.open(output_path, 'w', 'utf-8'),
              indent=4,
              sort_keys=True,
              ensure_ascii=False)
    output_path = os.path.join(data_dir, u'all.txt')
    json.dump({'data': communities_all},
              codecs.open(output_path, 'w', 'utf-8'),
              indent=4,
              sort_keys=True,
              ensure_ascii=False)


def main():
    """main.
    """
    # init
    model.init()
    community_output_dir = None
    if OUTPUT_DIR:
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        community_output_dir = os.path.join(OUTPUT_DIR, 'community')
        if not os.path.exists(community_output_dir):
            os.makedirs(community_output_dir)
    # get data
    logging.info('get_community_by_region')
    for region_name in REGIONLIST:
        get_community_by_region(CITY, region_name, community_output_dir)
    # generate web
    logging.info('generate_bizcircle_website')
    generate_bizcircle_website()


if __name__ == "__main__":
    main()
