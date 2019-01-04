import re
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, pyqtSignal, QRunnable, QThreadPool
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QLineEdit, QDialog, QLabel
from waitingspinnerwidget import QtWaitingSpinner
from main import  MainWindow
from APIs import API
import const
from login import Ui_Dialog
from tool import Utility


class RequestRunnable(QRunnable):

    def __init__(self,target):
        super(RequestRunnable,self).__init__()
        self.target =target


    def run(self):
      self.target()

    def start(self):
        QThreadPool.globalInstance().start(self)


class LoginDialog(QtWidgets.QDialog, Ui_Dialog):
    doneSignal = pyqtSignal()
    def __init__(self,parent = None):
        super(LoginDialog, self).__init__(parent)
        self.initUI()
        self.session = Utility().session
        self.gifLabel = QLabel(self)
        # self.showLoading()
        self.userName = ''
        self.loginButton.clicked.connect(self.login)



    def initUI(self):
        self.setupUi(self)
        self.setFixedSize(QSize(self.width(),self.height()))
        self.setWindowIcon(QIcon('Pictures/loginIcon.png'))
        self.setWindowTitle('12306登录')
        # self.userNameEdit.setClearButtonEnabled(True) #设置清空按钮

        self.setIcon(self.passwordEdit,'Pictures/password_new.png')
        self.setIcon(self.userNameEdit,'Pictures/user_new.png')
        self.userNameEdit.textChanged.connect(self.isLoginClickable)
        self.passwordEdit.textChanged.connect(self.isLoginClickable)

        self.initCSS()

        self.initSpinner()

        self.remberCheckBox.stateChanged.connect(lambda :self.isBoxChecked(self.remberCheckBox))


    def initSpinner(self):
        self.spinner = QtWaitingSpinner(self, centerOnParent=True, disableParentWhenSpinning=True)
        self.spinner.setNumberOfLines(15)
        # self.spinner.setColor(QColor(81, 4, 71))
        self.spinner.setInnerRadius(20)  #设置内圆大小
        self.spinner.setLineLength(15)  #设置线长
        self.spinner.setLineWidth(5)  # 设置线宽
        self.spinner.setTrailFadePercentage(80)


    def isBoxChecked(self,checkBox):
        if checkBox.isChecked():
            checkBox.setStyleSheet("QCheckBox{color:#d81e06}"
                                               "QCheckBox::indicator {width: 20px; height: 20px}"
                                               "QCheckBox::indicator:unchecked {image:url(Pictures/unselect.png)}"
                                               "QCheckBox::indicator:checked {image:url(Pictures/selected.png)}")
        else:
            checkBox.setStyleSheet("QCheckBox{color:white}"
                                               "QCheckBox::indicator {width: 20px; height: 20px}"
                                               "QCheckBox::indicator:unchecked {image:url(Pictures/unselect.png)}"
                                               "QCheckBox::indicator:checked {image:url(Pictures/selected.png)}")


    def isLoginClickable(self):
        if self.userNameEdit.text() =='' or self.passwordEdit.text() =='':
            self.initLoginButton()
        else:
            self.loginButton.setStyleSheet("QPushButton{color:white}"
                                       "QPushButton{background-color:orange}"
                                       "QPushButton{border:1px}"
                                       "QPushButton{border-radius:5px}"
                                       "QPushButton{padding:2px 4px}")
            self.loginButton.setEnabled(True)



    def login(self):

        self.spinner.start()

        self.pool = RequestRunnable(target=self.login12306)
        self.pool.start()



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
        print(result)
        if result['result_code'] != 0:  # 出错的话，显示错误信息
            self.errorLabel.setText(result['result_message'])
            self.spinner.hide()
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

        genderStr = \
        re.findall(r'<div id="my12306page".*?</span>(.*?)</h3>', html, re.S)[0].replace('\n', '').split('，')[0]
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


    def setIcon(self,lineEdit,iconPath):
        action = QAction(lineEdit)
        action.setIcon(QIcon(iconPath))
        lineEdit.addAction(action, QLineEdit.TrailingPosition) #LeadingPosition


    def initLoginButton(self):
        self.loginButton.setStyleSheet('QPushButton{color:white;background-color:rgba(0,0,0,0.5);border:1px;border-radius:5px}')

        self.loginButton.setEnabled(False)

    def initCSS(self):
        # self.setStyleSheet("QDialog{background-color:white}")

        self.errorLabel.setStyleSheet("QLabel{color:red}")
        self.setStyleSheet("QDialog{border-image:url(Pictures/loginBg.png)}")

        self.initLoginButton()

        self.bgLabel.setStyleSheet("QLabel{background-color:rgba(0,0,0,0.25)}" # 设置透明背景色
                                   "QLabel{border-radius:5px}")
        self.remberCheckBox.setStyleSheet("QCheckBox{color:white}"
                                           "QCheckBox::indicator {width: 20px; height: 20px}"
                                           "QCheckBox::indicator:unchecked {image:url(Pictures/unselect.png)}"
                                           "QCheckBox::indicator:checked {image:url(Pictures/selected.png)}")
        self.setQLineEditStyle(self.userNameEdit)
        self.setQLineEditStyle(self.passwordEdit)


    def setQLineEditStyle(self,qLineEdit):
        qLineEdit.setStyleSheet("QLineEdit{border-width:5px;"
                      "border-radius:5px;font-size:12px;"
                      # "background-color:rgba(255,255,255,0.5);"
                      "color:black;"
                      "border:1px solid gray}"
                      "QLineEdit{padding-left:10px}"
                      "QLineEdit:hover{border-width:5;"
                      "border:1px  rgb(160,50,25)}")




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    loginDialog = LoginDialog()
    if loginDialog.exec_() == QDialog.Accepted:
        mainWindow = MainWindow()
        mainWindow.setWindowTitle('{},欢迎您进入查询余票'.format(loginDialog.userName))
        mainWindow.show()
        sys.exit(app.exec_())






