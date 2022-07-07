# -*- coding: UTF-8 -*-
'''
@Project -> File   ：yfj -> doJDSD
@Author ：ToualeCula
@Email ：1367642349@qq.com
@Date ：2022/6/22 21:27
@Desc ：经典诵读
'''

import time, requests, json

class DoJDSD:
    # 无语了，第二课堂分满了学校还要搞强制搞经典诵读分
    def __init__(self, key):
        self.url = "https://jdsd.gzhu.edu.cn/coctl_gzhu/index_wx.php"
        self.headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        }
        self.key = key
        self.client = requests.Session()

    def post(self, data):
        ''':cvar统一异常处理
        '''
        try:
            return self.client.request('POST', self.url, data=data, headers=self.headers).json()
        except Exception as e:
            print(e)
            return None

    def dealRes(self, res):
        ''':cvar 异常处理
        '''
        try:
            return True if res['status'] == 1 else False, res
        except Exception as e:
            return False, "解析失败"

    def getInfo(self):
        ''':cvar 获取个人信息
        '''
        data = 'route=user_info&key=' + self.key
        res = self.post(data)
        return self.dealRes(res)

    def doSign(self):
        ''':cvar 签到
        '''
        data = 'route=signin&key=' + self.key
        res = self.post(data)
        return self.dealRes(res)

    def doTrain(self):
        ''':cvar 每日一练
        '''
        data = 'route=train_list_get&diff=0&key=' + self.key
        res = self.post(data)
        try:
            if res['status'] == 0: return "获取题目失败"
        except Exception as e:
            return "获取题目失败"

        temp = []
        for i in res['re']['question_bag']:
            temp.append([i['num'], 1])

        data = 'route=train_finish&train_id=' + res['re']['train_id'] + \
               '&train_result=' + json.dumps(temp) + '&key=' + self.key

        res = self.post(data)
        try:
            return res['tip']
        except Exception as e:
            return "解析失败"

    def doRead(self):
        ''':cvar 阅读
        '''
        for i in range(1, 6):
            data = 'route=classic_time&addtime={}&type={}&key={}'.format(0, i, self.key)
            res = self.post(data)
            data = 'route=classic_time&addtime={}&type={}&key={}'.format(120, i, self.key)
            res = self.post(data)
        return self.dealRes(res)

    def doGame(self):
        ''':cvar 随机匹配
        '''
        count = 0
        while (1):
            data = 'route=get_counterpart&key={}&counter={}&find_type=0'.format(self.key, count)
            res = self.post(data)
            print(res)
            if (res['status'] == 1):
                gameKey = res['question_bag']['gaming_key']
                break
            count += 1
            if (count > 15): count = 0
        if (gameKey == None): return False
        print("匹配成功", gameKey)

        # 回答问题
        data = 'route=ask_opponent_score&key={}&gaming_key={}'.format(self.key, gameKey)
        count = 0
        try:
            for i in range(500):
                res = self.post(data)
                print(res)
                if (i == 0): time.sleep(20) # 假死促进机器人离开房间从而加速完成
                if res['status'] == 2: count += 1
                elif res['status'] >2: return False
                if count >= 10:
                    return True
                time.sleep(1)
        except Exception as e:
            return False
        return False if count < 5 else True

    def doExam(self, type=0, time=1000):
        ''':cvar 考试
        :parameter
            type: 0模拟考试，1正式考试
            time: 答题时间 单位厘秒 1000代表100秒

        说一下思路：
            讲道理，题目只返回了问题选项，没有把答案存储本地或者获取题目的在数据包里时候拿到，只有最后提交题目的时候才能拿到答案
            本质上，也就是说，只有交卷了才知道答案
            但是，有个离谱的地方，tmd居然可以交卷，而且交卷两次，那么第二次拿着第一次的答案，直接就是第一了
            具体操作：因为第一次提交返回的答案中只有答错的题目的答案，那么直接第一次提交的答案全部是Null值，此时就可保证提交后
            得到所有题目的答案，接着直接重复性提交即可
        '''

        if (type == 0):
            testId, mode = 9, -1
        else:
            testId, mode = 7, 1

        data = 'route=get_test&test_id={}&test_mode={}&key={}'.format(testId, mode, self.key)
        res = self.post(data)

        try:
            if (res['error'] != None):
                return res['error']
        except Exception as e:
            pass

        try:
            testId = res['bag']['test_id']
        except Exception as e:
            return "考试题目获取失败"

        i = 0
        result = []  # 异常处理，懒得写了
        for arr in res['bag']['question_arr']:
            temp = {"question_id": arr['question_id'], "answer_id": "", "question_num": str(arr['num']), "index": i}
            result.append(temp)
            i += 1

        data = 'route=submit_test&test_id={}&result={}&use_time={}&key={}'.format(testId, json.dumps(result), time,
                                                                                  self.key)
        newRes = self.post(data)
        print(newRes)  # 第一次考试结果

        result = []
        i = 0
        for arr in res['bag']['question_arr']:
            temp = {"question_id": arr['question_id'], "answer_id": newRes['answer'][i]['answer'],
                    "question_num": str(arr['num']), "index": i}
            result.append(temp)
            i += 1

        data = 'route=submit_test&test_id={}&result={}&use_time={}&key={}'.format(testId, json.dumps(result), time,
                                                                                  self.key)
        print("提交data", data)
        newRes = self.post(data)
        return (newRes)


if __name__ == '__main__':
    pass
    # just used for test
    # n = DoJDSD(
    #     '')
    # print(n.getInfo())  # 获取个人信息
    # print(n.doSign())  # 签到
    # print(n.doRead())  # 阅读
    # for i in range(3): print(n.doTrain())  # 每日一练，每次3分，上限9分
    # for i in range(5):
    #     if (n.doGame()): break  # 随机匹配,提高成功率
    # print(n.doExam(type=1,time=2000))  # 考试（需要消耗2次考试机会）
