# -*- coding: utf-8 -*-
import scrapy
import time
import re
import random
import queue
import traceback
from tongcheng.items import Shop_propertyItem
from tongcheng.items import Shop_rentItem
from tongcheng.items import Shop_match_middleItem
from tongcheng.items import match_facilitiesItem
from tongcheng.items import Shop_detailItem
from scrapy.http.cookies import CookieJar

cookiejar = CookieJar()
que = queue.Queue(maxsize=500)


class Tc58Spider(scrapy.Spider):
    name = 'tc58'
    allowed_domains = ['www.58.com']
    start_urls = ['http://bj.58.com']

    def start_requests(self):
        # 列表页爬取
        for val in self.settings.get("CITY_LIST"):
            url = "http://%s.58.com/shangpucz/" % val
            print('列表页%s开始采集'% val)
            yield scrapy.Request(url, headers=self.settings.get("DEFAULT_REQUEST_HEADERS"), callback=self.get_url)

    def get_url(self, response):
        # 获取当前页面的所有信息的url
        url_list = response.xpath("//div[@class='pic']/a/@href").extract()
        self.settings.get("DEFAULT_REQUEST_HEADERS")['referer'] = response.url
        for i in url_list:
            time.sleep(random.random())
            # 对详细页进行抓取解析
            print('详情页%s开始采集'% i)
            yield scrapy.Request(i, headers=self.settings.get("DEFAULT_REQUEST_HEADERS"),
                                 callback=self.detial_parse, dont_filter=True)
        # 抓取下一页内容
        try:
            next_url = response.xpath('//a[@class="next"]/@href').extract_first()
            if next_url:
                print('下一页%s开始采集'% next_url)
                yield scrapy.Request(next_url, headers=self.settings.get("DEFAULT_REQUEST_HEADERS"), callback=self.get_url,
                                     dont_filter=True)
            else:
                return
        except:
            print('爬虫结束！')
            return

    def detial_parse(self, response,):
        shop_propertyItem = Shop_propertyItem()
        shop_rentItem = Shop_rentItem()
        shop_match_middleItem = Shop_match_middleItem()
        shop_detailItem = Shop_detailItem()

        if response.body == None:
            print('该数据重复！--->%s' % response.url)

        else:
            print('----------->', 'Inner')
            try:
                # 商铺类型      /html/body/table/tbody/tr[155]/td[2]/text()
                panbie = {'临街门面': 0, '商业街商铺': 2, '商业街卖场': 2, '写字楼配套': 1, '住宅底商': 0, '档口摊位': 0, '摊位柜台': 0, '其他': 0,
                          '购物百货中心': 2, '社区底商': 0}
                shop_type = response.xpath('/html/body/table/tbody/tr[155]/td[2]/text()').extract_first()
                shop_type = panbie.get(shop_type)
                if shop_type:
                    shop_type = shop_type
                else:
                    shop_type = 0

                # 商铺面积
                shop_area = response.xpath('/html/body/div[4]/div[2]/div[2]/ul/li[1]/span[2]/text()').extract_first()[:-1]
                if not shop_area:
                    shop_area = 0

                # 商铺主干道
                result = response.xpath('/html/body/div[4]/div[2]/div[2]/ul/li[1]/span[4]/text()').extract_first()
                if not result:
                    is_main_road = 1
                else:
                    is_main_road = 2

                # 商铺楼层
                floor_all = response.xpath('/html/body/div[4]/div[2]/div[2]/ul/li[5]/span[2]/text()').extract_first()
                floor_all = data_cleansing(floor_all)
                if '/' in floor_all:
                    floor_list = floor_all.split('/')
                    floor = floor_list[0].strip('层').split('-')[0]
                    all_floor = int(floor_list[1].strip('[共 层]'))
                else:
                    all_floor = 1
                    floor = 1

                # 租金   /html/body/div[4]/div[2]/div[2]/p[1]/span[1]
                rent = response.xpath('/html/body/div[4]/div[2]/div[2]/p[1]/span[1]/text()').extract_first()

                # 付款方式
                pay_met = {'押1付3': 0, '押1付6': 1, '押1付12': 2, '押2付3': 3, '押2付6': 4, '押2付12': 5, '年付': 6, '押2付1': 7,
                           '押3付1': 8, '押3付3': 9}
                pay_method = response.xpath("/html/body/div[4]/div[2]/div[2]/ul/li[4]/span[4]/text()").extract_first()
                pay_method = pay_met.get(pay_method)
                if not pay_method:
                    pay_method = 10

                # 起租时间
                let_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                # 物业费
                property_fee = 0

                # 转让费
                transfer_fee = 0

                # 商铺名字
                shop_name = response.xpath('//h1/text()').extract_first()
                shop_name = data_cleansing(shop_name)

                # 商铺备注          //*[@id="generalSound"]/div/text()[1]
                infomation = response.xpath('//div[@id="generalSound"]/div/text()').extract()
                infomation = data_cleansing(infomation)

                # 房屋状态
                house_let = response.xpath('/html/body/div[4]/div[2]/div[2]/ul/li[2]/span[4]/text()').extract()
                house_let = data_cleansing(house_let)
                if '空置中' in house_let:
                    house_let = 0
                else:
                    house_let = 1

                # 配套设施      //*[@id="peitao"]/div/ul/li[15]
                facility_lis = []
                try:
                    facility = response.xpath('//*[@id="peitao"]/div/ul/li/@class').extract()
                    if facility[14] == 'peitao-on':
                        facility_lis.append(1)
                    if facility[8] == 'peitao-on':
                        facility_lis.append(3)
                    if facility[9] == 'peitao-on':
                        facility_lis.append(4)
                    if facility[12] == 'peitao-on':
                        facility_lis.append(5)
                    if facility[3] == 'peitao-on':
                        facility_lis.append(6)
                    if facility[10] == 'peitao-on':
                        facility_lis.append(7)
                    if facility[11] == 'peitao-on':
                        facility_lis.append(8)
                    if facility[4] == 'peitao-on':
                        facility_lis.append(9)
                except:
                    print('facility')
                # 历史经营类型(0其他 1餐饮 2休闲 3美容美发 4教育 5服务)
                business_type = response.xpath('/html/body/div[4]/div[2]/div[2]/ul/li[3]/span[4]/text()').extract_first()
                if business_type == '暂无':
                    business_type = 0
                elif '餐饮' in business_type:
                    business_type = 1
                elif '休闲' in business_type:
                    business_type = 2
                elif '美容美发' in business_type:
                    business_type = 3
                elif '教育' in business_type:
                    business_type = 4
                elif '服务' in business_type:
                    business_type = 5
                else:
                    business_type = 0

                # 装修程度
                fit_up = '1'

                # 产权地址
                detail_header = response.xpath('/html/body/div[4]/div[2]/div[2]/ul/li[6]/a[1]/text()').extract_first()
                try:
                    detail_content = response.xpath('/html/body/div[4]/div[2]/div[2]/ul/li[6]/a[2]/text()').extract_first()
                    cq_addr = detail_header + detail_content
                except:
                    cq_addr = detail_header

                # 所属区域      /html/body/div[4]/div[2]/div[2]/ul/li[6]/a[1]
                area_header = response.xpath('//ul/li[6]/a[1]/text()').extract_first()
                area = area_header

                # 详细地址
                detail_addr = response.xpath('//ul/li[6]/span[2]/text()').extract()[0]
                detail_addr = data_cleansing(detail_addr)
                if detail_addr:
                    detail_addr = detail_addr
                else:
                    detail_addr = '未知'

                # 图片
                img_url_lis = response.xpath('//ul[@class="general-pic-list"]/li/img/@src').extract()
                if len(img_url_lis) > 3:
                    img_url_lis = img_url_lis[:3]

                # 所在城市             /html/body/div[3]/div[2]/a[1]
                city = response.xpath('/html/body/div[3]/div[2]/a[1]/text()').extract_first()
                city = city.replace('58同城','')

                # 创建时间
                create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                # 所在道路
                try:
                    road = response.xpath('/html/body/div[4]/div[2]/div[2]/ul/li[6]/a[2]/text()').extract()[0]
                except:
                    road = '未知'
                # 浏览次数
                read_time = 1

                # 是否上架
                on_shelf = 1

                # 联系人
                owner_name = response.xpath('/html/body/div[4]/div[2]/div[2]/div[1]/div/a/text()').extract_first()

                owner_phone = response.xpath('//*[@id="houseChatEntry"]/div/p[1]/text()').extract_first()

                # x 坐标
                position_x = re.search('"baidulon":"(.*?)"', str(response.body), re.S).group()
                position_x = re.search('[1-9]\d*.\d*|0.\d*[1-9]\d*', position_x, re.S).group()

                # y 坐标
                position_y = re.search('"baidulat":"(.*?)"', str(response.body), re.S).group()
                position_y = re.search('[1-9]\d*.\d*|0.\d*[1-9]\d*', position_y, re.S).group()

                # 更新时间
                update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                # 商铺类型
                shop_propertyItem["shop_type"] = shop_type
                shop_propertyItem["shop_area"] = shop_area
                shop_propertyItem["is_main_road"] = is_main_road
                shop_propertyItem["floor"] = floor
                shop_propertyItem["all_floor"] = all_floor

                shop_rentItem["rent"] = rent
                shop_rentItem["pay_method"] = pay_method
                shop_rentItem["let_time"] = let_time
                shop_rentItem["property_fee"] = property_fee
                shop_rentItem["transfer_fee"] = transfer_fee

                shop_detailItem["shop_name"] = shop_name
                shop_detailItem["infomation"] = infomation
                shop_detailItem["house_let"] = house_let
                shop_detailItem["business_type"] = business_type
                shop_detailItem["fit_up"] = fit_up
                shop_detailItem["cq_addr"] = cq_addr
                shop_detailItem["area"] = area
                shop_detailItem["detail_addr"] = detail_addr
                shop_detailItem["img_list"] = img_url_lis
                shop_detailItem["city"] = city
                shop_detailItem["create_time"] = create_time
                shop_detailItem["road"] = road
                shop_detailItem["read_time"] = read_time
                shop_detailItem["on_shelf"] = on_shelf
                shop_detailItem["owner_name"] = owner_name
                shop_detailItem["owner_phone"] = owner_phone
                shop_detailItem["position_x"] = position_x
                shop_detailItem["position_y"] = position_y
                shop_detailItem["position_y"] = position_y
                shop_detailItem["update_time"] = update_time

                shop_match_middleItem["match_id"] = facility_lis

                data = {'shop_propertyItem': shop_propertyItem,
                        'shop_rentItem': shop_rentItem,
                        'shop_detailItem': shop_detailItem,
                        'shop_match_middleItem': shop_match_middleItem,
                        'url': response.url,
                        'imge_list':img_url_lis,
                        }
                print('+++++++++++++++++', 'PIPELINES')
                return data
            except:
                print('%s 数据处理错误' % response.url)
                traceback.print_exc()


# 去除空格 \n \t
def data_cleansing(data):
    if type(data) == list:
        data = ''.join(''.join([i for i in data]).split())
    else:
        data = data.replace(' ', '').replace('\n', '').replace('\t', '')
    return data
