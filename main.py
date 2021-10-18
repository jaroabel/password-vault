import sys
import sqlite3, hashlib
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem
from PyQt5.uic import loadUi

from dbmodel import db_queries

# Database code
# Database code
with sqlite3.connect("password_vault.db") as db:
    cursor = db.cursor()

cursor.execute(db_queries['master'])
cursor.execute(db_queries['login'])

# db_conn = Dbconnect()

class HashPassword():
    def __init__(self):
        self.hash = ""

    def hash_password(self, input):
        self.hash = hashlib.md5(input)
        self.hash = self.hash.hexdigest()
        return self.hash


class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("welcompage.ui", self)
        self.loginButton.clicked.connect(self.displayLogin)
        self.passwordInput.setEchoMode(QtWidgets.QLineEdit.Password)

    def displayLogin(self):
        password = self.passwordInput.text()
        data = ('Apple', 'www.apple.com', 'jeff', 'colt@123')
        insert_new = "INSERT INTO vault (site_name, website, username, password) VALUES(?, ?, ?, ?);"
        cursor.execute(insert_new, data)
        db.commit()
        window = ShowVault()
        print(f"clicked on the login Button and enter password: {password}")

class MasterPassword(QDialog):
    def __init__(self):
        super(MasterPassword, self).__init__()
        loadUi("create_master_account.ui", self)
        self.createAccountBtn.clicked.connect(self.create_master_pass)
        self.masterPass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.masterPassConfirm.setEchoMode(QtWidgets.QLineEdit.Password)

    def create_master_pass(self):
        if self.masterPass.text() == self.masterPassConfirm.text():
            password = self.masterPass.text()

            set_hash = HashPassword()
            hashPassword = set_hash.hash_password(self.masterPass.text().encode('utf-8'))
            insert_password = """ INSERT INTO master_password(password) VALUES(?) """
            cursor.execute(insert_password, [(hashPassword)])
            db.commit()
            print(f"Successful created master password: {password}")


class ShowVault(QDialog):
    def __init__(self):
        super(ShowVault, self).__init__()
        loadUi("password_show_vault.ui", self)
        self.show_data_in_table()

    def show_data_in_table(self):
        cursor.execute("SELECT * FROM vault")
        row_fetchall = cursor.fetchall()
        cnt = 0
        num_row = len(row_fetchall)
        self.tableWidget.setRowCount(num_row)
        for row in row_fetchall:
            self.tableWidget.setItem(cnt, 0, QTableWidgetItem(str(row[0])))
            self.tableWidget.setItem(cnt, 1, QTableWidgetItem(row[1]))
            self.tableWidget.setItem(cnt, 2, QTableWidgetItem(row[2]))
            self.tableWidget.setItem(cnt, 3, QTableWidgetItem(row[3]))
            self.tableWidget.setItem(cnt, 4, QTableWidgetItem(row[4]))
            cnt = cnt + 1

        self.addButton.clicked.connect(self.add_new_password)

    def add_new_password(self):
        sitename = self.siteName.text()
        siteurl = self.siteUrl.text()
        username = self.userName.text()
        password = self.passWord.text()

        data = (sitename, siteurl, username, password)
        insert_new = "INSERT INTO vault (site_name, website, username, password) VALUES(?, ?, ?, ?);"
        cursor.execute(insert_new, data)
        db.commit()
        self.tableWidget.setRowCount(0) # Clear the table
        self.show_data_in_table()


app = QApplication(sys.argv)


def show_window():
    cursor.execute("SELECT * FROM master_password")
    if cursor.fetchall():
        #window = Login()
        window = ShowVault()
    else:
        window = MasterPassword()
    return window

window = show_window()
widget = QtWidgets.QStackedWidget()
widget.addWidget(window)
#widget.setFixedWidth(346)
#widget.setFixedHeight(427)

widget.setFixedWidth(833)
widget.setFixedHeight(504)
widget.show()
app.exec_()


