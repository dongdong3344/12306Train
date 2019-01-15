
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate, Qt, QSize, QPoint, QRect, QLocale
from PyQt5.QtGui import QColor, QIcon, QPen, QFont, QTextCharFormat
from PyQt5.QtWidgets import QCalendarWidget, QToolButton, QWidget, QLabel


monthDict = {
    '一月': '01', '二月': '02', '三月': '03', '四月': '04',
    '五月': '05', '六月': '06', '七月': '07', '八月': '08',
    '九月': '09', '十月': '10', '十一月': '11', ' 十二月': '12'
}

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
      painter.setFont(QFont('黑体', fontSize))
      painter.drawText(rect, Qt.AlignCenter, text)  # str(date.day())
      painter.restore()


  def paintCell(self,painter,rect,date):

      if date == self.currentDate :
          self.setupPainter(painter,rect,'#d81e06','white','今天',10)
      elif date == self.selectedDate():
          self.setupPainter(painter,rect,'#BBFFFF','red',str(date.day()),12)
      elif date < self.currentDate or date > self.maxDate:
          painter.setPen(QPen(QColor('gray')))
          painter.drawText(rect, Qt.AlignCenter, str(date.day()))
          painter.restore()
      else:
          super(MyCalendar, self).paintCell(painter, rect, date)



if __name__ == '__main__':


    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MyCalendar()
    mainWindow.show()
    sys.exit(app.exec_())