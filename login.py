import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from utils import load_users, save_user_config

class LoginWindow:
    def __init__(self, root, on_success, open_signup_callback):
        self.master = root
        self.on_success = on_success
        self.open_signup_callback = open_signup_callback

        self.window = tk.Toplevel(root)
        self.window.title("Đăng nhập hệ thống")
        self.window.iconbitmap("app_icon.ico")
        self.center_window(1100, 700)
        self.window.configure(bg="white")
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.master.destroy)

        image = Image.open("login.png").resize((650, 600))
        self.bg_image = ImageTk.PhotoImage(image)
        tk.Label(self.window, image=self.bg_image, bg="white").place(x=50, y=60)

        tk.Label(self.window, text="© Bản quyền thuộc nhóm 14", font=("Arial", 10, "bold"),
                 fg="#3498db", bg="white").place(x=800, y=600)

        tk.Label(self.window, text="Đăng nhập", font=("Arial", 24, "bold"),
                 fg="#3498db", bg="white").place(x=800, y=80)

        tk.Label(self.window, text="Tên đăng nhập:", font=("Arial", 12), bg="white").place(x=800, y=160)
        self.entry_username = tk.Entry(self.window, width=30, bd=2)
        self.entry_username.place(x=800, y=190)

        tk.Label(self.window, text="Mật khẩu:", font=("Arial", 12), bg="white").place(x=800, y=230)
        self.entry_password = tk.Entry(self.window, width=30, bd=2, show="*")
        self.entry_password.place(x=800, y=260)

        tk.Button(self.window, text="Đăng nhập", font=("Arial", 12, 'bold'), width=18, bg="#3498db", fg="white",
                  command=self.do_login).place(x=800, y=310)

        tk.Label(self.window, text="Chưa có tài khoản?", bg="white").place(x=800, y=360)
        tk.Button(self.window, text="Đăng ký", fg="#3498db", bg="white", bd=0,
                  command=self.open_signup).place(x=940, y=360)

    def center_window(self, win_width, win_height):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        center_x = int(screen_width / 2 - win_width / 2)
        center_y = int(screen_height / 2 - win_height / 2)
        self.window.geometry(f'{win_width}x{win_height}+{center_x}+{center_y}')

    def do_login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        users = load_users()

        for user in users:
            if user["username"] == username and user["password"] == password:
                save_user_config({
                    "username": username,
                    "role": user["role"],
                    "image_path": user.get("image_path", "user_img.png")
                    })
                messagebox.showinfo("Thành công", "Đăng nhập thành công!")
                self.window.destroy()
                self.master.deiconify()
                self.on_success(user["role"])
                return
        messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu!")

    def open_signup(self):
        self.window.destroy()
        self.master.after(100, self.open_signup_callback)
