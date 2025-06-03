import tkinter as tk
from main_app import MainAppWindow
from utils import load_user_config, clear_user_config
from login import LoginWindow
from signup import SignupWindow
import os
import sys
import ctypes

myappid = 'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

root = None

def restart_app():
    os.execl(sys.executable, sys.executable, *sys.argv)

def run_main_app(role):
    global root
    if root is not None:
        root.destroy()
    main_root = tk.Tk()
    MainAppWindow(main_root, role)
    main_root.mainloop()
    root.destroy()

def show_signup_window():
    signup = SignupWindow(root, lambda: LoginWindow(root, run_main_app, show_signup_window))
    signup.signup_root.lift()
    signup.signup_root.focus_force()

if __name__ == "__main__":
    #config = load_user_config()
    #if config.get("username") and config.get("role"):
        #tk.Tk().withdraw()
        #run_main_app(config["role"])
    #else:
        root = tk.Tk()
        root.withdraw()
        clear_user_config()
        LoginWindow(root, run_main_app, show_signup_window)
        root.mainloop()
