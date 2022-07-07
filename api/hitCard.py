# -*- coding: UTF-8 -*-

import json


from config.renderData import generateTestRenderFormData
from utils.dataDealUtil import getMidString, getCurrentTimestamp
from utils.jsExec import generateRank


class HitCard:
    def __init__(self, client):
        self.client = client
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded; Charset=UTF-8',
                        'Referer': 'https://yqtb.gzhu.edu.cn/infoplus/interface/preview',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55'}

    def getCsrfTokenAndWorkflowId(self):  # XNYQSB
        url = 'https://yqtb.gzhu.edu.cn/infoplus/form/XNYQSB/start'
        res = self.client.get(url=url, verify=False, headers=self.headers).text
        csrfToken = getMidString(res, 'csrfToken" content="', '">')
        workflowId = getMidString(res, 'workflowId = "', '"')
        return csrfToken, workflowId

    def getPreview(self, csrfToken, workflowId):
        url = 'https://yqtb.gzhu.edu.cn/infoplus/interface/preview'
        data = 'workflowId=' + workflowId + '&rand=400.1695693011468&width=1266&csrfToken=' + csrfToken
        res = self.client.request('POST', url, verify=False, data=data, headers=self.headers).text
        js = json.loads(res)
        return json.dumps(js['entities'][0]['data'])

    def getRender(self, csrfToken, formData):
        url = 'https://yqtb.gzhu.edu.cn/infoplus/interface/start'
        data = 'idc=XNYQSB&release=&csrfToken=' + \
               csrfToken + \
               '&formData=' + \
               str(formData) + \
               '&lang=zh'

        res = self.client.request('POST', url, verify=False, data=data, headers=self.headers).text
        js = json.loads(res)
        url = js['entities'][0]
        stepId = getMidString(url, 'form/', '/render')
        return url, stepId

    def getSumbitData(self, stepId, csrfToken):
        url = 'https://yqtb.gzhu.edu.cn/infoplus/interface/render'
        data = 'stepId=' + \
               stepId + \
               '&instanceId=&admin=false&rand=' + \
               generateRank() + \
               '&width=304&lang=zh&csrfToken=' + \
               csrfToken

        res = self.client.request('POST', url, data=data, headers=self.headers, verify=False).text
        js = json.loads(res)
        fields = ''

        '''To adapt to the system, I analyze the data of the form to get the real field names and values, 
        so that when the form is changed, the system can be adapted to the new form. '''
        for field in js['entities'][0]['fields']:
            bound, name = None, None
            try:
                bound = js['entities'][0]['fields'][field]['bound']
            except:
                pass
            name = js['entities'][0]['fields'][field]['name']
            if (bound == True and name != None):
                fields += name + ','
        fields = fields[:-1]

        cjs = json.loads(generateTestRenderFormData())
        for _data in cjs:
            try:
                cjs[_data] = js['entities'][0]['data'][_data]
            except:
                continue

        '''
        In the form,the field values are not allowed to be repeated from the last form which you had submitted yesterday.
        '''
        cjs['fieldCNS'] = True  # 勾选本人承诺
        cjs['fieldYQJLsfjcqtbl'] = '2'  # 无接触
        cjs['fieldJKMsfwlm'] = '1'  # 是绿码
        cjs['fieldCXXXsftjhb'] = '2'  # 无外出
        cjs['fieldJBXXdrsfwc'] = '2'  # 当日五外出
        cjs['fieldSTQKbrstzk1'] = '1'  # 身体状况正常
        formData = json.dumps(cjs)
        return formData, fields

    def listNextStepsUsers(self, stepId, formData, fields, csrfToken):
        url = 'https://yqtb.gzhu.edu.cn/infoplus/interface/listNextStepsUsers'
        data = 'stepId=' + stepId + \
               '&actionId=1&formData=' + formData + \
               '&timestamp=' + getCurrentTimestamp() + \
               '&rand=' + generateRank() + \
               '&boundFields=' + fields + \
               '&csrfToken=' + csrfToken + \
               '&lang=zh'

        res = self.client.request('POST', url, verify=False, data=data, headers=self.headers).text
        return json.loads(res)['ecode']

    def doAction(self, stepId, formData, fields, csrfToken):
        url = 'https://yqtb.gzhu.edu.cn/infoplus/interface/doAction'
        data = 'actionId=1' + \
               '&formData=' + formData + \
               '&remark=&rand' + generateRank() + \
               '&nextUsers=%7B%7D' + \
               '&stepId=' + stepId + \
               '&timestamp=' + getCurrentTimestamp() + \
               '&boundFields=' + fields + \
               '&csrfToken=' + csrfToken + \
               '&lang=zh'

        try:
            res = self.client.request('POST', url, verify=False, data=data, headers=self.headers).text
            js = json.loads(res)
            return js['error']
        except:
            return 'doAction Error'

    def run(self):
        try:
            csrfToken, workflowId = self.getCsrfTokenAndWorkflowId()
            formData = self.getPreview(csrfToken, workflowId)
            url, stepId = self.getRender(csrfToken, formData)
            formData, fields = self.getSumbitData(stepId, csrfToken)
            self.listNextStepsUsers(stepId, formData, fields, csrfToken)
            csrfToken, workflowId = self.getCsrfTokenAndWorkflowId()
            self.listNextStepsUsers(stepId, formData, fields, csrfToken)
            res = self.doAction(stepId, formData, fields, csrfToken)
            return self.generateResult(0, '打卡失败', res) if res != '打卡成功' else self.generateResult(1, res)
        except Exception as e:
            return self.generateResult(1, '打卡异常', str(e))

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
