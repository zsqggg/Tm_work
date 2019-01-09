# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TongchengItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Shop_propertyItem(scrapy.Item):
    shop_type = scrapy.Field()
    shop_area = scrapy.Field()
    is_main_road = scrapy.Field()
    floor = scrapy.Field()
    all_floor = scrapy.Field()

class Shop_rentItem(scrapy.Item):
    rent = scrapy.Field()
    pay_method = scrapy.Field()
    let_time = scrapy.Field()
    property_fee = scrapy.Field()
    transfer_fee = scrapy.Field()

class Shop_match_middleItem(scrapy.Item):
    match_id = scrapy.Field()
    shop_id = scrapy.Field()

class match_facilitiesItem(scrapy.Item):
    name = scrapy.Field()

class Shop_detailItem(scrapy.Item):
    shop_name = scrapy.Field()
    infomation = scrapy.Field()
    house_let = scrapy.Field()
    business_type = scrapy.Field()
    fit_up = scrapy.Field()
    cq_addr = scrapy.Field()
    area = scrapy.Field()
    detail_addr = scrapy.Field()
    img_list = scrapy.Field()
    city = scrapy.Field()
    create_time = scrapy.Field()
    road = scrapy.Field()
    read_time = scrapy.Field()
    on_shelf = scrapy.Field()
    set_top = scrapy.Field()
    user_id = scrapy.Field()
    down_user_id = scrapy.Field()
    position_x = scrapy.Field()
    position_y = scrapy.Field()
    owner_name = scrapy.Field()
    owner_phone = scrapy.Field()
    update_time = scrapy.Field()
    sort_id = scrapy.Field()

class ImageItem(scrapy.Item):
    image_list = scrapy.Field()
    # 图片名称
    images = scrapy.Field()
    # 图片存储路径
    image_paths = scrapy.Field()
