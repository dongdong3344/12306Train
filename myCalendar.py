
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate, Qt, QSize, QPoint, QRect, QLocale
from PyQt5.QtGui import QColor, QIcon, QPen, QFont, QTextCharFormat
from PyQt5.QtWidgets import QCalendarWidget, QToolButton, QWidget, QLabel


monthDict = {
    '一月': '1', '二月': '2', '三月': '3', '四月': '4',
    '五月': '5', '六月': '6', '七月': '7', '八月': '8',
    '九月': '9', '十月': '10', '十一月': '11', ' 十二月': '12'
}

currentDateBackgroundColor = '#d81e06'
selectDateBackgroundColor  = '#BBFFFF'

class MyCalendar(QCalendarWidget):
  def __init__(self,parent=None):
      super(MyCalendar,self).__init__(parent)
      self.initUI()
      self.setupTableViewStyles()
      self.initNavigationBar()
      self.initMessageLabel()


  def initUI(self):
      self.setWindowTitle('我的日历')
      self.setWindowIcon(QIcon('Pictures/cal.png'))
      self.setLocale(QLocale(QLocale.Chinese, QLocale.China))  # 设置语言和地区
      self.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)  # 去除周数列表
      self.setGridVisible(False)  # 去除网络线
      # self.setFirstDayOfWeek(1)  # 第一列是周一
      # self.setWindowOpacity(0.5) #设置窗口透明度
      self.setHorizontalHeaderFormat(self.SingleLetterDayNames) #将周一改成一
      self.setupTextFormat()
      self.currentDate = QDate.currentDate()
      self.maxDate = self.currentDate.addDays(29)  # 30天选择期
      self.setDateRange(self.currentDate, self.maxDate)



  def setupTextFormat(self):
      # 表头设置文字颜色
      format = QTextCharFormat()
      format.setForeground(Qt.black)
      format.setBackground(QColor(253, 245, 230))  # lod place color
      format.setFont(QFont('黑体', 10))
      self.setHeaderTextFormat(format)

      # 设置周六、周天颜色
      for day in (Qt.Saturday, Qt.Sunday):
          format = self.weekdayTextFormat(day)
          format.setForeground(QColor('#d81e06'))
          self.setWeekdayTextFormat(day, format)

  def setupTableViewStyles(self):
      self.setStyleSheet("QTableView{alternate-background-color:#DEDEDE;" #周几的背景颜色哦
                         "background-color: white;}" #整个日历表格的背景色
                         "QAbstractItemView:enabled {font: 10pt;" #字号
                         "font-family:Arial;" #字体
                         "color:black;"  #文字颜色
                         # "selection-background-color: lightBlue; " #选择的cell背景色
                         "selection-color:white; }"  #选中的cell文字颜色
                         "QAbstractItemView:disabled {color:gray;}" )


  def initNavigationBar(self):

      self.prevmonthButton = self.findChild(QToolButton, 'qt_calendar_prevmonth')
      self.nextmonthButton = self.findChild(QToolButton, 'qt_calendar_nextmonth')
      self.prevmonthButton.clicked.connect(self.changeLabelText)
      self.nextmonthButton.clicked.connect(self.changeLabelText)
      self.monthButton = self.findChild(QToolButton, 'qt_calendar_monthbutton')
      self.yearButton  = self.findChild(QToolButton, 'qt_calendar_yearbutton')
      self.prevmonthButton.setIcon(QIcon('Pictures/Prev.png'))  # 设置icon
      self.nextmonthButton.setIcon(QIcon('Pictures/Next.png'))
      self.monthButton.hide()  # 隐藏年月按钮
      self.yearButton.hide()

      navBar = self.findChild(QWidget,'qt_calendar_navigationbar')
      navBar.setStyleSheet("QWidget{background-color: orange;min-height:25px;} ")
      layout = navBar.layout()  # QHBoxLayout
      self.monthAndYearLabel = QLabel()  # 年月标签
      self.changeLabelText()
      self.monthAndYearLabel.setAlignment(Qt.AlignCenter)  # 文字居中显示
      self.monthAndYearLabel.setFont(QFont('Arial', 12))
      self.monthAndYearLabel.setStyleSheet('QLabel{color:white}')
      layout.addWidget(self.prevmonthButton)  # 改变位置
      layout.addWidget(self.monthAndYearLabel, Qt.AlignCenter)
      layout.addWidget(self.nextmonthButton)


  def changeLabelText(self):

      self.monthAndYearLabel.setText('{}年{}月'.format(self.yearButton.text(), monthDict[self.monthButton.text()]))


  def initMessageLabel(self):
      label = QLabel()
      label.setFixedHeight(25)  # 设置固定高度
      label.setText('当前预售期为30天，请选择您的出发日期') #这地方你想咋提示就写啥
      label.setAlignment(Qt.AlignCenter)  # 文字居中显示
      label.setFont(QFont('黑体', 8))
      label.setStyleSheet('QLabel{color:gray;background-color:rgb(253,245,230)}')
      self.layout().addWidget(label)


  def setupPainter(self,painter,rect,backgroundColor,textColor,text,fontSize):

      painter.save()
      # painter.fillRect(rect, QColor("#D3D3D3"))
      painter.setPen(Qt.NoPen)
      painter.setBrush(QColor(backgroundColor))
      r = QRect(QPoint(), min(rect.width(), rect.height()) * QSize(1, 1))
      r.moveCenter(rect.center())
      painter.drawEllipse(r)
      painter.setPen(QPen(QColor(textColor)))
      # font = painter.font() #设置字体
      # font.setPixelSize(12)
      painter.setFont(QFont('Arial', fontSize))
      painter.drawText(rect, Qt.AlignCenter, text)  # str(date.day())
      painter.restore()


  def paintCell(self,painter,rect,date):

      if date == self.currentDate: #当前日期
          self.setupPainter(painter,rect,currentDateBackgroundColor,'white','今天',9)
      elif date == self.selectedDate(): #选择的日期
          self.setupPainter(painter,rect,selectDateBackgroundColor,'red',str(date.day()),12)
      elif date < self.currentDate or date > self.maxDate:
          self.setupPainter(painter,rect,'white','gray',str(date.day()),10)
      elif self.currentDate < date < self.maxDate:
          self.setupPainter(painter,rect,'white','black',str(date.day()),10)
      else:
          super(MyCalendar, self).paintCell(painter, rect, date)

      # 每个月只显示当月的日期
      # if date.month() != int(monthDict[self.monthButton.text()]):
      #     self.setupPainter(painter,rect,'white','white','',0)



if __name__ == '__main__':


    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MyCalendar()
    mainWindow.show()
    sys.exit(app.exec_())