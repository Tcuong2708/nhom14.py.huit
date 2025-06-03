import json
from tkinter import messagebox
import os
USER_CONFIG_FILE = 'user_config.json'
USERS_FILE = 'users.json'

def load_user_config():
    try:
        with open(USER_CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_user_config(config):
    try:
        with open(USER_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể lưu cấu hình: {e}")

def load_users():
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_users(users):
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể lưu người dùng: {e}")

def clear_user_config():
    if os.path.exists(USER_CONFIG_FILE):
        try:
            os.remove(USER_CONFIG_FILE)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xoá cấu hình: {e}")