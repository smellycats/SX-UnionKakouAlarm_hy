# -*- coding: utf-8 -*-
import os
import time
import datetime
import json

import arrow
import requests

from helper_kakou import Kakou
from helper_sms import SMS
from my_yaml import MyYAML
from my_logger import *


debug_logging('/var/logs/error.log')
logger = logging.getLogger('root')


class BKCPAlarm(object):
    def __init__(self):
        self.ini = MyYAML('/home/my.yaml')
        self.my_ini = self.ini.get_ini()

        # request方法类
        #self.kk = Kakou(**dict(self.my_ini['kakou']))
        #self.uk = UnionKakou(**dict(self.my_ini['union']))

        self.sms = SMS(**dict(self.my_ini['sms']))
        self.kakou = Kakou(**dict(self.my_ini['union']))

        self.id_flag = 0

        self.fx = {
            0: '其他',
            1: '由东向西',
            2: '由西向东',
            3: '由南向北',
            4: '由北向南',
            5: '由东南向西北',
            6: '由西北向东南',
            7: '由东北向西南',
            8: '由西南向东北',
            9: '进城',
            10: '出城',
            11: '进场',
            12: '出场'
        }
        # 布控车牌字典形如 {'粤LXX266': {'kkdd': '东江大桥卡口',
        # 'jgsj': <Arrow [2016-03-04T09:39:45.738000+08:00]>}}
        #self.bkcp_dict = {}
        self.time_flag = arrow.now('PRC')
        logger.info('start')
        
    def __del__(self):
        del self.my_ini

    def send_sms(self, content, mobiles):
        """发送短信"""
        try:
            self.sms.sms_send(content, mobiles)
            logger.info(content)
            logger.info(mobiles)
        except Exception as e:
            logger.error(e)

    def get_data(self):
        maxid = self.kakou.get_maxid()['maxid']
        if maxid > self.id_flag:
            print(self.id_flag+1)
            info = self.kakou.get_vehicle_by_id(self.id_flag+1)
            logger.info(self.id_flag+1)
            logger.info(info)
            if info != {}:
                print(arrow.now('PRC'))
                print(info['pass_time'])
                print(arrow.get(info['pass_time']).to('Asia/Shanghai').replace(hours=-8, minutes=15))
                if arrow.now('PRC') < arrow.get(info['stop_time']) and arrow.now('PRC') < arrow.get(info['pass_time']).to('Asia/Shanghai').replace(hours=-8, minutes=15):
                    crossing_info = self.kakou.get_traffic_crossing_info_by_id(info['crossing_id'])
                    logger.info(crossing_info)
                    if crossing_info == {}:
                        self.id_flag += 1
                        return
                    control_unit = self.kakou.get_control_unit_by_id(crossing_info['control_unit_id'])
                    logger.info(control_unit)
                    if control_unit != {}:
                        content = "[惠阳卡口平台-{0}报警]{1},{2},{3},{4}".format(
		            control_unit['name'], info['pass_time'], crossing_info['crossing_name'],
		            self.fx.get(info['direction_index'], '进城'), info['plate_no'])
                        self.send_sms(content, info['mobiles'])
            self.id_flag += 1
        
    def restart_config(self):
        now = arrow.now('PRC')
        t = now - self.time_flag
        if t.total_seconds() > 60 * 60 * 2 and self.time_flag.hour == 1:
            logger.info('restart')
            return True
        return False


    def loop_get_data(self):
        while 1:
            try:
                if self.id_flag == 0:
                    self.id_flag = self.kakou.get_maxid()['maxid']
                else:
                    time.sleep(1)
                    self.get_data()
                if self.restart_config():
                    break
            except Exception as e:
                logger.exception(e)
                time.sleep(15)

