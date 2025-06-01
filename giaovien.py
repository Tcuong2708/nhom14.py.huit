import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json

class GiaoVienFrame(tk.Frame):
    def __init__(self, master, role):
        super().__init__(master, bg='#F0F8FF')
        self.role = role

        tk.Frame(self, height=30, bg='#F0F8FF').pack()
        
        tk.Label(self, text="GIẢNG VIÊN", font=('Arial', 18, 'bold'), bg='#F0F8FF', fg='darkblue').pack(pady=(10, 10))

        search_frame = tk.Frame(self, bg='#F0F8FF')
        search_frame.pack(pady=(0, 5))

        tk.Label(search_frame, text="Tìm kiếm:", font=('Arial', 12), bg='#F0F8FF').pack(side='left', padx=(0, 5))
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, font=('Arial', 12), width=30).pack(side='left')
        tk.Button(search_frame, text="Tìm", font=('Arial', 11, 'bold'), bg='#1E90FF', fg='white', command=self.search_giaovien).pack(side='left', padx=5)

        self.cols = ("Mã GV", "Họ tên", "Số ĐT", "Trình độ", "Chủ nhiệm", "Khoa")
        self.tree = ttk.Treeview(self, columns=self.cols, show='headings')
        for col in self.cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor='center')
        self.tree.pack(pady=10)
        self.tree.bind('<<TreeviewSelect>>', self.tree_selection)
        
        form_frame_gv = tk.Frame(self, bg='#F0F8FF')
        form_frame_gv.pack(pady=(0, 5))

        self.fields_gv = {}

        tk.Label(form_frame_gv, text="Mã giảng viên", font=('Arial', 12), bg='#F0F8FF').grid(row=0, column=0, padx=5, pady=2, sticky='e')
        self.fields_gv["Mã GV"] = tk.Entry(form_frame_gv, font=('Arial', 12), width=20)
        self.fields_gv["Mã GV"].grid(row=0, column=1, padx=10, pady=2, sticky='w')

        tk.Label(form_frame_gv, text="Họ tên", font=('Arial', 12), bg='#F0F8FF').grid(row=0, column=2, padx=5, pady=2, sticky='e')
        self.fields_gv["Họ tên"] = tk.Entry(form_frame_gv, font=('Arial', 12), width=20)
        self.fields_gv["Họ tên"].grid(row=0, column=3, padx=10, pady=2, sticky='w')

        tk.Label(form_frame_gv, text="Số điện thoại", font=('Arial', 12), bg='#F0F8FF').grid(row=1, column=0, padx=5, pady=2, sticky='e')
        self.fields_gv["Số ĐT"] = tk.Entry(form_frame_gv, font=('Arial', 12), width=20)
        self.fields_gv["Số ĐT"].grid(row=1, column=1, padx=10, pady=2, sticky='w')

        tk.Label(form_frame_gv, text="Trình độ", font=('Arial', 12), bg='#F0F8FF').grid(row=1, column=2, padx=5, pady=2, sticky='e')
        self.fields_gv["Trình độ"] = ttk.Combobox(form_frame_gv, font=('Arial', 12), width=18, state="readonly")
        self.fields_gv["Trình độ"]['values'] = ("Cử nhân", "Thạc sĩ", "Tiến sĩ", "Phó Giáo sư", "Giáo sư")
        self.fields_gv["Trình độ"].current(0)
        self.fields_gv["Trình độ"].grid(row=1, column=3, padx=10, pady=2, sticky='w')

        tk.Label(form_frame_gv, text="Lớp chủ nhiệm", font=('Arial', 12), bg='#F0F8FF').grid(row=2, column=0, padx=5, pady=2, sticky='e')
        self.fields_gv["Chủ nhiệm"] = tk.Entry(form_frame_gv, font=('Arial', 12), width=20)
        self.fields_gv["Chủ nhiệm"].grid(row=2, column=1, padx=10, pady=2, sticky='w')

        tk.Label(form_frame_gv, text="Khoa", font=('Arial', 12), bg='#F0F8FF').grid(row=2, column=2, padx=5, pady=2, sticky='e')
        self.fields_gv["Khoa"] = tk.Entry(form_frame_gv, font=('Arial', 12), width=20)
        self.fields_gv["Khoa"].grid(row=2, column=3, padx=10, pady=2, sticky='w')

        btn_frame_gv = tk.Frame(self, bg='#F0F8FF')
        btn_frame_gv.pack(pady=10)

        self.add_button = tk.Button(btn_frame_gv, text="Thêm", command=self.add_giaovien,
                                    font=('Arial', 12, 'bold'),
                                    bg="#28a745", fg="white",
                                    activebackground="#1e7e34", activeforeground="white",
                                    relief="raised", bd=2, width=12, height=2)
        self.add_button.grid(row=0, column=0, padx=5)

        self.update_button = tk.Button(btn_frame_gv, text="Cập nhật", command=self.update_giaovien,
                                       font=('Arial', 12, 'bold'),
                                       bg="#fd7e14", fg="white",
                                       activebackground="#d46b08", activeforeground="white",
                                       relief="raised", bd=2, width=12, height=2)
        self.update_button.grid(row=0, column=1, padx=5)

        self.delete_button = tk.Button(btn_frame_gv, text="Xóa", command=self.delete_giaovien,
                                       font=('Arial', 12, 'bold'),
                                       bg="#dc3545", fg="white",
                                       activebackground="#a71d2a", activeforeground="white",
                                       relief="raised", bd=2, width=12, height=2)
        self.delete_button.grid(row=0, column=2, padx=5)

        self.load_button = tk.Button(btn_frame_gv, text="Tải dữ liệu", command=self.load_giaovien,
                                     font=('Arial', 12, 'bold'),
                                     bg="#007bff", fg="white",
                                     activebackground="#0056b3", activeforeground="white",
                                     relief="raised", bd=2, width=12, height=2)
        self.load_button.grid(row=0, column=3, padx=5)

        self.export_button = tk.Button(btn_frame_gv, text="Xuất dữ liệu", command=self.export_giaovien,
                                       font=('Arial', 12, 'bold'),
                                       bg="#17a2b8", fg="white",
                                       activebackground="#117a8b", activeforeground="white",
                                       relief="raised", bd=2, width=12, height=2)
        self.export_button.grid(row=0, column=4, padx=5)

        if self.role != 'admin':
            self.disable_admin_buttons()
            
    def disable_admin_buttons(self):
        self.add_button["state"] = "disabled"
        self.update_button["state"] = "disabled"
        self.delete_button["state"] = "disabled"
        self.load_button["state"] = "disabled"
        self.export_button["state"] = "disabled"
        
    def search_giaovien(self):
        query = self.search_var.get().lower()
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            if any(query in str(v).lower() for v in values):
                self.tree.selection_set(item)
                self.tree.see(item)
                return
        messagebox.showinfo("Không tìm thấy", "Không có giảng viên nào khớp với từ khóa.")

    def tree_selection(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], 'values')
            for i, field in enumerate(self.cols):
                widget = self.fields_gv[field]
                if isinstance(widget, ttk.Combobox):
                    widget.set(values[i])
                else:
                    widget.delete(0, 'end')
                    widget.insert(0, values[i])
                
    def add_giaovien(self):
        values = [self.fields_gv[field].get().strip() for field in self.fields_gv]

        if not all(values):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin.")
            return

        new_magv = values[0]

        for item in self.tree.get_children():
            if self.tree.item(item, 'values')[0] == new_magv:
                messagebox.showwarning("Trùng mã", f"Mã giảng viên '{new_magv}' đã tồn tại.")
                return

        self.tree.insert('', 'end', values=values)

        for field in self.fields_gv.keys():
            if field not in ["Trình độ"]:
                self.fields_gv[field].delete(0, 'end')
                
    def update_giaovien(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Chưa chọn", "Vui lòng chọn một dòng để cập nhật.")
            return

        values = [self.fields_gv[field].get().strip() for field in self.fields_gv]

        if not all(values):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin.")
            return

        new_magv = values[0]
        current_item = selected[0]

        for item in self.tree.get_children():
            if item != current_item and self.tree.item(item, 'values')[0] == new_magv:
                messagebox.showwarning("Trùng mã", f"Mã giảng viên '{new_magv}' đã tồn tại.")
                return

        self.tree.item(current_item, values=values)

        for field in self.fields_gv.keys():
            if field not in ["Trình độ"]:
                self.fields_gv[field].delete(0, 'end')

    def delete_giaovien(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Chưa chọn", "Vui lòng chọn một dòng để xóa.")
            return

        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa giảng viên này?"):
            for item in selected:
                self.tree.delete(item)

    def load_giaovien(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.tree.delete(*self.tree.get_children())
                for item in data:
                    self.tree.insert('', 'end', values=(
                        item.get("magv", ""),
                        item.get("hoten", ""),
                        item.get("sodt", ""),
                        item.get("trinhdo", ""),
                        item.get("chunhiem", ""),
                        item.get("khoa", "")
                    ))
                messagebox.showinfo("Thành công", "Đã tải dữ liệu giảng viên thành công!")
            except Exception as e:
                messagebox.showerror("Lỗi tải dữ liệu", str(e))

    def export_giaovien(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if path:
            try:
                data = []
                for item in self.tree.get_children():
                    values = self.tree.item(item, 'values')
                    data.append({
                        "magv": values[0],
                        "hoten": values[1],
                        "sodt": values[2],
                        "trinhdo": values[3],
                        "chunhiem": values[4],
                        "khoa": values[5]
                    })
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                messagebox.showinfo("Thành công", "Dữ liệu đã được xuất thành công.")
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
