import re
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, pyqtSignal, QRunnable, QThreadPool, QRect, QSettings, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QLineEdit, QDialog, QLabel
from waitingspinnerwidget import QtWaitingSpinner
from main import  MainWindow
from APIs import API
import const
from login import Ui_Dialog
from tool import Utility

rememberBoxStyle = '''
                    QCheckBox::indicator {width: 20px; height: 20px}
                    QCheckBox::indicator:unchecked {image:url(Pictures/unselect.png)}
                    QCheckBox::indicator:checked {image:url(Pictures/selected.png)}
'''

lineEditStyle = '''
                  QLineEdit{border-width:5px;border-radius:5px;font-size:12px;color:black;border:1px solid gray}
                  QLineEdit{padding-left:10px}
                  QLineEdit:hover{border-width:5;border:1px rgb(160,50,25)}
'''



class RequestRunnable(QRunnable):

    def __init__(self,target):
        super(RequestRunnable,self).__init__()
        self.target =target

    def run(self):
      self.target()


class LoginDialog(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self,parent = None):
        super(LoginDialog, self).__init__(parent)
        self.initUI()
        self.session = Utility().session
        self.userName = None


    def initUI(self):
        self.setupUi(self)
        self.setFixedSize(QSize(self.width(),self.height()))
        self.setWindowIcon(QIcon('Pictures/loginIcon.png'))
        self.setWindowTitle('12306登录')
        # self.userNameEdit.setClearButtonEnabled(True) #设置清空按钮

        self.setLineEditIcon(self.passwordEdit, 'Pictures/password_new.png')
        self.setLineEditIcon(self.userNameEdit, 'Pictures/user_new.png')

        self.userNameEdit.textChanged.connect(self.isLoginable)
        self.passwordEdit.textChanged.connect(self.isLoginable)

        self.loginButton.clicked.connect(self.login)

        self.initSettings()

        self.setupStyleSheet()

        self.isLoginable()

        self.initSpinner()

        self.initMessageLabel()

        self.remberCheckBox.stateChanged.connect(self.setupRememberCheck)


    def setupRememberCheck(self):

        if self.remberCheckBox.checkState() :
            self.remberCheckBox.setStyleSheet(rememberBoxStyle + 'QCheckBox{color:#d81e06}')
            self.settings.setValue('isChecked', True)
            self.settings.setValue('username', self.userNameEdit.text())
            self.settings.setValue('password', self.passwordEdit.text())
        else:
            self.remberCheckBox.setStyleSheet(rememberBoxStyle + 'QCheckBox{color:white}')
            self.settings.setValue('isChecked', False)
        self.settings.sync()


    def isLoginable(self):
        self.messageLabel.hide()

        if self.userNameEdit.text() == '' or self.passwordEdit.text() =='':
            self.loginButton.setStyleSheet('QPushButton{color:white;background-color:rgba(0,0,0,0.5);border:1px;border-radius:5px;}')
            self.loginButton.setEnabled(False)
        else:
            self.loginButton.setStyleSheet("QPushButton{color:white;background-color:rgb(250,80,0);border-radius:5px}")
            self.loginButton.setEnabled(True)

    def login(self):

        self.spinner.start()
        runnable = RequestRunnable(target=self.login12306)
        self.pool = QThreadPool.globalInstance()
        self.pool.start(runnable)


    def login12306(self):
        # step 1: check验证码

        self.captchaCheck()

        # step 2: login
        loginData = {
            'username': self.userNameEdit.text(),
            'password': self.passwordEdit.text(),
            'appid': 'otn'
        }
        result = self.session.post(API.login, data=loginData).json()


        if result['result_code'] != 0:  # 出错的话，显示错误信息
            self.messageLabel.setText('出错啦:' + result['result_message'])
            self.messageLabel.show()
            self.spinner.stop()
            return

        # step 3：checkuser
        data = {
            '_json_att': ''
        }
        self.session.post(API.checkUser, data=data)

        # step 4: uamtk
        data = {
            'appid': 'otn'
        }
        uamtk_res = self.session.post(API.uamtk, data=data)
        newapptk = uamtk_res.json()['newapptk']

        # step 5: uamauthclient
        clientData = {
            'tk': newapptk
        }
        uamauthclient_res = self.session.post(API.uamauthclient, data=clientData)
        username = uamauthclient_res.json()['username']
        self.userName = username

        # step 6: initMy12306
        html = self.session.get(API.initMy12306).text

        genderStr = re.findall(r'<div id="my12306page".*?</span>(.*?)</h3>', html, re.S)[0].replace('\n', '').split('，')[0]
        print("恭喜{}成功登录12306网站".format(username))
        if genderStr:
            self.accept()


    # 获取验证码正确答案
    def getCaptchaAnswer(self):
        response = self.session.get(API.captchaImage)
        if response.status_code == 200:
            print('验证码图片请求成功')
            with open(const.captchaFilePath, 'wb') as f:
                f.write(response.content)  # 写入文件
        else:
            print('验证码图片下载失败, 正在重试...')
            self.getCaptchaAnswer()  # 递归
        try:
            img = open(const.captchaFilePath, 'rb').read()  # 读取文件图片
            answerStr, cjyAnswerDict = const.chaoJiYing.PostPic(img, 9004)
            return answerStr, cjyAnswerDict  # 返回自己写的验证码信息和平台反应的信息
        except Exception as e:
            print(str(e))

    def captchaCheck(self):
        answer,cjyAnswerDict = self.getCaptchaAnswer()

        data = {
            'login_site':'E',  # 固定的
            'rand': 'sjrand',  # 固定的
            'answer': answer   # 验证码对应的坐标，两个为一组，跟选择顺序有关,有几个正确的，输入几个
        }
        result = self.session.post(API.captchaCheck,data=data).json()

        if result['result_code'] == '4':
            print('验证码验证成功')
        else:
            print('验证码验证失败')
            picID = cjyAnswerDict['pic_id']
            # 报错到打码平台
            const.chaoJiYing.ReportError(picID)
            self.captchaCheck()
            return


    def setLineEditIcon(self, lineEdit, iconPath):
        action = QAction(lineEdit)
        action.setIcon(QIcon(iconPath))
        lineEdit.addAction(action, QLineEdit.TrailingPosition) #LeadingPosition


    def setupStyleSheet(self):

        self.setStyleSheet('QDialog{border-image:url(Pictures/loginBg.png)}')

        self.bgLabel.setStyleSheet('QLabel{background-color:rgba(0,0,0,0.25);border-radius:5px}' )# 设置透明背景色

        if self.settings.value('isChecked') =='true':
            self.remberCheckBox.setStyleSheet('QCheckBox{color:#d81e06}' + rememberBoxStyle)
        else:
            self.remberCheckBox.setStyleSheet('QCheckBox{color:white}'+ rememberBoxStyle)

        self.userNameEdit.setStyleSheet(lineEditStyle)
        self.passwordEdit.setStyleSheet(lineEditStyle)

    def initSettings(self):

        self.settings = QSettings('Honeywell', '12306Train')
        if self.settings.value('isChecked') == 'true':
            self.remberCheckBox.setChecked(True)
            self.userNameEdit.setText(self.settings.value('username'))
            self.passwordEdit.setText(self.settings.value('password'))
        else:
            self.remberCheckBox.setChecked(False)

    def initMessageLabel(self):
        self.messageLabel.adjustSize()
        self.messageLabel.setGeometry(QRect(70, 15, 360, 50))
        self.messageLabel.setWordWrap(True)
        self.messageLabel.setScaledContents(True)
        self.messageLabel.setStyleSheet(
            'QLabel{background-color:rgb(255,0,79);color:white;font:9pt;padding-left:5px;padding-right:5px;}')  # border-radius:5px

        # height = self.messageLabel.fontMetrics().boundingRect(self.messageLabel.text()).height()
        self.messageLabel.hide()

    def initSpinner(self):
        self.spinner = QtWaitingSpinner(self, centerOnParent=True, disableParentWhenSpinning=True)
        self.spinner.setNumberOfLines(15)
        # self.spinner.setColor(QColor(81, 4, 71))
        self.spinner.setInnerRadius(20)  # 设置内圆大小
        self.spinner.setLineLength(15)  # 设置线长
        self.spinner.setLineWidth(5)  # 设置线宽
        self.spinner.setTrailFadePercentage(80)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    loginDialog = LoginDialog()
    if loginDialog.exec_() == QDialog.Accepted:
        mainWindow = MainWindow()
        mainWindow.setWindowTitle('{},欢迎您进入余票查询'.format(loginDialog.userName))
        mainWindow.show()
        sys.exit(app.exec_())






