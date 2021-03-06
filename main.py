# -*- coding: utf-8 -*-
import os
import time
import datetime
import json
#import io
#import sys

import arrow
import requests

from helper_kakou import Kakou
from helper_sms import SMS
from my_yaml import MyYAML
from my_logger import *

#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


debug_logging('/var/logs/error.log')
logger = logging.getLogger('root')


class BKCPAlarm(object):
    def __init__(self):
        self.ini = MyYAML('/home/my.yaml')
        self.my_ini = self.ini.get_ini()

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
        logger.info('start')
        
    def __del__(self):
        del self.my_ini

    def send_sms(self, content, mobiles):
        """发送短信"""
        try:
            self.sms.sms_send(content, mobiles)
            logger.info('mobiles={0}, content={1}'.format(mobiles, content))
        except Exception as e:
            logger.error(e)

    def get_data(self):
        maxid = self.kakou.get_alarm_maxid()['maxid']
        if maxid > self.id_flag:
            print('alarm={0}'.format(self.id_flag+1))
            logger.info('alarm={0}'.format(self.id_flag+1))
            info = self.kakou.get_alarm_by_id(self.id_flag+1)
            logger.info(info)
            if info == {}:
                self.id_flag += 1
                return
            if arrow.now('PRC') < arrow.get(info['pass_time']).to('Asia/Shanghai').replace(hours=-8, minutes=15):
                # 卡口地点信息
                crossing_info = self.kakou.get_traffic_crossing_info_by_id(info['crossing_id'])
                logger.info(crossing_info)
                if crossing_info == {}:
                    self.id_flag += 1
                    return
                # 控制单元
                control_unit = self.kakou.get_control_unit_by_id(crossing_info['control_unit_id'])
                logger.info(control_unit)
                if control_unit == {}:
                    self.id_flag += 1
                    return
                # 布控原因
                if info['disposition_reason'] == '99':
                    disposition_reason = info['res_str1']
                else:
                    sysdict_info = self.get_traffic_sysdict(
                        {'sysdict_type':1006,'sysdict_code':info['disposition_reason']})
                    if sysdict_info['total_count'] > 0:
                        disposition_reason = sysdict_info['items'][0]['sysdict_name']
                    else:
                        disposition_reason = ''
                # 集成发送内容
                content = "[惠阳卡口平台-{0}报警]{1},{2},{3},{4}{5}".format(
                    control_unit['name'], info['pass_time'],
                    crossing_info['crossing_name'],
                    self.fx.get(info['direction_index'], '进城'),
                    info['plate_no'], '({0})'.format(disposition_reason))
                self.send_sms(content, info['mobiles'])
            self.id_flag += 1


    def loop_get_data(self):
        while 1:
            try:
                if self.id_flag == 0:
                    self.id_flag = self.kakou.get_maxid()['maxid']
                else:
                    time.sleep(1)
                    self.get_data()
            except Exception as e:
                logger.exception(e)
                time.sleep(15)

