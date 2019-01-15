from PyQt5 import QtCore

from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QPixmap, QPainter, QIcon
from PyQt5.QtWidgets import QWidget, QFormLayout, QPushButton, QApplication



class Captcha(QWidget):
    signal = QtCore.pyqtSignal()

    def __init__(self,parent=None):
        super(Captcha,self).__init__(parent)
        self.setWindowTitle('验证码')

        self.startPoint = 0
        self.endPoint = 0
        self.coordinates = []
        self.captchaImage = 'captcha.jpg'
        self.setLayout(QFormLayout())
        self.resize(290,190)
        self.logo = QPixmap('./Pictures/12306.png')
        self.signal.connect(self.addIcon)

        refreshButton = QPushButton(self)
        refreshButton.setGeometry(250,0,30,30)
        # refreshButton.setText('刷新')
        refreshButton.setIcon(QIcon('Pictures/refresh.png'))
        refreshButton.setStyleSheet('QPushButton{background-color:transparent;qproperty-iconSize: 30px}')
        refreshButton.setToolTip('刷新，重新请求验证码')
        refreshButton.show()


    def addIcon(self):
        x = self.startPoint
        y = self.endPoint -30
        iconButton = QPushButton(self)
        iconButton.setIcon(QIcon('Pictures/12306.png'))
        iconButton.setStyleSheet('QPushButton{background-color:transparent;qproperty-iconSize: 25px}')
        iconButton.setGeometry(self.startPoint,self.endPoint,30,30)
        iconButton.show()
        self.coordinates.append("%s,%s" %(int(x),int(y)))
        iconButton.clicked.connect(lambda :self.deleteIcon(iconButton,x,y))
        return ','.join(self.coordinates)

    def deleteIcon(self,button,x,y):
        self.coordinates.remove("%s,%s" %((int(x),int(y))))
        button.close()
        return ','.join(self.coordinates)

    def mousePressEvent(self, event):
        if (event.type() == QEvent.MouseButtonPress):

            self.startPoint = event.pos().x() - 15
            self.endPoint   = event.pos().y() - 15
            self.signal.emit()

    def paintEvent(self, event):
        p = QPainter(self)
        p.drawPixmap(0, 0,290,190,QPixmap(self.captchaImage) )

if __name__=='__main__':
  import sys
  app=QApplication(sys.argv)
  win=Captcha()
  win.show()
  sys.exit(app.exec_())