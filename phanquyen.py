import tkinter as tk
from tkinter import ttk, messagebox
import json

class PhanQuyenFrame(tk.Frame):
    def __init__(self, container, users_file="users.json"):
        super().__init__(container, bg='#F0F8FF')
        self.users_file = users_file
        self.selected_user = tk.StringVar()
        self.selected_role = tk.StringVar()

        self.load_users()
        self.build_ui()

    def load_users(self):
        try:
            with open(self.users_file, "r", encoding="utf-8") as f:
                self.users = json.load(f)
        except:
            self.users = []
        self.usernames = [u["username"] for u in self.users]

    def build_ui(self):
        phanquyen_inner = tk.Frame(self, bg='#F0F8FF')
        phanquyen_inner.place(relx=0.5, rely=0.03, anchor='n')

        tk.Label(phanquyen_inner, text="PHÂN QUYỀN NGƯỜI DÙNG",
                 font=('Arial', 18, 'bold'), bg='#F0F8FF', fg='darkblue').pack(pady=(10, 20))

        tk.Label(phanquyen_inner, text="Chọn người dùng:", font=('Arial', 12), bg='#F0F8FF').pack(anchor='w', padx=10)
        user_menu = ttk.Combobox(phanquyen_inner, textvariable=self.selected_user, values=self.usernames, width=30)
        user_menu.pack(pady=5, padx=10)

        tk.Label(phanquyen_inner, text="Chọn vai trò:", font=('Arial', 12), bg='#F0F8FF').pack(anchor='w', padx=10)
        role_menu = ttk.Combobox(phanquyen_inner, textvariable=self.selected_role, values=["admin", "user"], width=30)
        role_menu.pack(pady=5, padx=10)

        btn_apply = tk.Button(phanquyen_inner, text="Áp dụng", font=('Arial', 12, 'bold'), bg='#1E90FF', fg='white',
                              activebackground='#104E8B', activeforeground='white', command=self.apply_role_change)
        btn_apply.pack(pady=15, ipadx=10, ipady=5)

    def apply_role_change(self):
        user = self.selected_user.get()
        role = self.selected_role.get()
        updated = False
        for u in self.users:
            if u["username"] == user:
                u["role"] = role
                updated = True
                break
        if updated:
            try:
                with open(self.users_file, "w", encoding="utf-8") as f:
                    json.dump(self.users, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Thành công", f"Đã cập nhật quyền của {user} thành {role}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu thay đổi: {e}")
        else:
            messagebox.showerror("Lỗi", "Người dùng không tồn tại")
