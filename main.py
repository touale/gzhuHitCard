import json
from api.hitCard import HitCard
from api.selectCard import SelctCard
from login.login import CasLogin
import urllib3
from api.selectRoom import SelctRoom
from api.doJDSD import DoJDSD
'''
in some cases, the ssl certificate is not trusted because of the school server is so rubbish.
'''
urllib3.disable_warnings()

# 登录测试
def loginTest(user, pwd):
    cas = CasLogin()
    res = cas.run(user, pwd)
    return res

# 查询历史打卡
def selectCardTest(user, pwd):
    cas = CasLogin()
    client = cas.getClient()

    res = cas.run(user, pwd)
    re = json.loads(res)
    if (re['code'] != 1):
        return res

    return SelctCard(client).getSelectData()

# 打卡
def hitcardTest(user, pwd):
    cas = CasLogin()
    client = cas.getClient()
    res = cas.run(user, pwd)

    re = json.loads(res)
    if (re['code'] != 1):
        return res

    res = HitCard(client).run()
    return res

# 查询图书馆软件
def selectRoomTest(user, pwd,roomId):
    cas = CasLogin()
    client = cas.getClient()

    res = cas.run(user, pwd)
    re = json.loads(res)
    if (re['code'] != 1):
        return res

    s = SelctRoom(client)
    if (not s.login()):
        return "login error"
    return s.getSelectData(roomId)


if __name__ == '__main__':

    user = ''
    pwd = ''

    # # 登录模块测试
    # res = loginTest(user, pwd)
    # print("登录结果",res)

    # 健康系统的打卡历史获取
    # res = selectCardTest(user, pwd)
    # print("打卡历史", res)

    # 打卡
    # print("打卡",hitcardTest(user, pwd))

    # 查询图书馆
    # print(selectRoomTest(user, pwd,'100589684'))

    # 经典诵读
    # n = DoJDSD(key)
    # print(n.getInfo())  # 获取个人信息
    # print(n.doSign())  # 签到
    # print(n.doRead())  # 阅读
    # for i in range(3): print(n.doTrain())  # 每日一练，每次3分，上限9分
    # for i in range(5):
    #     if (n.doGame()): break  # 随机匹配,提高成功率
    # print(n.doExam(type=0,time=2000))  # 考试（需要消耗2次考试机会）




