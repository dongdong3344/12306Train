#!/usr/bin/env python
# coding:utf-8

import requests
import const
from hashlib import md5

class CJYClient:

    def __init__(self, username, password, soft_id):
        #平台账号
        self.username = username
        #平台密码
        self.password = md5(password.encode('utf-8')).hexdigest()
        # 软件ID
        self.soft_id = soft_id
        self.base_params = {
            'user'  : self.username,
            'pass2' : self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, img, codetype):

        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', img)}
        result = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers).json()
        answerList = result['pic_str'].replace('|',',').split(',')

        # 将平台返回的纵坐标减去30
        for index in range(len(answerList)):
            if index % 2 != 0:
                answerList[index] = str(int(answerList[index])-30)
            else:
                answerList[index] = str(answerList[index])
        answerStr = ','.join(answerList)
        print('打码平台返回的验证码为:'+ answerStr)
        return answerStr,result  # result是打码平台返回的结果，answerStr是纵坐标减去30后拼接成的字符串


    def ReportError(self, im_id):

        params = {
            'id': im_id,  # im_id:报错验证码的图片ID
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


if __name__ == '__main__':

    const.chaoJiYing.PostPic('captcha.jpg', '9004')

