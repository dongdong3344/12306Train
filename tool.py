import datetime
import  time
import  requests


class Utility(object):

    def __init__(self):
        self.session = self.initSession()


    def initSession(self):

        session = requests.session()  # 创建session会话

        session.headers = {

            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
        }
        # session.verify = False  # 跳过SSL验证
        return session


    def getDepartureDate(self,date = None):
        today = datetime.datetime.today() # 获取今天此刻时间，2019-01-03 12:59:00.062419
        tomorrow = today + datetime.timedelta(days=1) # 获取明天此刻时间，

        if date == None:  # 默认购票时间为明天
            date = tomorrow
        dateList = str(date).split(' ')[0].split('-')
         #2018-12-29分割成2018，12，29
        month = dateList[1]
        day = dateList[2]
        if month.startswith('0'):
            month = month.replace('0', '')
        if day.startswith('0'):
            day = day.replace('0', '')
        if str(date).split(' ')[0] == str(tomorrow).split(' ')[0]:
            return ('{}月{}日'.format(month, day) + ' 明天 ' + self.getWeekDay(date))
        elif str(date).split(' ')[0] == str(today).split(' ')[0]:
            return ('{}月{}日'.format(month, day) + ' 今天 ' + self.getWeekDay(date))
        else:
            return ('{}月{}日'.format(month,day) + ' ' + self.getWeekDay(date))


    def getWeekDay(self, date):
        weekDayDict = {
            0: '周一',
            1: '周二',
            2: '周三',
            3: '周四',
            4: '周五',
            5: '周六',
            6: '周天',
        }
        return weekDayDict[date.weekday()]


    #把字符串转成datetime
    def stringToDatetime(self,st):
        return datetime.datetime.strptime(st, "%Y-%m-%d")


if __name__ == '__main__':
    Utility().getDate()


