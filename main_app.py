import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from datetime import datetime
from PIL import Image, ImageTk
from utils import load_user_config, save_user_config, load_users, save_users
import os
import sys
from lop import LopFrame
from sinhvien import SinhVienFrame
from giaovien import GiaoVienFrame
from khoa import KhoaFrame
from monhoc import MonHocFrame
from diem import DiemFrame
from phanquyen import PhanQuyenFrame
import ctypes

myappid = 'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

DEFAULT_IMAGE_PATH = "user_img.png"

class MainAppWindow:
    def __init__(self, root, role):
        self.master = root
        self.root = root
        self.role = role
        self.config = load_user_config()
        self.frames = {}
        self.build_ui()

    def build_ui(self):
        self.root.title("Ứng dụng quản lý sinh viên")
        self.center_window(1250, 700)
        self.root.resizable(True, True)
        self.root.iconbitmap("app_icon.ico")
        
        title = tk.Label(self.root, text="QUẢN LÝ SINH VIÊN", height=2, bg="#1E90FF", fg="white", font=("Arial", 22, "bold"))
        title.pack(side='top', fill='x')

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white")
        style.configure("Treeview.Heading", background="#1E90FF", foreground="white", font=('Arial', 12, 'bold'))
       
        self.menu_frame = tk.Frame(self.root, bg='#87CEFA', width=220, highlightthickness=3, highlightbackground='#00BFFF')
        self.menu_frame.pack(side='left', fill='y')

        username = self.config.get("username", "Người dùng")
        tk.Label(self.menu_frame, text=f"Người dùng: {username}", bg='#87CEFA', fg='red', font=('Arial', 10)).pack(pady=5)
        tk.Label(self.menu_frame, text="Hôm nay: " + datetime.now().strftime("%d-%m-%Y"), bg='#87CEFA', fg='red', font=('Arial', 10)).pack()
        tk.Label(self.menu_frame, text="MENU", font=('Arial', 16, 'bold'), bg='#87CEFA').pack(pady=(20,10))

        button_style = {"font": ("Arial", 12, "bold"), "bg": "#1E90FF", "fg": "white", "width": 14, "height": 2}

        self.main_frame = tk.Frame(self.root, bg='#F0F8FF')
        self.main_frame.pack(side='left', fill='both', expand=True, padx=2, pady=2)

        for name in ['home', 'sinhvien', 'giaovien', 'lop', 'khoa', 'monhoc', 'diem', 'phanquyen']:
            if name == 'lop':
                frame = LopFrame(self.main_frame, self.role)
            elif name == 'sinhvien':
                frame = SinhVienFrame(self.main_frame, self.role)
            elif name == 'giaovien':
                frame = GiaoVienFrame(self.main_frame, self.role)
            elif name == 'khoa':
                frame = KhoaFrame(self.main_frame, self.role)
            elif name == 'monhoc':
                frame = MonHocFrame(self.main_frame, self.role)
            elif name == 'diem':
                frame = DiemFrame(self.main_frame, self.role)
            elif name == 'phanquyen':
                frame = PhanQuyenFrame(self.main_frame)
            else:
                frame = tk.Frame(self.main_frame, bg='#F0F8FF')

            self.frames[name] = frame

        nav_items = [
            ("Trang chủ", "home"),
            ("Sinh viên", "sinhvien"),
            ("Giáo viên", "giaovien"),
            ("Lớp", "lop"),
            ("Khoa", "khoa"),
            ("Môn học", "monhoc"),
            ("Điểm", "diem")
        ]

        if self.role == "admin":
            nav_items.append(("Phân quyền", "phanquyen"))

        for label, name in nav_items:
            tk.Button(self.menu_frame, text=label, command=lambda n=name: self.show_frame(n), **button_style).pack(pady=5)

        self.build_home_frame()
        self.show_frame("home")

    def center_window(self, win_width, win_height):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        center_x = int(screen_width / 2 - win_width / 2)
        center_y = int(screen_height / 2 - win_height / 2)
        self.root.geometry(f'{win_width}x{win_height}+{center_x}+{center_y}')

    def build_home_frame(self):
        home_frame = self.frames['home']
        home_inner = tk.Frame(home_frame, bg='#F0F8FF')
        home_inner.place(relx=0.5, rely=0.05, anchor='n')

        username = self.config.get("username", "Người dùng")
        tk.Label(home_inner, text=f"XIN CHÀO, {username.upper()} \U0001F44B", font=('Arial', 18, 'bold'), bg='#F0F8FF', fg='darkblue').pack(pady=(0, 5))
        tk.Label(home_inner, text="Vui lòng chọn chức năng từ menu bên trái", font=('Arial', 14), bg='#F0F8FF', fg='darkblue').pack(pady=(0, 15))

        self.img_label = tk.Label(home_inner, bg='#F0F8FF')
        self.img_label.pack(pady=10)

        image_path = self.config.get("image_path")
        if not image_path or not os.path.exists(image_path):
            image_path = DEFAULT_IMAGE_PATH
        self.update_picture(image_path)

        tk.Button(home_inner, text="Cập nhật ảnh", command=self.choose_new_picture,
                  font=('Arial', 12, 'bold'), bg="#1E90FF", fg="white",
                  activebackground="#0056b3", activeforeground="white",
                  relief="raised", bd=2, width=12, height=2).pack(padx=5)

        tk.Button(self.menu_frame, text="Đăng xuất", command=self.logout,
                  font=("Arial", 12, "bold"), bg="#dc3545", fg="white",
                  activebackground="#a71d2a", activeforeground="white",
                  relief="raised", bd=2, width=14, height=2).pack(pady=20)

    def update_picture(self, path):
        try:
            image = Image.open(path)
            image = image.resize((200, 200))
            photo = ImageTk.PhotoImage(image)
            self.img_label.configure(image=photo)
            self.img_label.image = photo
        except Exception as e:
            messagebox.showerror("Lỗi tải ảnh", str(e))
            
    def logout(self):
        self.config.pop("username", None)
        self.config.pop("role", None)
        self.config.pop("image_path", None)
        save_user_config(self.config)
        os.execl(sys.executable, sys.executable, *sys.argv)

    def choose_new_picture(self):
        path = filedialog.askopenfilename(title="Chọn ảnh", filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        if path:
            self.update_picture(path)
            self.config['image_path'] = path
            save_user_config(self.config)
            users = load_users()
            username = self.config.get("username")
            for user in users:
                if user.get("username") == username:
                    user["image_path"] = path
                    break
            save_users(users)

    def show_frame(self, name):
        for frame in self.frames.values():
            frame.place_forget()
        if name in self.frames:
            self.frames[name].place(relx=0, rely=0, relwidth=1, relheight=1)
