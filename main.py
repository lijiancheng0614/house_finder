# -*- coding: utf-8 -*-
#
# @Author: lijiancheng0614
# @Date:   2020-03-06
#
"""main.
"""
import logging
import os

from src import model
from src.community_parser import get_community_by_region
from src.settings import CITY, OUTPUT_DIR, REGIONLIST

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    level=logging.INFO)


def main():
    """main.
    """
    model.init()
    community_output_dir = None
    if OUTPUT_DIR:
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        community_output_dir = os.path.join(OUTPUT_DIR, 'community')
        if not os.path.exists(community_output_dir):
            os.makedirs(community_output_dir)
    logging.info('get_community_by_region')
    for region_name in REGIONLIST:
        get_community_by_region(CITY, region_name, community_output_dir)


if __name__ == "__main__":
    main()
