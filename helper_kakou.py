# -*- coding: utf-8 -*-
import json

import requests


class Kakou(object):
    def __init__(self, **kwargs):
        self.host = kwargs['host']
        self.port = kwargs['port']
        self.headers = {'content-type': 'application/json'}

        self.status = False

    def get_maxid(self):
        """获取最大ID值"""
        url = 'http://{0}:{1}/alarm_maxid'.format(self.host, self.port)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.status = False
            raise

    def get_vehicle_by_id(self, _id):
        """根据ID范围获取车辆信息"""
        url = 'http://{0}:{1}/alarm/{2}'.format(
            self.host, self.port, _id)
        try:
            r = requests.get(url)
            if r.status_code == 200 or r.status_code == 404:
                return json.loads(r.text)
            else:
                self.status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.status = False
            raise


    def get_alarm_maxid(self):
        """获取过车报警最大ID值"""
        url = 'http://{0}:{1}/alarm/maxid'.format(self.host, self.port)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.status = False
            raise

    def get_alarm_by_id(self, _id):
        """根据ID范围获取过车报警信息"""
        url = 'http://{0}:{1}/alarm/{2}'.format(
            self.host, self.port, _id)
        try:
            r = requests.get(url)
            if r.status_code == 200 or r.status_code == 404:
                return json.loads(r.text)
            else:
                self.status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.status = False
            raise

    def get_kkdd_by_id(self, kkdd_id):
        """根据车牌号码获取布控信息"""
        url = 'http://{0}:{1}/kkdd/{2}'.format(
            self.host, self.port, kkdd_id)
        try:
            r = requests.get(url)
            if r.status_code == 200 or r.status_code == 404:
                return json.loads(r.text)
            else:
                self.status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.status = False
            raise

    def get_traffic_crossing_info_by_id(self, crossing_id):
        """根据ID获取卡口地点信息"""
        url = 'http://{0}:{1}/traffic_crossing_info/{2}'.format(
            self.host, self.port, crossing_id)
        try:
            r = requests.get(url)
            if r.status_code == 200 or r.status_code == 404:
                return json.loads(r.text)
            else:
                self.status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.status = False
            raise


    def get_control_unit_by_id(self, control_unit_id):
        """根据ID获取控制单元信息"""
        url = 'http://{0}:{1}/control_unit/{2}'.format(
            self.host, self.port, control_unit_id)
        try:
            r = requests.get(url)
            if r.status_code == 200 or r.status_code == 404:
                return json.loads(r.text)
            else:
                self.status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.status = False
            raise

