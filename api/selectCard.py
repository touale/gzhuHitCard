# -*- coding: UTF-8 -*-
'''
@Project -> File   ：app -> selectCard
@Author ：ToualeCula
@Email ：1367642349@qq.com
@Date ：2021/11/13 17:37
@Desc ：
'''

import time, requests, json


class SelctCard:
    def __init__(self, client=requests.Session()):
        self.client = client

    def getSelectData(self):
        try:
            url = 'https://yqtb.gzhu.edu.cn/taskcenter/api/me/processes/done?limit=10&start=0'
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"}

            res = self.client.request('POST', url,verify=False,headers=headers).text
            return res
        except Exception as e:
            return 'something error'

