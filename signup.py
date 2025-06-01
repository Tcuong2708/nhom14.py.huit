import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
from utils import save_users
import ctypes

myappid = 'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
class SignupWindow:
    def __init__(self, root, login_windows):
        self.master = root
        self.signup_root = tk.Toplevel(root)
        self.signup_root.title("Đăng ký tài khoản")
        self.signup_root.iconbitmap("app_icon.ico")
        
        self.center_window(1100, 700)
        self.signup_root.configure(bg="white")
        self.signup_root.resizable(False, False)

        self.login_windows = login_windows

        image = Image.open("login.png").resize((650, 600))
        self.bg_image = ImageTk.PhotoImage(image)
        label_img = tk.Label(self.signup_root, image=self.bg_image, bg="white")
        label_img.image = self.bg_image
        label_img.place(x=50, y=60)

        self.create_widgets()
        
    def center_window(self, win_width, win_height):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        center_x = int(screen_width / 2 - win_width / 2)
        center_y = int(screen_height / 2 - win_height / 2)
        self.signup_root.geometry(f'{win_width}x{win_height}+{center_x}+{center_y}')
        
    def create_widgets(self):
        tk.Label(self.signup_root, text="© Bản quyền thuộc nhóm 14", font=("Arial", 10, "bold"),
                 fg="#3498db", bg="white").place(x=800, y=600)

        tk.Label(self.signup_root, text="Đăng ký", font=("Arial", 24, "bold"),
                 fg="#3498db", bg="white").place(x=800, y=80)

        tk.Label(self.signup_root, text="Tên đăng nhập:", font=("Arial", 12), bg="white").place(x=800, y=160)
        self.entry_username = tk.Entry(self.signup_root, width=30, bd=2)
        self.entry_username.place(x=800, y=190)

        tk.Label(self.signup_root, text="Mật khẩu:", font=("Arial", 12), bg="white").place(x=800, y=230)
        self.entry_password = tk.Entry(self.signup_root, width=30, bd=2, show="*")
        self.entry_password.place(x=800, y=260)

        tk.Label(self.signup_root, text="Xác nhận mật khẩu:", font=("Arial", 12), bg="white").place(x=800, y=300)
        self.entry_confirm = tk.Entry(self.signup_root, width=30, bd=2, show="*")
        self.entry_confirm.place(x=800, y=330)

        tk.Button(self.signup_root, text="Đăng ký", font=("Arial", 12, 'bold'), width=18, bg="#3498db", fg="white", command=self.register_user).place(x=800, y=390)

        tk.Label(self.signup_root, text="Bạn đã có tài khoản?", bg="white").place(x=800, y=440)
        tk.Button(self.signup_root, text="Đăng nhập", fg="#3498db", bg="white", bd=0,
                  command=self.goto_login_window).place(x=930, y=440)

    def register_user(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        confirm_password = self.entry_confirm.get().strip()

        if not username or not password or not confirm_password:
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin.")
            return

        if password != confirm_password:
            messagebox.showerror("Lỗi", "Mật khẩu không khớp.")
            return

        try:
            with open("users.json", "r", encoding="utf-8") as f:
                users = json.load(f)
        except FileNotFoundError:
            users = []

        if any(user["username"] == username for user in users):
            messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại.")
            return

        users.append({
            "username": username,
            "password": password,
            "role": "user"
        })

        save_users(users)

        messagebox.showinfo("Thành công", "Đăng ký thành công!")
        self.signup_root.destroy()
        self.login_windows()

    def goto_login_window(self):
        self.signup_root.destroy()
        self.master.after(100, self.login_windows)
