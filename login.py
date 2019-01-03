# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(489, 373)
        Dialog.setModal(True)
        self.remberCheckBox = QtWidgets.QCheckBox(Dialog)
        self.remberCheckBox.setGeometry(QtCore.QRect(110, 200, 101, 20))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.remberCheckBox.setFont(font)
        self.remberCheckBox.setObjectName("remberCheckBox")
        self.userNameEdit = QtWidgets.QLineEdit(Dialog)
        self.userNameEdit.setGeometry(QtCore.QRect(110, 110, 280, 35))
        self.userNameEdit.setObjectName("userNameEdit")
        self.passwordEdit = QtWidgets.QLineEdit(Dialog)
        self.passwordEdit.setGeometry(QtCore.QRect(110, 155, 280, 35))
        self.passwordEdit.setText("")
        self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordEdit.setObjectName("passwordEdit")
        self.loginButton = QtWidgets.QPushButton(Dialog)
        self.loginButton.setGeometry(QtCore.QRect(110, 240, 280, 40))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.loginButton.setFont(font)
        self.loginButton.setAutoDefault(False)
        self.loginButton.setFlat(False)
        self.loginButton.setObjectName("loginButton")
        self.bgLabel = QtWidgets.QLabel(Dialog)
        self.bgLabel.setGeometry(QtCore.QRect(70, 75, 360, 240))
        self.bgLabel.setText("")
        self.bgLabel.setObjectName("bgLabel")
        self.errorLabel = QtWidgets.QLabel(Dialog)
        self.errorLabel.setGeometry(QtCore.QRect(40, 340, 420, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.errorLabel.setFont(font)
        self.errorLabel.setText("")
        self.errorLabel.setScaledContents(False)
        self.errorLabel.setObjectName("errorLabel")
        self.bgLabel.raise_()
        self.remberCheckBox.raise_()
        self.userNameEdit.raise_()
        self.passwordEdit.raise_()
        self.loginButton.raise_()
        self.errorLabel.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "用户登录"))
        self.remberCheckBox.setText(_translate("Dialog", "记住账号"))
        self.userNameEdit.setPlaceholderText(_translate("Dialog", "用户名/邮箱/手机号"))
        self.passwordEdit.setPlaceholderText(_translate("Dialog", "密码"))
        self.loginButton.setText(_translate("Dialog", "登录"))

