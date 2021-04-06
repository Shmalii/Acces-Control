import tkinter as tk
from tkinter import filedialog as fd, messagebox, ttk
import win32api as wa
import  hashlib
import base64
import  os
import  winreg
from binnary import *
# wa.GetUserName()
# wa.GetComputerName()
# wa.GetWindowsDirectory()
# wa.GetSystemDirectory()
# wa.GetSystemMetrics(43) кількість кнопок
# wa.GetSystemMetrics(1) висота екрану


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


def writeregister(inform):
    REG_NAME="Shmalii"
    name = "Hash_code"
    try:
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_NAME)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_NAME, 0,
                                      winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, inform)
        winreg.CloseKey(registry_key)
        return True
    except WindowsError:
        return False

def install_files(directory):
    file_exe=directory+'/'+filename
    img = directory+'/'+imagename
    answer = True
    if os.path.isfile(file_exe) or os.path.isfile(img):
        answer = messagebox.askokcancel("Error", "Files with this name already exist,replace the files?")
    if answer:
        try:
            exe = open(file_exe, 'wb')
            exe.write(base64.b64decode(exefile))
            exe.close()
            icon = open(img, 'wb')
            icon.write(base64.b64decode(image))
            icon.close()
            messagebox.showinfo("Instalation", "Files installed!")
        except Exception:
            messagebox.showerror("Error", "Error creating files!")
            if os.path.isfile(file_exe):
                os.remove(file_exe)
            if os.path.isfile(img):
                os.remove(img)


def ask_directory():
    if writeregister(SysInformation()):
        directory = fd.askdirectory()
        if directory!='':
            install_files(directory)
    else:
        messagebox.showerror("Error", "Error adding information to register!")


def main():
    root = tk.Tk()
    root.title("Installer")
    root.geometry("220x100+450+50")
    install = tk.Button(text="Install file", command=ask_directory, font="Arial 13", activebackground='#FF0000')
    install.place(relx=0.15, rely=0.3, width=150)
    root.mainloop()


if __name__ == "__main__":
    main()