from  codePlatform import  CJYClient

# 12306登录用户名
userName = 'dongdong3344@163.com'
# 12306密码
password = 'dongdong3344'
# 超级鹰打码平台
chaoJiYing = CJYClient('dongdong3344', 'dongdong3344!','896970')

# 验证码图片路径
captchaFilePath = 'captcha.jpg'
# 车站电报码路径
stationCodesFilePath = 'stationsCode.txt'

# 座位类型，订票下单时需要传入
noSeat            = 'WZ' #无座
firstClassSeat    = 'M'  #一等座
secondClassSeat   = 'O'  #二等座
advancedSoftBerth = '6'  #高级软卧 A6
hardBerth         = '3'  #硬卧 A3
softBerth         = '4'  #软卧 A4
moveBerth         = 'F'  #动卧
hardSeat          = '1'  #硬座 A1
businessSeat      = '9'  #商务座 A9

