import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkcalendar import DateEntry
import json

class SinhVienFrame(tk.Frame):
    def __init__(self, master, role):
        super().__init__(master, bg='#F0F8FF')
        self.role = role
        
        tk.Frame(self, height=30, bg='#F0F8FF').pack()

        tk.Label(self, text="SINH VIÊN", font=('Arial', 18, 'bold'), bg='#F0F8FF', fg='darkblue').pack(pady=10)

        search_frame = tk.Frame(self, bg='#F0F8FF')
        search_frame.pack(pady=5)

        tk.Label(search_frame, text="Tìm kiếm:", font=('Arial', 12), bg='#F0F8FF').pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, font=('Arial', 12), width=30).pack(side='left')
        tk.Button(search_frame, text="Tìm", font=('Arial', 11, 'bold'), bg='#1E90FF', fg='white', command=self.search_sinhvien).pack(side='left', padx=5)

        self.cols = ("Mã SV", "Họ tên", "Ngày sinh", "Địa chỉ", "Số ĐT", "Giới tính", "Lớp", "Hệ ĐT")
        self.tree = ttk.Treeview(self, columns=self.cols, show='headings')
        for col in self.cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor='center')
        self.tree.pack(pady=10)
        self.tree.bind('<<TreeviewSelect>>', self.tree_selection)
        
        form_frame_sv = tk.Frame(self, bg='#F0F8FF')
        form_frame_sv.pack(pady=5)
        
        self.fields_sv = {}

        tk.Label(form_frame_sv, text="Mã sinh viên", font=('Arial', 12), bg='#F0F8FF').grid(row=0, column=0, padx=5, pady=2, sticky='e')
        self.fields_sv["Mã SV"] = tk.Entry(form_frame_sv, font=('Arial', 12), width=20)
        self.fields_sv["Mã SV"].grid(row=0, column=1, padx=5, pady=2, sticky='w')

        tk.Label(form_frame_sv, text="Họ tên", font=('Arial', 12), bg='#F0F8FF').grid(row=0, column=2, padx=5, pady=2, sticky='e')
        self.fields_sv["Họ tên"] = tk.Entry(form_frame_sv, font=('Arial', 12), width=20)
        self.fields_sv["Họ tên"].grid(row=0, column=3, padx=5, pady=2, sticky='w')

        tk.Label(form_frame_sv, text="Lớp", font=('Arial', 12), bg='#F0F8FF').grid(row=1, column=0, padx=5, pady=2, sticky='e')
        self.fields_sv["Lớp"] = tk.Entry(form_frame_sv, font=('Arial', 12), width=20)
        self.fields_sv["Lớp"].grid(row=1, column=1, padx=5, pady=2, sticky='w')

        tk.Label(form_frame_sv, text="Hệ đào tạo", font=('Arial', 12), bg='#F0F8FF').grid(row=1, column=2, padx=5, pady=2, sticky='e')
        self.fields_sv["Hệ ĐT"] = ttk.Combobox(form_frame_sv, font=('Arial', 12), width=18, state="readonly")
        self.fields_sv["Hệ ĐT"]['values'] = ("Chính quy", "Không chính quy")
        self.fields_sv["Hệ ĐT"].current(0)
        self.fields_sv["Hệ ĐT"].grid(row=1, column=3, padx=5, pady=2, sticky='w')

        tk.Label(form_frame_sv, text="Ngày sinh", font=('Arial', 12), bg='#F0F8FF').grid(row=2, column=0, padx=5, pady=2, sticky='e')
        self.fields_sv["Ngày sinh"] = DateEntry(form_frame_sv, font=('Arial', 12), width=18, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
        self.fields_sv["Ngày sinh"].grid(row=2, column=1, padx=5, pady=2, sticky='w')

        tk.Label(form_frame_sv, text="Địa chỉ", font=('Arial', 12), bg='#F0F8FF').grid(row=2, column=2, padx=5, pady=2, sticky='e')
        self.fields_sv["Địa chỉ"] = tk.Entry(form_frame_sv, font=('Arial', 12), width=20)
        self.fields_sv["Địa chỉ"].grid(row=2, column=3, padx=5, pady=2, sticky='w')

        tk.Label(form_frame_sv, text="Giới tính", font=('Arial', 12), bg='#F0F8FF').grid(row=3, column=0, padx=5, pady=2, sticky='e')
        self.gt_var = tk.StringVar(value="Nam")
        gt_frame = tk.Frame(form_frame_sv, bg='#F0F8FF')
        gt_frame.grid(row=3, column=1, padx=5, pady=2, sticky='w')
        tk.Radiobutton(gt_frame, text="Nam", variable=self.gt_var, value="Nam", bg='#F0F8FF', font=('Arial', 12)).pack(side='left', padx=5)
        tk.Radiobutton(gt_frame, text="Nữ", variable=self.gt_var, value="Nữ", bg='#F0F8FF', font=('Arial', 12)).pack(side='left', padx=5)
        self.fields_sv["Giới tính"] = self.gt_var

        tk.Label(form_frame_sv, text="Số điện thoại", font=('Arial', 12), bg='#F0F8FF').grid(row=3, column=2, padx=5, pady=2, sticky='e')
        self.fields_sv["Số ĐT"] = tk.Entry(form_frame_sv, font=('Arial', 12), width=20)
        self.fields_sv["Số ĐT"].grid(row=3, column=3, padx=5, pady=2, sticky='w')

        btn_frame_sv = tk.Frame(self, bg='#F0F8FF')
        btn_frame_sv.pack(pady=10)

        self.add_button = tk.Button(btn_frame_sv, text="Thêm", command=self.add_sinhvien,
                               font=('Arial', 12, 'bold'),
                               bg="#28a745", fg="white",
                               activebackground="#1e7e34", activeforeground="white",
                               relief="raised", bd=2, width=12, height=2)
        self.add_button.grid(row=0, column=0, padx=5)

        self.update_button = tk.Button(btn_frame_sv, text="Cập nhật", command=self.update_sinhvien,
                                  font=('Arial', 12, 'bold'),
                                  bg="#fd7e14", fg="white",
                                  activebackground="#d46b08", activeforeground="white",
                                  relief="raised", bd=2, width=12, height=2)
        self.update_button.grid(row=0, column=1, padx=5)

        self.delete_button = tk.Button(btn_frame_sv, text="Xóa", command=self.delete_sinhvien,
                                  font=('Arial', 12, 'bold'),
                                  bg="#dc3545", fg="white",
                                  activebackground="#a71d2a", activeforeground="white",
                                  relief="raised", bd=2, width=12, height=2)
        self.delete_button.grid(row=0, column=2, padx=5)

        self.load_button = tk.Button(btn_frame_sv, text="Tải dữ liệu", command=self.load_sinhvien,
                                     font=('Arial', 12, 'bold'),
                                     bg="#007bff", fg="white",
                                     activebackground="#0056b3", activeforeground="white",
                                     relief="raised", bd=2, width=12, height=2)
        self.load_button.grid(row=0, column=3, padx=5)

        self.export_button = tk.Button(btn_frame_sv, text="Xuất dữ liệu", command=self.export_sinhvien,
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
        
    def search_sinhvien(self):
        query = self.search_var.get().lower()
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            if any(query in str(value).lower() for value in values):
                self.tree.selection_set(item)
                self.tree.see(item)
                return
        messagebox.showinfo("Không tìm thấy", "Không có sinh viên nào khớp với từ khóa.")

    def tree_selection(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], 'values')
            for i, field in enumerate(self.cols):
                widget = self.fields_sv[field]
                if field == "Giới tính":
                    widget.set(values[i])
                elif field == "Ngày sinh":
                    widget.set_date(values[i])
                else:
                    widget.delete(0, 'end')
                    widget.insert(0, values[i])

    
    def add_sinhvien(self):
        values = []
        for field in self.cols:
            widget = self.fields_sv[field]
            if field == "Ngày sinh":
                values.append(widget.get_date().strftime("%d/%m/%Y"))
            elif field == "Giới tính":
                values.append(widget.get())
            elif field == "Hệ ĐT":
                values.append(widget.get())
            else:
                values.append(widget.get().strip())

        if not all(values):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin.")
            return

        new_masv = values[0]
        for item in self.tree.get_children():
            current_masv = self.tree.item(item, 'values')[0]
            if new_masv == current_masv:
                messagebox.showwarning("Trùng mã", f"Mã sinh viên '{new_masv}' đã tồn tại.")
                return

        self.tree.insert('', 'end', values=values)

        for field in self.fields_sv.keys():
            if field not in ["Giới tính", "Ngày sinh", "Hệ ĐT"]:
                self.fields_sv[field].delete(0, 'end')

    def update_sinhvien(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Chưa chọn", "Vui lòng chọn một dòng để cập nhật.")
            return

        values = []
        for field in self.cols:
            widget = self.fields_sv[field]
            if field == "Ngày sinh":
                values.append(widget.get_date().strftime("%d/%m/%Y"))
            elif field == "Giới tính":
                values.append(widget.get())
            elif field == "Hệ ĐT":
                values.append(widget.get())
            else:
                values.append(widget.get().strip())

        if not all(values):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin.")
            return

        new_masv = values[0]
        current_item = selected[0]

        for item in self.tree.get_children():
            if item != current_item:
                existing_masv = self.tree.item(item, 'values')[0]
                if existing_masv == new_masv:
                    messagebox.showwarning("Trùng mã", f"Mã sinh viên '{new_masv}' đã tồn tại.")
                    return

        self.tree.item(current_item, values=values)

        for field in self.fields_sv.keys():
            if field not in ["Giới tính", "Ngày sinh", "Hệ ĐT"]:
                self.fields_sv[field].delete(0, 'end')

    def delete_sinhvien(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Chưa chọn", "Vui lòng chọn một dòng để xóa.")
            return

        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa sinh viên này?"):
            for item in selected:
                self.tree.delete(item)
            
    def load_sinhvien(self):
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
                        item.get("ngaysinh", ""),
                        item.get("diachi", ""),
                        item.get("sdt", ""),
                        item.get("gioitinh", ""),
                        item.get("lop", ""),
                        item.get("hedt", "")
                    ))
                messagebox.showinfo("Thành công", "Dữ liệu đã được tải thành công.")
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

    def export_sinhvien(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if path:
            try:
                data = []
                for item in self.tree.get_children():
                    values = self.tree.item(item, 'values')
                    data.append({
                        "masv": values[0],
                        "hoten": values[1],
                        "ngaysinh": values[2],
                        "diachi": values[3],
                        "sdt": values[4],
                        "gioitinh": values[5],
                        "lop": values[6],
                        "hedt": values[7]
                    })
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                messagebox.showinfo("Thành công", "Dữ liệu đã được xuất thành công.")
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
