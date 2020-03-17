# -*- coding: utf-8 -*-
#
# @Author: lijiancheng0614
# @Date:   2020-03-06
#
"""Model.
"""
import datetime

from peewee import (BigIntegerField, BooleanField, CharField, CompositeKey,
                    DateTimeField, FloatField, Model, MySQLDatabase,
                    PostgresqlDatabase, SqliteDatabase)
from settings import DBENGINE, DBHOST, DBNAME, DBPASSWORD, DBPORT, DBUSER

if DBENGINE.lower() == 'sqlite3':
    DATABASE = SqliteDatabase(DBNAME)
elif DBENGINE.lower() == 'mysql':
    DATABASE = MySQLDatabase(
        DBNAME,
        host=DBHOST,
        port=DBPORT,
        user=DBUSER,
        passwd=DBPASSWORD,
        charset='utf8',
        use_unicode=True,
    )
elif DBENGINE.lower() == 'postgresql':
    DATABASE = PostgresqlDatabase(
        DBNAME,
        user=DBUSER,
        password=DBPASSWORD,
        host=DBHOST,
        charset='utf8',
        use_unicode=True,
    )
else:
    raise AttributeError("Please setup DBENGINE at settings.py")


class BaseModel(Model):
    """Base model.
    """
    class Meta:
        """Meta.
        """
        database = DATABASE


class Community(BaseModel):
    """Community.
    """
    NAME_DICT = {
        u'交易权属': 'trading_right',
        u'产权年限': 'property_right_years',
        u'供暖类型': 'heating_type',
        u'供暖费用': 'heating_cost',
        u'停车费用': 'parking_cost',
        u'固定车位数': 'parking_place_number',
        u'容积率': 'volume_ratio',
        u'建成年代': 'building_finish_year',
        u'建筑类型': 'building_type',
        u'开发企业': 'development_company',
        u'房屋用途': 'house_type',
        u'燃气费用': 'gas_cost',
        u'物业公司': 'property_management_company',
        u'物业电话': 'property_management_phone_number',
        u'物业费用': 'property_management_cost',
        u'用水类型': 'water_use_type',
        u'用电类型': 'power_consumption_type',
        u'绿化率': 'green_coverage',
        u'附近学校': 'nearby_schools',
        u'楼栋总数': 'building_number',
        u'建筑面积': 'built_area',
        u'人车分流': 'separation_pedestrian_vehicular',
        u'占地面积': 'covered_area',
        u'是否封闭': 'close',
        u'总户数': 'house_number',
        u'电梯房': 'elevator',
        u'建筑品质': 'score_building_quality',
        u'户型设计': 'score_apartment_layout_design',
        u'交通条件': 'score_traffic_condition',
        u'教育质量': 'score_education_quality',
        u'商业环境': 'score_business_environment',
        u'花园景观': 'score_garden_View',
        u'物业管理': 'score_property_management',
        u'游泳池': 'is_swimming_pool',
        u'小区花园': 'is_community_garden',
        u'运动场地': 'is_sports_ground',
        u'康乐设施': 'is_recreational_facility',
        u'会所': 'is_club',
        u'健身房': 'is_gym',
        u'大堂': 'is_lobby',
        u'活动中心': 'is_activity_center',
        u'水系': 'is_river_system',
        u'儿童游乐': 'is_playground'
    }
    community_id = BigIntegerField(primary_key=True)
    title = CharField(null=True)  # 标题
    link = CharField(unique=True)  # 链接
    district = CharField(null=True)  # 区域
    bizcircle = CharField(null=True)  # 商圈
    intro = CharField(null=True)  # 介绍
    tags = CharField(null=True)  # 标签列表
    onsale = CharField(null=True)  # 在售套数
    onrent = CharField(null=True)  # 在租套数
    building_number = CharField(null=True)  # 楼栋总数
    house_number = CharField(null=True)  # 总户数
    average_unit_price = CharField(null=True)  # 均价
    building_finish_year = CharField(null=True)  # 建成年代
    built_area = CharField(null=True)  # 建筑面积
    covered_area = CharField(null=True)  # 占地面积
    house_type = CharField(null=True)  # 房屋用途
    property_right_years = CharField(null=True)  # 产权年限
    building_type = CharField(null=True)  # 建筑类型
    development_company = CharField(null=True)  # 开发企业
    trading_right = CharField(null=True)  # 交易权属
    property_management_company = CharField(null=True)  # 物业公司
    property_management_cost = CharField(null=True)  # 物业费用
    property_management_phone_number = CharField(null=True)  # 物业电话
    heating_type = CharField(null=True)  # 供暖类型
    heating_cost = CharField(null=True)  # 供暖费用
    water_use_type = CharField(null=True)  # 用水类型
    power_consumption_type = CharField(null=True)  # 用电类型
    parking_place_number = CharField(null=True)  # 固定车位数
    parking_cost = CharField(null=True)  # 停车费用
    gas_cost = CharField(null=True)  # 燃气费用
    volume_ratio = CharField(null=True)  # 容积率
    green_coverage = CharField(null=True)  # 绿化率
    separation_pedestrian_vehicular = CharField(null=True)  # 人车分流
    close = CharField(null=True)  # 是否封闭
    elevator = CharField(null=True)  # 是否电梯房
    nearby_schools = CharField(null=True)  # 附近学校
    score = FloatField(null=True)  # 评分
    score_building_quality = FloatField(null=True)  # 建筑品质
    score_apartment_layout_design = FloatField(null=True)  # 户型设计
    score_traffic_condition = FloatField(null=True)  # 交通条件
    score_education_quality = FloatField(null=True)  # 教育质量
    score_business_environment = FloatField(null=True)  # 商业环境
    score_garden_View = FloatField(null=True)  # 花园景观
    score_property_management = FloatField(null=True)  # 物业管理
    good_point = CharField(null=True)  # 优点
    bad_point = CharField(null=True)  # 弱点
    is_swimming_pool = BooleanField(null=True)  # 游泳池
    is_community_garden = BooleanField(null=True)  # 小区花园
    is_sports_ground = BooleanField(null=True)  # 运动场地
    is_recreational_facility = BooleanField(null=True)  # 康乐设施
    is_club = BooleanField(null=True)  # 会所
    is_gym = BooleanField(null=True)  # 健身房
    is_lobby = BooleanField(null=True)  # 大堂
    is_activity_center = BooleanField(null=True)  # 活动中心
    is_river_system = BooleanField(null=True)  # 水系
    is_playground = BooleanField(null=True)  # 儿童游乐
    valid_date = DateTimeField(default=datetime.datetime.now)  # 更新时间


class House(BaseModel):
    """House.
    """
    house_id = BigIntegerField(primary_key=True)
    title = CharField(null=True)  # 标题
    link = CharField(null=True)  # 链接
    intro = CharField(null=True)  # 介绍
    community = CharField(null=True)  # 所在小区
    total_price = CharField(null=True)  # 总价
    unit_price = CharField(null=True)  # 单价
    images = CharField(null=True)  # 图片
    layout = CharField(null=True)  # 房屋户型
    structure = CharField(null=True)  # 户型结构
    built_area = CharField(null=True)  # 建筑面积
    usable_area = CharField(null=True)  # 套内面积
    orientation = CharField(null=True)  # 房屋朝向
    floor = CharField(null=True)  # 所在楼层
    building_type = CharField(null=True)  # 建筑类型
    building_structure = CharField(null=True)  # 建筑结构
    decoration_type = CharField(null=True)  # 装修情况
    elevator = CharField(null=True)  # 配备电梯
    heating_type = CharField(null=True)  # 供暖类型
    stairs_and_households = CharField(null=True)  # 梯户比例
    building_finish_year = CharField(null=True)  # 建成年代
    property_right_years = CharField(null=True)  # 产权年限
    trading_right = CharField(null=True)  # 交易权属
    listing_time = DateTimeField(null=True)  # 挂牌时间
    house_type = CharField(null=True)  # 房屋用途
    life_years = CharField(null=True)  # 房屋年限
    ownership = CharField(null=True)  # 房权所属
    valid_date = DateTimeField(default=datetime.datetime.now)  # 更新时间


class HistoryPrice(BaseModel):
    """History price.
    """
    house_id = CharField()
    total_price = CharField()
    date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        """Meta.
        """
        primary_key = CompositeKey('house_id', 'total_price')


class Sell(BaseModel):
    """Sell.
    """
    house_id = CharField(primary_key=True)
    title = CharField(null=True)
    link = CharField(null=True)
    community = CharField(null=True)
    years = CharField(null=True)
    house_type = CharField(null=True)
    square = CharField(null=True)
    direction = CharField(null=True)
    floor = CharField(null=True)
    status = CharField(null=True)
    source = CharField(null=True)
    total_price = CharField(null=True)
    unit_price = CharField(null=True)
    dealdate = CharField(null=True)
    update_date = DateTimeField(default=datetime.datetime.now)


class Rent(BaseModel):
    """Rent.
    """
    house_id = CharField(primary_key=True)
    title = CharField(null=True)
    link = CharField(null=True)
    region = CharField(null=True)
    zone = CharField(null=True)
    meters = CharField(null=True)
    other = CharField(null=True)
    subway = CharField(null=True)
    decoration_type = CharField(null=True)
    heating = CharField(null=True)
    price = CharField(null=True)
    pricepre = CharField(null=True)
    update_date = DateTimeField(default=datetime.datetime.now)


def init():
    """Init database.
    """
    DATABASE.connect()
    # DATABASE.create_tables([Community, House, HistoryPrice, Sell, Rent],
    #                        safe=True)
    DATABASE.create_tables([Community], safe=True)
    DATABASE.close()
