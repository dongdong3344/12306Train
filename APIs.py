
class API(object):
    # 登录链接
    login = 'https://kyfw.12306.cn/passport/web/login'
    # 验证码验证链接
    captchaCheck = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
    # 获取验证码图片
    captchaImage = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand'
    # 车站Code
    stationCode = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
    # 查余票
    queryTicket = 'https://kyfw.12306.cn/otn/leftTicket/query'
    # 查票价
    queryPrice = 'https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice'

    # 检查用户
    checkUser = 'https://kyfw.12306.cn/otn/login/checkUser'
    # 用户登录
    userLogin = 'https://kyfw.12306.cn/otn/login/userLogin'

    uamtk = 'https://kyfw.12306.cn/passport/web/auth/uamtk'

    uamauthclient = 'https://kyfw.12306.cn/otn/uamauthclient'

    initMy12306 = 'https://kyfw.12306.cn/otn/index/initMy12306'

    # 确定订单信息
    submitOrderRequest = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
    # initDc,获取globalRepeatSubmitToken
    initDc = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
    # 获取曾经用户列表
    getPassengerDTOs = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
    # 检查订单信息
    checkOrderInfo = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
    # 获取队列查询
    getQueueCount = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
    # 确认队列
    confirmSingleForQueue = 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'