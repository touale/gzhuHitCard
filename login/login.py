# -*- coding: UTF-8 -*-
'''
@Project -> File   ：yfj -> login
@Author ：ToualeCula
@Email ：1367642349@qq.com
@Date ：2022/1/12 19:43
@Desc ：
'''
# -*- coding: UTF-8 -*-
'''
@Project -> File   ：AutoLogin -> casLogin
@Author ：ToualeCula
@Email ：1367642349@qq.com
@Date ：2021/11/10 14:22
@Desc ：
'''
import json
import requests

from utils.jsExec import cacuRSA
from utils.dataDealUtil import getMidString

'''
in some cases, the ssl certificate is not trusted because of the school server is so rubbish.
'''
import urllib3

urllib3.disable_warnings()


class CasLogin:

    def __init__(self):
        self.client = requests.session()
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded; Charset=UTF-8',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55'}

    def getItAndExecution(self):
        url = 'https://newcas.gzhu.edu.cn/cas/login?service=https%3A%2F%2Fnewmy.gzhu.edu.cn%2Fup%2F'
        res = self.client.get(url=url, headers=self.headers, verify=False, allow_redirects=False, )

        It = getMidString(res.text, 'name="lt" value="', '"')
        execution = getMidString(res.text, 'execution" value="', '"')
        return It, execution

    def login(self, user, pwd, it, exc):
        url = 'https://newcas.gzhu.edu.cn/cas/login'
        data = 'rsa=' + cacuRSA(user + pwd + it + exc) + \
               '&ul=' + str(len(user)) + \
               '&pl=' + str(len(pwd)) + \
               '&lt=' + it + \
               '&execution=' + exc + \
               '&_eventId=submit'

        res = self.client.request('POST', url, data=data, verify=False, headers=self.headers)
        msg = getMidString(res.text, '<span id="errormsghide" class="login_box_title_notice script_red">', '<br/>')

        '''
        in some special case, the msg is empty, but the login is false
        '''
        return ("登录异常" if res.text.find("统一身份认证") != -1 else None) \
            if (msg == None) else msg

    def run(self, user, pwd):
        try:
            It, execution = self.getItAndExecution()
            msg = self.login(user, pwd, It, execution)
            return self.generateResult(1, 'success') if (msg == None) else self.generateResult(0, msg)
        except Exception as e:
            return self.generateResult(0, "登录异常，请重新登录")

    def getClient(self):
        return self.client

    def generateResult(self, code, msg, data=None):
        req = {
            "code": code,
            "msg": msg,
            "data": data
        }
        try:
            return json.dumps(req, ensure_ascii=False)
        except:
            return 'Sys Error'


if __name__ == '__main__':
    # just used for test
    print(CasLogin().run('123', '123'))
