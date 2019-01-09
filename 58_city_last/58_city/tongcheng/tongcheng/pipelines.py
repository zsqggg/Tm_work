# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.exceptions import DropItem
from scrapy.conf import settings
import random
import time
import traceback
import requests

class TongchengPipeline(object):
    def process_item(self, item, spider):
        return item

class DuplicatesPipeline(object):
    """去重"""
    def __init__(self):
        self.settings = settings
        self.client_mysql = pymysql.connect(
            host=self.settings.get('MYSQL_HOST'),
            port= self.settings.get('MYSQL_PROT'),
            db=self.settings.get('MYSQL_DBNAME'),
            user=self.settings.get('MYSQL_USER'),
            passwd=self.settings.get('MYSQL_PASSWD'),
            charset='utf8',
            use_unicode=True)
        self.curser = self.client_mysql.cursor()

    def process_item(self, item, spider):
        try:
            sql = """SELECT url FROM shop_detail where shop_name=(%s)"""
            self.curser.execute(sql, (item['shop_detailItem']['shop_name']))
            sortid = self.curser.fetchone()
            self.client_mysql.close()
            if sortid:
                print('已去重！！！')
                raise DropItem('Duplicate sort_id fount:%s' % sortid)
            else:
                print('错误方法！！！')
                return item
        except:
            print('没去重！！！')
            return item
        # finally:
        #     sortid = self.curser.fetchone()[0]
        #     if item['shop_detailItem']['sort_id'] == sortid:
        #         raise DropItem("Duplicate book found:%s" % item)
        #     else:
        #         return item


class MysqlPipeline(object):

    def __init__(self):
        self.settings = settings
        # 连接数据库
        # self.connect = pymysql.connect(
        #     host=settings.get('MYSQL_HOST'),
        #     db=settings.get('MYSQL_DBNAME'),
        #     user=settings.get('MYSQL_USER'),
        #     passwd=settings.get('MYSQL_PASSWD'),
        #     charset='utf8',
        #     use_unicode=True)
        # self.cursor = self.connect.cursor()
        # self.url_set = set()
        pass

    def process_item(self, item, spider):
        self.connect = pymysql.connect(
            host=settings.get('MYSQL_HOST'),
            db=settings.get('MYSQL_DBNAME'),
            user=settings.get('MYSQL_USER'),
            passwd=settings.get('MYSQL_PASSWD'),
            charset='utf8',
            use_unicode=True)

        self.cursor = self.connect.cursor()
        self.url_set = set()

        try:
            # 查询所在城市 id
            # print('查询所在城市')
            self.cursor.execute("select id from sys_city where city_name = (%s)", (item['shop_detailItem']['city']))
            city_id = self.cursor.fetchone()[0]

            # 查询所属区域 id
            try:
                self.cursor.execute("select id from sys_area where area_name = (%s)", (item['shop_detailItem']['area']))
                area_id = self.cursor.fetchone()[0]
            except:
                area_id = 0

            # 查询所属道路 id
            try:
                self.cursor.execute("select id from sys_road where road_name = (%s)", (item['shop_detailItem']['road']))
                road_id = self.cursor.fetchone()[0]
            except:
                road_id = 0

            # 生成名字
            img_url_lis = item['imge_list']
            img_lis = []
            date = int(time.time())
            s = 0
            for i in img_url_lis:
                s += 1
                img_name = 'spider58_' + str(date) + '_' + str(s) + '.jpg'
                img_lis.append(img_name)
            # 动态处理图片数量
            imag_list = []
            count = 0
            for i in img_lis:
                if count < len(img_lis):
                    imag_list.append(i)
                    count += 1
                else:
                    imag_list.append(' ')
            img_list = imag_list

            # shop_detail表
            self.cursor.execute("""insert into shop_detail (img1, img2, img3, shop_name, infomation, house_let, business_type, fit_up, cq_addr, area, 
                  detail_addr, city, create_time, road, read_time, on_shelf, owner_name, owner_phone, position_x, position_y,update_time,url) 
                 values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (img_list[0], img_list[1], img_list[2], item['shop_detailItem']['shop_name'], item['shop_detailItem']['infomation'],
                 item['shop_detailItem']['house_let'],item['shop_detailItem']['business_type'], item['shop_detailItem']['fit_up'],item['shop_detailItem']['cq_addr'], area_id,
                 item['shop_detailItem']['detail_addr'], city_id, item['shop_detailItem']['create_time'], road_id,item['shop_detailItem']['read_time'],
                 item['shop_detailItem']['on_shelf'], item['shop_detailItem']['owner_name'],item['shop_detailItem']['owner_phone'],
                 item['shop_detailItem']['position_x'], item['shop_detailItem']['position_y'], item['shop_detailItem']['update_time'], item['url']))
            # print('插入shop_detail表！')

            # 查询店铺id
            shop_id = self.cursor.lastrowid
            # print('查询shop_id')

            # shop_rent表
            self.cursor.execute("""insert into shop_rent (shop_id, rent, pay_method, let_time, property_fee, transfer_fee) values (%s, %s, %s, %s, %s, %s)""",
                                  (shop_id, item['shop_rentItem']['rent'], item['shop_rentItem']['pay_method'], item['shop_rentItem']['let_time'],
                                   item['shop_rentItem']['property_fee'], item['shop_rentItem']['transfer_fee']))
            # print('插入shop_rent表！')

            # shop_property表
            self.cursor.execute("insert into shop_property (shop_id, shop_type, shop_area, is_main_road, floor, all_floor) values (%s, %s, %s, %s, %s, %s)",
                                  (shop_id, item['shop_propertyItem']['shop_type'], item['shop_propertyItem']['shop_area'], item['shop_propertyItem']['is_main_road'],
                                   item['shop_propertyItem']['floor'], item['shop_propertyItem']['all_floor']))
            # print('插入shop_property表！')

            # shop_match_middle表
            for match_id in item['shop_match_middleItem']['match_id']:
                self.cursor.execute("insert into shop_match_middle (match_id, shop_id) values (%s, %s)", (match_id, shop_id))
            # print('插入shop_match_middle表！')
            self.connect.commit()

            # 下载图片
            img_url_lis = item['imge_list']
            s = 0
            for i in img_url_lis:
                # 获取图片内容
                res = requests.get(i, headers=self.settings.get('DEFAULT_REQUEST_HEADERS'))
                if res.status_code == 200:
                    with open(self.settings.get('IMAGES_STORE') + '/%s/%s' % (city_id, img_lis[s]), 'wb')as f:
                        f.write(res.content)
                    s += 1
            print('{}存入完成'.format(item['url']))
        except Exception:
            # 出现错误时打印错误日志,并回滚
            print('%s 数据存储错误' % item['url'])
            traceback.print_exc()
            self.connect.rollback()
        self.connect.close()
        return item
