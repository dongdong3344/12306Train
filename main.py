import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, QDate, QPropertyAnimation, QRect, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QPushButton, QStylePainter, QStyle, QMainWindow

from query import Ui_MainWindow
from tool import Utility
from myCalendar import MyCalendar

calHeight = 280
checkBoxQSS = '''
           QCheckBox{color: white}
           QCheckBox::indicator {width: 20px; height: 20px}
           QCheckBox::indicator:unchecked {image:url(Pictures/unselect.png)}
           QCheckBox::indicator:checked {image:url(Pictures/selected.png)}
      '''

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.initUI()


    def initUI(self):
        self.setupUi(self)
        self.setupCSSStyle()
        self.utility = Utility() #实例化工具类
        # self.setFixedSize(QSize(self.width(),self.height()))  #禁止拉伸窗口大小
        self.winHeight = self.height() # 获取窗体高度，便用
        self.setWindowIcon(QIcon('Pictures/train.png'))  #设置图标
        self.logoLabel.resize(150,150)
        self.logoLabel.setScaledContents(True) #图片填满label
        self.logoLabel.setPixmap(QPixmap('Pictures/train3.png')) #设置label上的图片

        self.exchangeButton.setIcon(QIcon("Pictures/exchange.png")) # 设置Icon
        self.exchangeButton.setIconSize(QSize(50, 50))  # 设置交换按钮icon size
        self.exchangeButton.clicked.connect(self.exchangePlace)

        self.timeButton.setText(self.utility.getDepartureDate()) #设置出发日期
        self.timeButton.setIcon(QIcon("Pictures/calendar.png")) # 设置Icon
        self.timeButton.clicked.connect(self.selectDate)

        self.startButton.setIcon(QIcon("Pictures/start.png"))  # 设置Icon
        self.destinationButton.setIcon(QIcon("Pictures/destination.png"))

        self.studentCheckBox.stateChanged.connect(lambda: self.iSBoxChecked(self.studentCheckBox))
        self.highSpeedCheckBox.stateChanged.connect(lambda: self.iSBoxChecked(self.highSpeedCheckBox))



    def selectDate(self):
        x = self.timeButton.x()  # 获取时间按钮的坐标x
        y = self.timeButton.y() + self.timeButton.height()
        w = self.timeButton.width()
        h = calHeight
        self.cal = MyCalendar(self)
        self.cal.setGeometry(x,y,w,h)
        self.cal.clicked[QDate].connect(self.showDate)  # clicked[参数]，即定义showDate是传入的参数类型设置
        self.cal.show()
        self.startRect = QRect(self.geometry().x(), self.geometry().y(), self.width(), self.height())
        self.endRect = QRect(self.geometry().x(), self.geometry().y(), self.width(), self.cal.y() + self.cal.height() + 15)
        self.setFrameAnimation(self.startRect, self.endRect)
        self.timeButton.setEnabled(False)

    def setFrameAnimation(self, startRect, endRect):
        self.animation = QPropertyAnimation(self, b'geometry')
        self.animation.setDuration(250)
        self.animation.setStartValue(startRect)
        self.animation.setEndValue(endRect)
        self.animation.start()


    def showDate(self,date):

        dateStr = date.toString('yyyy-MM-dd')
        dateTime = self.utility.stringToDatetime(dateStr)
        self.timeButton.setText(self.utility.getDepartureDate(dateTime)) #"yyyy-MM-dd ddd(星期)"
        self.setFrameAnimation(self.endRect, self.startRect)
        self.cal.close()  # 关闭日期控件
        self.timeButton.setEnabled(True)


    def iSBoxChecked(self,checkBox):

        if checkBox.isChecked():
            checkBox.setStyleSheet(checkBoxQSS + "QCheckBox{color:#d81e06}")
        else:
            checkBox.setStyleSheet(checkBoxQSS)

        if self.studentCheckBox.isChecked():
            self.queryButton.setText('查询学生票')
        else:
            self.queryButton.setText('查询车票')


    def exchangePlace(self):
        startPlace = self.startButton.text()
        self.startButton.setText(self.destinationButton.text())
        self.destinationButton.setText(startPlace)

    def setupCSSStyle(self):
        # self.setStyleSheet("QMainWindow{background-color:white}")
        self.setStyleSheet("QMainWindow{border-image: url(Pictures/bg3.jpg)}") #设置背景图

        self.exchangeButton.setStyleSheet("QPushButton{background-color:transparent}")


        self.queryButton.setStyleSheet("QPushButton{color:white}"
                                       "QPushButton{background-color:#d81e06}"
                                       "QPushButton{border:1px}"
                                       "QPushButton{border-radius:5px}"
                                       "QPushButton{padding:2px 4px}")

        self.destinationButton.setStyleSheet(self.getButtonQSS('right'))

        for button in (self.startButton,self.timeButton):
            button.setStyleSheet(self.getButtonQSS('left'))

        for checkBox in (self.highSpeedCheckBox,self.studentCheckBox):
                checkBox.setStyleSheet(checkBoxQSS)


    def getButtonQSS(self,str):
       return  'QPushButton{text-align:%s;color:white;background-color:transparent;qproperty-iconSize: 25px}' % str
       # qproperty-iconSize 设置icon size

class RotatedButton(QPushButton):
    def __init__(self,parent = None):
        super(RotatedButton,self).__init__(parent)
        self.setStyleSheet('QPushButton{background-color:white}')

    def paintEvent(self, event):
        painter = QStylePainter(self)
        painter.rotate(90)
        painter.translate(0, -1 * self.width())




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())