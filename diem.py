import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import re

class DiemFrame(tk.Frame):
    def __init__(self, master, role):
        super().__init__(master, bg='#F0F8FF')
        self.role = role
        
        tk.Frame(self, height=30, bg='#F0F8FF').pack()
        
        tk.Label(self, text="ĐIỂM", font=('Arial', 18, 'bold'), bg='#F0F8FF', fg='darkblue').pack(pady=(10, 10))

        search_frame = tk.Frame(self, bg='#F0F8FF')
        search_frame.pack(pady=(0, 5))

        tk.Label(search_frame, text="Tìm kiếm:", font=('Arial', 12), bg='#F0F8FF').pack(side='left', padx=(0, 5))
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, font=('Arial', 12), width=30).pack(side='left')
        tk.Button(search_frame, text="Tìm", font=('Arial', 11, 'bold'), bg='#1E90FF', fg='white', command=self.search_diem).pack(side='left', padx=5)

        self.cols = ("Mã SV", "Họ tên", "Môn học", "Điểm quá trình", "Điểm thi", "Số lần thi")
        self.tree = ttk.Treeview(self, columns=self.cols, show='headings')
        for col in self.cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130, anchor='center')
        self.tree.pack(pady=10)
        self.tree.bind('<<TreeviewSelect>>', self.tree_selection)
        
        form_frame_diem = tk.Frame(self, bg='#F0F8FF')
        form_frame_diem.pack(pady=5)
        self.fields_diem = {}

        vcmd_float = (self.register(lambda P: self.valid_float(P)), '%P')
        vcmd_int = (self.register(lambda P: self.valid_int(P)), '%P')

        tk.Label(form_frame_diem, text="Mã sinh viên", font=('Arial', 12), bg='#F0F8FF').grid(row=0, column=0, padx=5, pady=2, sticky='e')
        self.fields_diem["Mã SV"] = tk.Entry(form_frame_diem, font=('Arial', 12), width=20)
        self.fields_diem["Mã SV"].grid(row=0, column=1, padx=5, pady=2, sticky='w')

        tk.Label(form_frame_diem, text="Họ tên", font=('Arial', 12), bg='#F0F8FF').grid(row=0, column=2, padx=5, pady=2, sticky='e')
        self.fields_diem["Họ tên"] = tk.Entry(form_frame_diem, font=('Arial', 12), width=20)
        self.fields_diem["Họ tên"].grid(row=0, column=3, padx=5, pady=2, sticky='w')

        tk.Label(form_frame_diem, text="Môn học", font=('Arial', 12), bg='#F0F8FF').grid(row=1, column=0, padx=5, pady=2, sticky='e')
        self.fields_diem["Môn học"] = tk.Entry(form_frame_diem, font=('Arial', 12), width=20)
        self.fields_diem["Môn học"].grid(row=1, column=1, padx=5, pady=2, sticky='w')

        tk.Label(form_frame_diem, text="Điểm quá trình", font=('Arial', 12), bg='#F0F8FF').grid(row=1, column=2, padx=5, pady=2, sticky='e')
        self.fields_diem["Điểm quá trình"] = tk.Entry(form_frame_diem, font=('Arial', 12), width=20)
        self.fields_diem["Điểm quá trình"].grid(row=1, column=3, padx=5, pady=2, sticky='w')
        self.fields_diem["Điểm quá trình"].config(validate="key", validatecommand=vcmd_float)

        tk.Label(form_frame_diem, text="Điểm thi", font=('Arial', 12), bg='#F0F8FF').grid(row=2, column=0, padx=5, pady=2, sticky='e')
        self.fields_diem["Điểm thi"] = tk.Entry(form_frame_diem, font=('Arial', 12), width=20)
        self.fields_diem["Điểm thi"].grid(row=2, column=1, padx=5, pady=2, sticky='w')
        self.fields_diem["Điểm thi"].config(validate="key", validatecommand=vcmd_float)

        tk.Label(form_frame_diem, text="Số lần thi", font=('Arial', 12), bg='#F0F8FF').grid(row=2, column=2, padx=5, pady=2, sticky='e')
        self.fields_diem["Số lần thi"] = tk.Entry(form_frame_diem, font=('Arial', 12), width=20)
        self.fields_diem["Số lần thi"].grid(row=2, column=3, padx=5, pady=2, sticky='w')
        self.fields_diem["Số lần thi"].config(validate="key", validatecommand=vcmd_int)

        btn_frame_diem = tk.Frame(self, bg='#F0F8FF')
        btn_frame_diem.pack(pady=10)

        self.add_button = tk.Button(btn_frame_diem, text="Thêm", command=self.add_diem,
                               font=('Arial', 12, 'bold'),
                               bg="#28a745", fg="white",
                               activebackground="#1e7e34", activeforeground="white",
                               relief="raised", bd=2, width=12, height=2)
        self.add_button.grid(row=0, column=0, padx=5)

        self.update_button = tk.Button(btn_frame_diem, text="Cập nhật", command=self.update_diem,
                                  font=('Arial', 12, 'bold'),
                                  bg="#fd7e14", fg="white",
                                  activebackground="#d46b08", activeforeground="white",
                                  relief="raised", bd=2, width=12, height=2)
        self.update_button.grid(row=0, column=1, padx=5)

        self.delete_button = tk.Button(btn_frame_diem, text="Xóa", command=self.delete_diem,
                                       font=('Arial', 12, 'bold'),
                                       bg="#dc3545", fg="white",
                                       activebackground="#a71d2a", activeforeground="white",
                                       relief="raised", bd=2, width=12, height=2)
        self.delete_button.grid(row=0, column=2, padx=5)

        self.load_button = tk.Button(btn_frame_diem, text="Tải dữ liệu", command=self.load_diem,
                                     font=('Arial', 12, 'bold'),
                                     bg="#007bff", fg="white",
                                     activebackground="#0056b3", activeforeground="white",
                                     relief="raised", bd=2, width=12, height=2)
        self.load_button.grid(row=0, column=3, padx=5)

        self.export_button = tk.Button(btn_frame_diem, text="Xuất dữ liệu", command=self.export_diem,
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

    def valid_float(self, val):
        if val == "":
            return True
        return bool(re.match(r'^(\d+(\.\d*)?|\.\d+)$', val))

    def valid_int(self, val):
        return val == "" or val.isdigit()
    
    def search_diem(self):
        query = self.search_var.get().lower()
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            if any(query in str(value).lower() for value in values):
                self.tree.selection_set(item)
                self.tree.see(item)
                break
        else:
            messagebox.showinfo("Không tìm thấy", "Không có mục điểm nào khớp với từ khóa.")

    def tree_selection(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], 'values')
            for i, field in enumerate(self.fields_diem):
                self.fields_diem[field].delete(0, 'end')
                self.fields_diem[field].insert(0, values[i])
                
    def add_diem(self):
        values = [self.fields_diem[field].get().strip() for field in self.fields_diem]
        if not all(values):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin.")
            return

        for item in self.tree.get_children():
            existing = self.tree.item(item, 'values')
            if values[0] == existing[0] and values[2] == existing[2] and values[5] == existing[5]:
                messagebox.showwarning("Trùng dữ liệu", "Đã tồn tại điểm cho sinh viên này.")
                return

        self.tree.insert('', 'end', values=values)
        
        for field in self.fields_diem.keys():
            self.fields_diem[field].delete(0, 'end')
            
    def update_diem(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Chưa chọn", "Vui lòng chọn một dòng để cập nhật.")
            return

        values = [self.fields_diem[field].get().strip() for field in self.fields_diem]

        if not all(values):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin.")
            return

        current = selected[0]

        for item in self.tree.get_children():
            existing = self.tree.item(item, 'values')
            if item != current and values[0] == existing[0] and values[2] == existing[2] and values[5] == existing[5]:
                messagebox.showwarning("Trùng dữ liệu", "Đã tồn tại điểm cho sinh viên này.")
                return

        self.tree.item(current, values=values)
        for field in self.fields_diem.keys():
            self.fields_diem[field].delete(0, 'end')

    def delete_diem(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Chưa chọn", "Vui lòng chọn một dòng để xóa.")
            return

        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa điểm này?"):
            for item in selected:
                self.tree.delete(item)

    def load_diem(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tree.delete(*self.tree.get_children())
                    for item in data:
                        self.tree.insert('', 'end', values=(
                            item.get("masv", ""),
                            item.get("hoten", ""),
                            item.get("monhoc", ""),
                            item.get("diemqt", ""),
                            item.get("diemthi", ""),
                            item.get("lanthi", "")
                        ))
            except Exception as e:
                messagebox.showerror("Lỗi tải dữ liệu", str(e))

    def export_diem(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if path:
            try:
                data = []
                for item in self.tree.get_children():
                    values = self.tree.item(item, 'values')
                    data.append({
                        "masv": values[0],
                        "hoten": values[1],
                        "monhoc": values[2],
                        "diemqt": values[3],
                        "diemthi": values[4],
                        "lanthi": values[5]
                    })
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                messagebox.showinfo("Thành công", "Dữ liệu điểm đã được xuất thành công.")
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

