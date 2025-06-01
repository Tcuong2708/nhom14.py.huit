import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json

class LopFrame(tk.Frame):
    def __init__(self, master, role):
        super().__init__(master, bg='#F0F8FF')
        self.role = role
        
        tk.Frame(self, height=30, bg='#F0F8FF').pack()
        
        tk.Label(self, text="LỚP", font=('Arial', 18, 'bold'), bg='#F0F8FF', fg='darkblue').pack(pady=(10, 10))

        search_frame = tk.Frame(self, bg='#F0F8FF')
        search_frame.pack(pady=(0, 5))

        tk.Label(search_frame, text="Tìm kiếm:", font=('Arial', 12), bg='#F0F8FF').pack(side='left', padx=(0, 5))
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, font=('Arial', 12), width=30).pack(side='left')
        tk.Button(search_frame, text="Tìm", font=('Arial', 11, 'bold'), bg='#1E90FF', fg='white', command=self.search_lop).pack(side='left', padx=5)
        
        self.cols = ("Mã lớp", "Tên lớp", "Khoa", "Khóa học")
        self.tree = ttk.Treeview(self, columns=self.cols, show='headings')
        for col in self.cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor='center')
        self.tree.pack(pady=10)
        self.tree.bind('<<TreeviewSelect>>', self.tree_selection)
        
        form_frame_lop = tk.Frame(self, bg='#F0F8FF')
        form_frame_lop.pack(pady=(5, 5))

        self.fields_lop = {}

        tk.Label(form_frame_lop, text="Mã lớp", font=('Arial', 12), bg='#F0F8FF').grid(row=0, column=0, padx=5, pady=2, sticky='e')
        self.fields_lop["Mã lớp"] = tk.Entry(form_frame_lop, font=('Arial', 12), width=20)
        self.fields_lop["Mã lớp"].grid(row=0, column=1, padx=5, pady=2, sticky='w')

        tk.Label(form_frame_lop, text="Tên lớp", font=('Arial', 12), bg='#F0F8FF').grid(row=0, column=2, padx=5, pady=2, sticky='e')
        self.fields_lop["Tên lớp"] = tk.Entry(form_frame_lop, font=('Arial', 12), width=20)
        self.fields_lop["Tên lớp"].grid(row=0, column=3, padx=5, pady=2, sticky='w')

        tk.Label(form_frame_lop, text="Khoa", font=('Arial', 12), bg='#F0F8FF').grid(row=1, column=0, padx=5, pady=2, sticky='e')
        self.fields_lop["Khoa"] = tk.Entry(form_frame_lop, font=('Arial', 12), width=20)
        self.fields_lop["Khoa"].grid(row=1, column=1, padx=5, pady=2, sticky='w')

        tk.Label(form_frame_lop, text="Khóa học", font=('Arial', 12), bg='#F0F8FF').grid(row=1, column=2, padx=5, pady=2, sticky='e')
        self.fields_lop["Khóa học"] = tk.Entry(form_frame_lop, font=('Arial', 12), width=20)
        self.fields_lop["Khóa học"].grid(row=1, column=3, padx=5, pady=2, sticky='w')

        btn_frame_lop = tk.Frame(self, bg='#F0F8FF')
        btn_frame_lop.pack(pady=10)

        self.add_button = tk.Button(btn_frame_lop, text="Thêm", command=self.add_lop,
                                    font=('Arial', 12, 'bold'),
                                    bg="#28a745", fg="white",
                                    activebackground="#1e7e34", activeforeground="white",
                                    relief="raised", bd=2, width=12, height=2)
        self.add_button.grid(row=0, column=0, padx=5)
        
        self.update_button = tk.Button(btn_frame_lop, text="Cập nhật", command=self.update_lop,
                                       font=('Arial', 12, 'bold'),
                                       bg="#fd7e14", fg="white",
                                       activebackground="#d46b08", activeforeground="white",
                                       relief="raised", bd=2, width=12, height=2)
        self.update_button.grid(row=0, column=1, padx=5)

        self.delete_button = tk.Button(btn_frame_lop, text="Xóa", command=self.delete_lop,
                                       font=('Arial', 12, 'bold'),
                                       bg="#dc3545", fg="white",
                                       activebackground="#a71d2a", activeforeground="white",
                                       relief="raised", bd=2, width=12, height=2)
        self.delete_button.grid(row=0, column=2, padx=5)

        self.load_button = tk.Button(btn_frame_lop, text="Tải dữ liệu", command=self.load_lop,
                                     font=('Arial', 12, 'bold'),
                                     bg="#007bff", fg="white",
                                     activebackground="#0056b3", activeforeground="white",
                                     relief="raised", bd=2, width=12, height=2)
        self.load_button.grid(row=0, column=3, padx=5)

        self.export_button = tk.Button(btn_frame_lop, text="Xuất dữ liệu", command=self.export_lop,
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
        
    def search_lop(self):
        query = self.search_var.get().lower()
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            if any(query in str(value).lower() for value in values):
                self.tree.selection_set(item)
                self.tree.see(item)
                break
        else:
            messagebox.showinfo("Không tìm thấy", "Không có lớp nào khớp với từ khóa.")

    def tree_selection(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], 'values')
            for i, field in enumerate(self.fields_lop):
                self.fields_lop[field].delete(0, 'end')
                self.fields_lop[field].insert(0, values[i])
                
    def add_lop(self):
        values = [self.fields_lop[field].get().strip() for field in self.fields_lop]

        if not all(values):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin.")
            return

        new_malop = values[0]
        for item in self.tree.get_children():
            current_malop = self.tree.item(item, 'values')[0]
            if new_malop == current_malop:
                messagebox.showwarning("Trùng mã lớp", f"Mã lớp '{new_malop}' đã tồn tại.")
                return

        self.tree.insert('', 'end', values=values)

        for field in self.fields_lop:
            self.fields_lop[field].delete(0, 'end')

    def update_lop(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Chưa chọn", "Vui lòng chọn một dòng để cập nhật.")
            return

        new_values = [self.fields_lop[field].get().strip() for field in self.fields_lop]

        if not all(new_values):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin.")
            return

        new_malop = new_values[0]
        item = selected[0]
        old_malop = self.tree.item(item, 'values')[0]

        for other_item in self.tree.get_children():
            if other_item != item:
                existing_malop = self.tree.item(other_item, 'values')[0]
                if existing_malop == new_malop:
                    messagebox.showwarning("Trùng mã lớp", f"Mã lớp '{new_malop}' đã tồn tại.")
                    return

        self.tree.item(item, values=new_values)

        for field in self.fields_lop:
            self.fields_lop[field].delete(0, 'end')

    def delete_lop(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Chưa chọn", "Vui lòng chọn một dòng để xóa.")
            return

        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa lớp này?"):
            for item in selected:
                self.tree.delete(item)

    def load_lop(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.tree.delete(*self.tree.get_children())
                for item in data:
                    self.tree.insert('', 'end', values=(
                        item.get("malop", ""),
                        item.get("tenlop", ""),
                        item.get("khoa", ""),
                        item.get("khoahoc", "")
                    ))
                messagebox.showinfo("Thành công", "Đã tải dữ liệu lớp thành công!")
            except Exception as e:
                messagebox.showerror("Lỗi tải dữ liệu", str(e))

    def export_lop(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if path:
            try:
                data = []
                for item in self.tree.get_children():
                    values = self.tree.item(item, 'values')
                    data.append({
                        "malop": values[0],
                        "tenlop": values[1],
                        "khoa": values[2],
                        "khoahoc": values[3]
                    })
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                messagebox.showinfo("Thành công", "Dữ liệu lớp đã được xuất thành công.")
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
