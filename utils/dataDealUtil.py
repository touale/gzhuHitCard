# -*- coding: UTF-8 -*-
'''
@Project -> File   ：AutoHitCard -> utils
@Author ：ToualeCula
@Email ：1367642349@qq.com
@Date ：2021/11/9 21:40
@Desc ：
'''
import time


def getMidString(html, start_str, end_str):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end_str, start)
        if end >= 0:
            return html[start:end].strip()

def getCurrentTimestamp():
    return str(int(time.time()))