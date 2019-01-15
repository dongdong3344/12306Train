import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QSize, QDate, QPropertyAnimation, QRect, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow,QCompleter,QAction,QLineEdit
from query import Ui_MainWindow
from tool import Utility
from myCalendar import MyCalendar
from stationCodes import StationCodes



calHeight = 280
checkBoxQSS = '''
           QCheckBox{color: white}
           QCheckBox::indicator {width: 20px; height: 20px}
           QCheckBox::indicator:unchecked {image:url(Pictures/unselect.png)}
           QCheckBox::indicator:checked {image:url(Pictures/selected.png)}
      '''

class CompleterDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(CompleterDelegate, self).initStyleOption(option, index)

        option.backgroundBrush = QtGui.QColor('white')
        option.palette.setBrush(QtGui.QPalette.Text, QtGui.QColor('black'))
        option.displayAlignment = Qt.AlignLeft


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

        self.exchangeButton.setIcon(QIcon('Pictures/exchange.png')) # 设置Icon
        self.exchangeButton.setIconSize(QSize(50, 50))  # 设置交换按钮icon size
        self.exchangeButton.clicked.connect(self.exchangePlace)

        self.timeButton.setText(self.utility.getDepartureDate())  # 设置出发日期
        self.timeButton.setIcon(QIcon('Pictures/calendar.png'))  # 设置Icon
        self.timeButton.clicked.connect(self.selectDate)

        self.studentCheckBox.stateChanged.connect(lambda: self.iSBoxChecked(self.studentCheckBox))
        self.highSpeedCheckBox.stateChanged.connect(lambda: self.iSBoxChecked(self.highSpeedCheckBox))

        self.stations = StationCodes().getStations()
        self.setupLineEdit()





    def setupLineEdit(self):
        # 增加自动补全
        self.completer = QCompleter(self.stations)
        self.completer.setFilterMode(Qt.MatchStartsWith)  # 起始位置
        delegate = CompleterDelegate(self)
        self.completer.popup().setStyleSheet("QScrollBar{background:skyBlue;}")
        self.completer.popup().setItemDelegate(delegate)

        self.setupEditIcon(self.startLineEdit,'始发地')
        self.setupEditIcon(self.destinationLineEdit,'目的地')


    # def selectStation(self):
    #
    #     self.placeLists = QListWidget(self)
    #     self.placeLists.setGeometry(QRect(self.startButton.x(),self.startButton.y()+self.startButton.height(),self.startButton.width(),self.height()-self.startButton.y()-self.startButton.height()))
    #     self.placeLists.addItems(self.stations)
    #
    #     self.placeLists.setSortingEnabled(True)
    #     # self.placeLists.sortItems()  # 排序
    #     self.placeLists.setCurrentRow(0)
    #     self.placeLists.setStyleSheet("QListWidget{color:black; background:white}"
    #                        "QListWidget::Item{padding-top:2.5px; padding-bottom:2.5px; }"
    #                        "QListWidget::Item:hover{background:skyblue; }"  #下拉滑动背景色
    #                        "QListWidget::item:selected{ color:red; background:skyblue;}" #当前被选择的item背景，颜色
    #                        "QListWidget::item:selected:!active{ background:skyblue; }")
    #
    #     self.placeLists.currentItemChanged.connect(self.selectPlaceItem)
    #
    #     self.placeLists.show()
    #
    #
    # def selectPlaceItem(self):
    #
    #     self.startButton.setText(self.placeLists.currentItem().text())
    #     self.placeLists.close()

    def setupEditIcon(self,lineEdit,placeHolderText):
        if lineEdit==self.startLineEdit:
            iconPath = 'Pictures/start.png'
        else:
            iconPath = 'Pictures/destination.png'
        lineEdit.setCompleter(self.completer)
        lineEdit.setPlaceholderText(placeHolderText)
        action = QAction(lineEdit)
        action.setIcon(QIcon(iconPath))
        lineEdit.addAction(action, QLineEdit.LeadingPosition)

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
        self.endRect   = QRect(self.geometry().x(), self.geometry().y(), self.width(), self.cal.y() + self.cal.height() + 15)
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
        startPlace = self.startLineEdit.text()
        self.startLineEdit.setText(self.destinationLineEdit.text())
        self.destinationLineEdit.setText(startPlace)


    def setupCSSStyle(self):
        # self.setStyleSheet("QMainWindow{background-color:white}")
        self.setStyleSheet("QMainWindow{border-image: url(Pictures/bg3.jpg)}") #设置背景图

        self.exchangeButton.setStyleSheet("QPushButton{background-color:transparent}")

        self.queryButton.setStyleSheet('QPushButton{color:white;background-color:#d81e06;border:1px;border-radius:5px}')

        self.timeButton.setStyleSheet('QPushButton{text-align:left;color:white;background-color:transparent;qproperty-iconSize: 25px}')


        for lineEdit in (self.startLineEdit,self.destinationLineEdit):
            lineEdit.setStyleSheet("QLineEdit{border-width:5px;border-radius:5px;font-size:12pt;padding-left:2px;"
                          "background-color:transparent;color:white;font-familiy:黑体;font-weight:bold;"
                          "border: 1px solid lightGray;}")

        self.highSpeedCheckBox.setStyleSheet(checkBoxQSS)
        self.studentCheckBox.setStyleSheet(checkBoxQSS)




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())