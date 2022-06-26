import sys
import sqlite3, hashlib
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from dbmodel import db_queries

# Database connextion
with sqlite3.connect("password_vault.db") as db:
    cursor = db.cursor()

cursor.execute(db_queries['master'])
cursor.execute(db_queries['login'])


# Create hashed password
class HashPassword():
    def __init__(self):
        self.hash = ""

    def hash_password(self, input):
        self.hash = hashlib.md5(input)
        self.hash = self.hash.hexdigest()
        return self.hash


# Login window
class Login(QDialog, HashPassword):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("welcompage.ui", self)
        self.loginButton.clicked.connect(self.displayLogin)
        self.passwordInput.setEchoMode(QtWidgets.QLineEdit.Password)

    def displayLogin(self):
        password = self.passwordInput.text()
        # check if password exist in DB
        get_hash_password = self.hash_password(password.encode('utf-8')) # convert text password to hash
        qry = "SELECT * FROM master_password WHERE password = ?"
        cursor.execute(qry, (get_hash_password,))
        if cursor.fetchall():
            # Display the vault window (widget)
            window = ShowVault()
            widget.addWidget(window)
            widget.setCurrentIndex(widget.currentIndex() + 1)
            widget.setFixedWidth(884)
            widget.setFixedHeight(652)
        else:
            QMessageBox.information(self, "Warning", "Sorry no matching password!\nPLease try again")




# Master password window
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

            # encode master password and store in database
            set_hash = HashPassword()
            hashPassword = set_hash.hash_password(self.masterPass.text().encode('utf-8'))
            insert_password = """ INSERT INTO master_password(password) VALUES(?) """
            cursor.execute(insert_password, [(hashPassword)])
            db.commit()
            print(f"Successful created master password: {password}")

            # Display the login window (widget)
            window = Login()
            widget.addWidget(window)
            widget.setCurrentIndex(widget.currentIndex()+1)
            widget.setFixedWidth(346)
            widget.setFixedHeight(427)




# show vault
class ShowVault(QDialog):
    def __init__(self):
        super(ShowVault, self).__init__()
        loadUi("password_show_vault.ui", self)
        self.show_data_in_table()

    # Get data from the database to populate the table rows
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
            self.tableWidget.setItem(cnt, 5, QTableWidgetItem(row[5]))
            cnt = cnt + 1

        self.addButton.clicked.connect(self.add_new_password)


    # Add a new password to the vault
    def add_new_password(self):
        sitename = self.siteName.text()
        siteurl = self.siteUrl.text()
        username = self.userName.text()
        password = self.passWord.text()

        data = (sitename, siteurl, username, password)
        insert_new = "INSERT INTO vault (site_name, website, username, password) VALUES(?, ?, ?, ?);"
        cursor.execute(insert_new, data)
        db.commit()
        # Clear the table
        self.tableWidget.setRowCount(0)
        # call function to reload table with the new data
        self.show_data_in_table()


app = QApplication(sys.argv)

# Check if a master password was already created
def show_window():
    cursor.execute("SELECT * FROM master_password")
    if cursor.fetchall():
        window = Login()
    else:
        window = MasterPassword()
    return window

window = show_window()
widget = QtWidgets.QStackedWidget()
widget.addWidget(window)
widget.setFixedWidth(346)
widget.setFixedHeight(427)

widget.show()
app.exec_()


