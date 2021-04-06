    # -*- coding: utf-8 -*-
from database import *
import tkinter as tk
from tkinter import messagebox
import os
import winreg
import win32api as wa
root = tk.Tk()
root.title('Розмежування доступу')
root.geometry("500x400+325+0")
con = sql_connection(root)
sql_table(root, con)
createRoot(root, con)


def exitt():
    answ = messagebox.askokcancel("Вихід", "Вийти з програми?")
    if answ:
        root.destroy()


def about():
    messagebox.showinfo("Автор", "Шмалій Горигорій Григорович\nГрупа ФБ-81\nВаріант 21")


def exercise():
    messagebox.showinfo("Завдання", "Варіант 21\nНаявність латинських букв, символів кирилиці, цифр і знаків "
                                    "арифметичних операцій")


def instructions():
    messagebox.showinfo("Інструкція", "Поки якийсь текст")


def checkreqular(pasw):
    import re
    lat = r"[A-Za-z]"
    kyr = r"[А-Яа-яЁёІі]"
    num = r"[0-9]"
    math = r"[\+\=\-\*]"
    a = re.search(lat, pasw)
    b = re.search(kyr, pasw)
    c = re.search(num, pasw)
    d = re.search(math, pasw)
    if not a or not b or not c or not d:
        tkinter.messagebox.showerror("Помилка", "Пароль не відповідає вимогам")
        return False
    return True


def logout():
    global Userr, Enter
    if 'Userr' in globals():
        Userr.hideall()
        Enter.enter()
        del Userr


class Person:
    username = ""
    password = ""
    blocked = 0
    passrstr = 0
    admin = 0
    label = ''
    changepsw = ''
    oldpswlbl = tk.Label(text="Current pass")
    newpswlbl = tk.Label(text="New password")
    reppswlbl = tk.Label(text="Repeat new password")
    oldpsw = tk.Entry(show='*')
    newpsw = tk.Entry(show="*")
    repnewpsw = tk.Entry(show="*")
    change = tk.Button(text="OK")
    cancel = tk.Button(text="CANCEL")
    img = tk.PhotoImage(file='eye.png')
    showbtn = tk.Button(text='', image=img)

    def __init__(self):
        self.changepsw = tk.Button(text="Змінити пароль", activebackground='#FF0000')

    def showpass(self):
        if self.newpsw.cget("show") == "*":
            self.newpsw.config(show="")
            self.repnewpsw.config(show="")
        else:
            self.newpsw.config(show="*")
            self.repnewpsw.config(show="*")

    def changepass(self):
        self.clear()
        if self.blocked == 0:
            self.showbtn.place(y=150.5, x=361, height=24)
            self.showbtn.config(command=self.showpass)
            self.oldpswlbl.place(x=160, y=80)
            self.oldpsw.place(width=200, height=25, x=160, y=100)
            self.newpswlbl.place(x=160, y=130)
            self.newpsw.place(width=200, height=25, x=160, y=150)
            self.reppswlbl.place(x=160, y=180)
            self.repnewpsw.place(width=200, height=25, x=160, y=200)
            self.change.config(command=self.acceptchpsw)
            self.change.place(width=80, height=30, x=160, y=230)
            self.cancel.config(command=self.cancelchpsw)
            self.cancel.place(width=80, height=30, x=280, y=230)
        else:
            tk.messagebox.showerror("Помилка", "Даний обліковий запис заблокований адміністратором")

    def clear(self):
        pass

    def cancelchpsw(self):
        self.newpsw.config(show="*")
        self.repnewpsw.config(show="*")
        self.oldpsw.delete(0, 'end')
        self.oldpsw.place_forget()
        self.newpsw.delete(0, 'end')
        self.newpsw.place_forget()
        self.repnewpsw.delete(0, 'end')
        self.repnewpsw.place_forget()
        self.change.place_forget()
        self.cancel.place_forget()
        self.oldpswlbl.place_forget()
        self.newpswlbl.place_forget()
        self.reppswlbl.place_forget()
        self.showbtn.place_forget()

    def acceptchpsw(self):
        oldpasw = self.oldpsw.get()
        new = self.newpsw.get()
        rep = self.repnewpsw.get()
        if not chck(self.username, oldpasw, con):
            tkinter.messagebox.showerror("Помилка", "Ви ввели неправильний пароль!")
        elif new == '':
            tkinter.messagebox.showerror("Помилка", "Пароль не може бути пустим")
        elif new != rep:
            tkinter.messagebox.showerror("Помилка", "Паролі не співпадають!")
        elif not self.passrstr or (self.passrstr and checkreqular(new)):
            changepasw(self.username, new, con)
            self.cancelchpsw()


class Admin(Person):
    addlbl = ""
    adduserbtn = ""
    adduok = ""
    adducnc = ""
    addEntry = ""
    usersbtn = ""
    users = ""
    usersLbl = ''
    usersnames = ""
    chckblocked = ""
    chckrestr = ""
    check1 = tk.IntVar()
    check2 = tk.IntVar()
    next = ""
    prev = ""
    cnlusrs = ""

    def __init__(self, usrname, pasw):
        super().__init__()
        self.username = usrname
        self.password = pasw
        parse = parseinform(usrname, con)
        self.blocked = parse[3]
        self.passrstr = parse[4]
        self.admin = parse[5]
        self.addlbl = tk.Label(text="Enter new name")
        self.adduserbtn = tk.Button(text="Add new user")
        self.adduok = tk.Button(text="Ok")
        self.adducnc = tk.Button(text="Cancel", activebackground='#FF0000')
        self.addEntry = tk.Entry(show="")
        self.usersbtn = tk.Button(text="Show users")
        self.usersLbl = tk.Label(text="NAME: ", bg="white", font="Arial 12")
        self.usersnames = tk.Label(bg="white", font="Arial 11")
        self.chckblocked = tk.Checkbutton(text="Blocked", variable=self.check1, onvalue=1, offvalue=0,
                                          command=self.Changeusr)
        self.passrestr = tk.Checkbutton(text="Restriction", variable=self.check2, onvalue=1, offvalue=0,
                                        command=self.Changeusr)

    def showall(self):
        text = "Hi, {0}".format(self.username)
        self.label = tk.Label(text=text, font="Arial 12", bg="white")
        self.label.place(x=1)
        self.changepsw.place(width=150, height=30, relx=0.002, rely=0.2)
        self.changepsw.config(command=self.changepass)
        self.adduserbtn.place(width=150, height=30, relx=0.002, rely=0.3)
        self.adduserbtn.config(command=self.showadding)
        self.usersbtn.place(width=150, height=30, relx=0.002, rely=0.4)
        self.usersbtn.config(command=self.showusers)
        self.adduok.config(command=self.okadding)
        self.adducnc.config(command=self.hideadding)
        self.next = tk.Button(text="next>", command=self.Next)
        self.prev = tk.Button(text="<prev", command=self.Prev)
        self.cnlusrs = tk.Button(text="Cancel", command=self.hideusers)

    def Next(self):
        global num, res
        if num < len(res)-1:
            num+=1
            self.USER()

    def Prev(self):
        global num, res
        if num > 0:
            num -= 1
            self.USER()

    def USER(self):
        global num, res
        self.usersnames.config(text="")
        self.usersnames.config(text=res[num][0])
        self.check1.set(res[num][1])
        self.check2.set(res[num][2])

    def showusers(self):
        global num, res
        num = 0
        self.clear()
        res = parseusers(con)
        if res is not None:
            self.usersLbl.place(width=65, x=160, y=60)
            self.usersnames.place(x=230, y=60)
            self.chckblocked.place(x=160, y=100)
            self.passrestr.place(x=160, y=130)
            self.prev.place(width=60, x=160, y=160)
            self.next.place(width=60, x=280, y=160)
            self.cnlusrs.place(width=60, x=220, y=190)
            self.USER()
        else:
            self.clear()

    def Changeusr(self):
        global res
        changesusrinfo(res[num][0], self.check1.get(), self.check2.get(), con)
        res.clear()
        res = parseusers(con)

    def hideusers(self):
        self.usersLbl.place_forget()
        self.usersnames.place_forget()
        self.chckblocked.place_forget()
        self.passrestr.place_forget()
        self.next.place_forget()
        self.prev.place_forget()
        self.cnlusrs.place_forget()

    def showadding(self):
        self.clear()
        self.addEntry.place(width=200, height=25, x=160, y=100)
        self.adduok.place(width=80, height=30, x=160, y=130)
        self.adducnc.place(width=80, height=30, x=280, y=130)
        self.addlbl.place(x=160, y=80)

    def okadding(self):
        name = self.addEntry.get()
        pasw = " "
        if name == '' or name == " ":
            tk.messagebox.showerror("Помилка", "Ім'я не може бути пустим!")
        elif adduser(name, pasw, con):
            self.hideadding()

    def hideadding(self):
        self.addEntry.delete(0, 'end')
        self.addEntry.place_forget()
        self.adduok.place_forget()
        self.adducnc.place_forget()
        self.addlbl.place_forget()

    def hideall(self):
        self.clear()
        self.label.destroy()
        self.changepsw.destroy()
        self.adduserbtn.destroy()
        self.usersbtn.destroy()

    def clear(self):
        self.hideusers()
        self.hideadding()
        self.cancelchpsw()


class User(Person):
    def __init__(self, usrname, pasw):
        super().__init__()
        self.username= usrname
        self.password = pasw
        parse = parseinform(usrname, con)
        self.blocked= parse[3]
        self.passrstr = parse[4]
        self.admin = parse[5]

    def showall(self):
        text = "Hi, {0}".format(self.username)
        self.label= tk.Label(text=text, font="Arial 12", bg= "white")
        self.label.place(x=1)
        self.changepsw.place(width=150, height=30, relx = 0.002, rely=0.08)
        self.changepsw.config(command = self.changepass)
        if self.passrstr:
            a=""
            if not checkreqular(self.password):
                a = tkinter.messagebox.askokcancel("Увага","Бажаєте змінити пароль?")
            if a:
                self.changepass()

    def hideall(self):
        self.cancelchpsw()
        self.label.destroy()
        self.changepsw.destroy()


class EnterWindow:
    userenter = tk.Entry(root)
    passenter = tk.Entry(root)
    name = tk.Label(text= "Username", font="Arial 12")
    pasw = tk.Label(text= "Password", font= "Arial 12")
    enterbtn = tk.Button(text="Вхід", activebackground='#FF0000')
    img = tk.PhotoImage(file='eye.png') if os.path.isfile("eye.png") else " "
    showbtn = tk.Button(text='', image=img)
    n=3

    def showpsw(self):
        if self.passenter.cget("show") == "*":
            self.passenter.config(show="")
        else:
            self.passenter.config(show="*")

    def hide(self):
        self.passenter.config(show="*")
        self.userenter.place_forget()
        self.name.place_forget()
        self.pasw.place_forget()
        self.passenter.place_forget()
        self.enterbtn.place_forget()
        self.showbtn.place_forget()

    def connect(self):
        name = self.userenter.get()
        pasw = self.passenter.get()
        if checkpass(name, pasw, con):
            self.userenter.delete(0, 'end')
            self.passenter.delete(0, 'end')
            self.hide()
            global Userr
            if not checkadmin(name, con):
                Userr = User(name, pasw)
            else:
                Userr = Admin(name, pasw)
            Userr.showall()
        else:
            self.n -= 1
            if self.n == 0:
                root.destroy()
        return None

    def enter(self):
        self.n = 3
        self.userenter.place(width=200, height=25, x=150, y=100)
        self.name.place(x=150, y=75)
        self.pasw.place(x=150, y=125)
        self.passenter.place(width=200, height=25, x=150, y=150)
        self.enterbtn.place(width=100, x=200, y=180)
        self.passenter.config(show="*")
        self.showbtn.place(y=150.5, x=350, height=24)
        self.showbtn.config(command=self.showpsw)
        self.enterbtn.config(command=self.connect)


def ReadRegister():
    REG_NAME = "Shmalii"
    name = "Hash_code"
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_NAME, 0,
                                      winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(registry_key, name)
        winreg.CloseKey(registry_key)
        return value
    except WindowsError:
        return None


def SysInformation():
    user = "User: "+wa.GetUserName()
    comp_name = "Computer Name: " + wa.GetComputerName()
    win_dir = "Windows directory: " + wa.GetWindowsDirectory()
    sys_dir = "System directory: " + wa.GetSystemDirectory()
    mouse_btns = "Amount of mouse buttons: " + str(wa.GetSystemMetrics(43))
    screen_height = "Height: " + str(wa.GetSystemMetrics(1))
    drivers = "Drivers: " + wa.GetLogicalDriveStrings()
    allinfo = " ".join([user, comp_name, win_dir, sys_dir, mouse_btns, screen_height, drivers])
    allinfo = hashlib.sha512(allinfo.encode())
    return allinfo.hexdigest()


def main():
    global Enter
    if SysInformation() != ReadRegister():
        tk.messagebox.showerror("Error", "Program launch error!")
        root.destroy()
        return None

    mainmenu = tk.Menu(root)
    root.config(menu=mainmenu)
    helpmenu = tk.Menu(mainmenu, tearoff=0)
    helpmenu.add_command(label="Інструкція", command=instructions)
    helpmenu.add_separator()
    helpmenu.add_command(label="Про автора", command=about)
    helpmenu.add_separator()
    helpmenu.add_command(label="Завдання", command=exercise)
    mainmenu.add_cascade(label="Довідка", menu=helpmenu)
    exitmenu = tk.Menu(mainmenu, tearoff=0)
    exitmenu.add_command(label="Log out", command=logout)
    exitmenu.add_separator()
    exitmenu.add_command(label="З програми", command=exitt)
    mainmenu.add_cascade(label="Вихід", menu=exitmenu)
    Enter = EnterWindow()
    Enter.enter()
    root.mainloop()


if __name__ == "__main__":
    main()
