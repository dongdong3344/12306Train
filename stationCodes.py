import os
import re
import json
import const
from APIs import API
from tool import Utility

class StationCodes(object):

    def saveStationCodes(self,session):
        # 若文件存在，则直接return
        if os.path.exists(const.stationCodesFilePath):
            return
        res = session.get(API.stationCode)
        stations = re.findall(r'([\u4e00-\u9fa5]+)\|([A-Z]+)',res.text)
        print(stations)
        # 注意编码格式utf-8
        with open(const.stationCodesFilePath, 'w', encoding='utf-8') as f:
            # ensure_ascii = False 防止乱码
            f.write(json.dumps(dict(stations),ensure_ascii = False))

    def getCodesDict(self):
        with open(const.stationCodesFilePath, 'r', encoding='utf-8') as file:
            dict = json.load(file)
            return dict


    def getStations(self):
        return self.getCodesDict().keys()




if __name__ == '__main__':
    StationCodes.saveStationCodes(Utility().session)
    StationCodes().getStations()