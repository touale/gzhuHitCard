# -*- coding: UTF-8 -*-
'''
@Project -> File   ：yfj -> selectRoom
@Author ：ToualeCula
@Email ：1367642349@qq.com
@Date ：2022/6/22 13:16
@Desc ：
'''

import time, requests, json


class SelctRoom:
    def __init__(self, client=requests.Session()):
        self.client = client
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"}

    def getSelectData(self, roomId):

        try:
            url = 'http://libbooking.gzhu.edu.cn/ic-web/seatRoom/openScope?roomId={}'.format(roomId)

            res = self.client.request('GET', url,verify=False,headers=self.headers).text
            return res
        except Exception as e:
            return 'something error'

    def login(self):

        try:
            url = 'http://libbooking.gzhu.edu.cn/ic-web/auth/address?finalAddress=http:%2F%2Flibbooking.gzhu.edu.cn&errPageUrl=' \
                  'http:%2F%2Flibbooking.gzhu.edu.cn%2F%23%2Ferror&manager=false&consoleType=16'

            res = self.client.request('GET', url,verify=False,headers=self.headers).text
            js = json.loads(res)

            res = self.client.request('GET', js['data'],verify=False,headers=self.headers).text
            return True
        except Exception as e:
            print(e)
            return False
