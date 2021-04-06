# This is a sample Python script.

# Press Shift+F10 to execute it  or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sqlite3
import uuid
from sqlite3 import Error
import hashlib
import tkinter as tk
import tkinter.messagebox


def sql_connection(root):
    try:
        con = sqlite3.connect('database.db')
        return con
    except Error:
        tkinter.messagebox.showerror("Помилка", "Помилка при під'єднанні до бази даних")
        root.destroy()


def hashing(passw, salt):
    amount = 1024
    pasw = salt.encode() + passw.encode()
    for i in range(amount):
        pasw = hashlib.sha256(pasw).hexdigest()
        pasw = bytes.fromhex(pasw)
    return pasw.hex(), salt


def sql_table(root, con):
    try:
        cursorObj = con.cursor()
        cursorObj.execute(
            " CREATE TABLE IF NOT EXISTS users(username VARCHAR(30) PRIMARY KEY, pass CHAR(512), salt CHAR(512), blocked TINYINT, "
              "passrestrictions TINYINT, admin TINYINT)")
        con.commit()
    except Error:
        tkinter.messagebox.showerror("Помилка", "Помилка при cтворенні таблиці. Спробуйте пізніше!")
        root.destroy()


def createRoot(root, con):
    curs = con.cursor()
    curs.execute('SELECT * FROM users')
    res = curs.fetchall()
    if res == []:
        try:
            curs = con.cursor()
            salt = uuid.uuid4().hex
            hashh = hashing(" ", salt)
            curs.execute('INSERT INTO users VALUES ("Admin", ?,?,0,0,1);', hashh)
            con.commit()
        except Error:
            tkinter.messagebox.showerror("Помилка", "Помилка при створенні адміністратора. Спробуйте пізніше!")
            root.destroy()


def checkpass(usrname, pasw, con):
    curs = con.cursor()
    param = list()
    param.append(usrname)
    curs.execute('SELECT * FROM users WHERE username=?;', param)
    res = curs.fetchone()
    if res is not None:
        passcheck = res[1]
        saltchck = res[2]
        pasw = hashing(pasw, saltchck)[0]
        if passcheck == pasw:
            return True
        else:
            tkinter.messagebox.showerror("Помилка", "Помилка при вході, перевірте введені дані!")
            return False
    else:
        tkinter.messagebox.showerror("Помилка", "Помилка при вході, перевірте введені дані!")
        return False


def adduser(username, pasw, con):
    curs = con.cursor()
    param = list()
    param.append(username)
    curs.execute('SELECT * FROM users WHERE username=?;', param)
    res = curs.fetchone()
    if res is not None:
        tkinter.messagebox.showerror("Помилка", "Користувач з таким ім'ям вже існує!")
        return False
    else:
        param = list()
        param.append(username)
        salt = uuid.uuid4().hex
        pasw = hashing(pasw, salt)
        param.append(pasw[0])
        param.append(pasw[1])
        try:
            curs.execute("INSERT INTO users VALUES(?,?,?,0,0,0);", param)
            con.commit()
            tkinter.messagebox.showinfo("Adding", "Користувача додано")
            return True
        except Error:
            tkinter.messagebox.showerror("Помилка", "Помилка під час додавання користувача!")
            return False


def parseusers(con):
    curs = con.cursor()
    try:
        curs.execute("SELECT username, blocked,passrestrictions, admin FROM users ")
        res = curs.fetchall()
        con.commit()
        return res
    except Error:
        tkinter.messagebox.showerror("Помилка", "Помилка під час отримання інформації про користувачів!")
        return None


def changesusrinfo(name, blocked, passrestrict, con):

    param = list()
    param.append(blocked)
    param.append(passrestrict)
    param.append(name)
    try:
        curs = con.cursor()
        curs.execute("UPDATE users SET blocked=?,passrestrictions=? WHERE username=?", param)
        con.commit()
    except Error:
        tkinter.messagebox.showerror("Помилка", "Помилка при змінені даних користувача!")


def parseinform(username, con):
    curs = con.cursor()
    param= list()
    param.append(username)
    curs.execute("SELECT * FROM users WHERE username=?",param)
    res= curs.fetchone()
    return res


def checkadmin(username, con):
    curs = con.cursor()
    param = list()
    param.append(username)
    curs.execute("SELECT * FROM users WHERE username=?", param)
    return curs.fetchone()[5]


def chck(user, pasw, con):
    curs = con.cursor()
    param = list()
    param.append(user)
    curs.execute('SELECT * FROM users WHERE username=?;', param)
    res = curs.fetchone()
    passcheck = res[1]
    saltchck = res[2]
    pasw = hashing(pasw, saltchck)[0]
    if passcheck == pasw:
        return True
    else:
        return False


def changepasw(usr, pasw, con):
    params = list()
    salt = uuid.uuid4().hex
    pasw = hashing(pasw, salt)
    params.append(pasw[0])
    params.append(pasw[1])
    params.append(usr)
    try:
        curs = con.cursor()
        curs.execute("UPDATE users SET pass=?, salt=? WHERE username=?", params)
        tkinter.messagebox.showinfo("Зміна", "Пароль змінено")
        con.commit()
    except Error:
        tkinter.messagebox.showerror("Помилка", "Помилка при змінені паролю")
