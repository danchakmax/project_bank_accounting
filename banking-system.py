from tkinter import messagebox, simpledialog
from datetime import datetime
from tkinter import *
import json

class BankSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("Bank Management System")
        self.master.geometry("500x500")

        self.users = self.load_data()
        self.init_main_screen()
        self.current_user_data = None

    def load_data(self):
        users = {}
        try:
            with open("bank_data.jsonl", "r") as file:
                for line in file:
                    user_data = json.loads(line.strip())
                    users[user_data["phone"]] = user_data
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return users


    def save_data(self):

        with open("bank_data.jsonl", "w") as file:
            for user_data in self.users.values():
                json.dump(user_data, file)
                file.write("\n")


    def is_valid_phone(self, value):
        if (value.startswith('+380') and len(value) == 13 and value[4:].isdigit()) or \
                (value.startswith('0') and len(value) == 10 and value.isdigit()):
            return True
        return False

    def is_positive_integer(self, value):
        return value.isdigit() and int(value) > 0

    def check_age(self, age):
        return int(age) >= 18

    def create_account(self):

        name = self.name_entry.get()
        phone = self.phone_entry.get()
        age = self.age_entry.get()
        salary = self.salary_entry.get()
        pin = self.pin_entry.get()
        confirm_pin = self.confirm_pin_entry.get()

        if not name:
            messagebox.showerror("Error", "Name is required!")
            return

        if not phone or not self.is_valid_phone(phone):
            messagebox.showerror("Error", "Invalid phone number format!")
            return

        if not self.is_positive_integer(age) or not self.check_age(age) :
            messagebox.showerror("Error", "Wrong age")
            return

        if not self.is_positive_integer(salary):
            messagebox.showerror("Error", "Salary must be a positive integer!")
            return

        if not pin.isdigit() or len(pin) != 4:
            messagebox.showerror("Error", "PIN must be a 4-digit number!")
            return

        if pin != confirm_pin:
            messagebox.showerror("Error", "PIN codes do not match!")
            return

        if phone in self.users:
            messagebox.showerror("Error", "Account with this phone number already exists!")
            return

        self.users[phone] = {
            'name': name,
            'phone': phone,
            'age': int(age),
            'salary': int(salary),
            'balance': 100,
            'pin': pin,
            'loan_amount': 0,
            'transactions': ["Account created with initial bonus: +100"]
        }
        self.save_data()
        messagebox.showinfo("Success", "Account created successfully with a bonus of 100!")

        self.create_account_frame.pack_forget()

    def login(self):
        phone = self.login_phone_entry.get().strip()
        pin = self.login_pin_entry.get().strip()

        if not phone or not pin:
            messagebox.showerror("Error", "Please enter both phone number and PIN!")
            return

        if phone in self.users and self.users[phone]["pin"] == pin:
            self.current_user_data = self.users[phone]
            self.login_phone_entry.delete(0, END)
            self.login_pin_entry.delete(0, END)
            self.login_frame.pack_forget()
        else:
            messagebox.showerror("Error", "Invalid phone number or PIN!")
            self.login_pin_entry.delete(0, END)

    def init_main_screen(self):
        self.main_screen_frame = Frame(self.master)
        self.main_screen_frame.pack(pady=50)

        Label(self.main_screen_frame, text="Bank Management System", font=("Arial", 16)).pack(pady=20)

        Button(self.main_screen_frame, text="Create Account", font=('Arial', 14), bg='#4CAF50', fg='#FFFFFF',)
        Button(self.main_screen_frame, text="Login", font=('Arial', 14), bg='#4CAF50', fg='#FFFFFF',)

    def go_back_to_main(self):
        if hasattr(self, 'create_account_frame'):
            self.create_account_frame.pack_forget()
        if hasattr(self, 'login_frame'):
            self.login_frame.pack_forget()
        if hasattr(self, 'user_details_frame'):
            self.user_details_frame.pack_forget()

        self.init_main_screen()

    def show_login(self):
        self.main_screen_frame.pack_forget()

        self.login_frame = Frame(self.master, bg="#FFFFFF")
        self.login_frame.pack(pady=20)

        Label(self.login_frame, text="Phone:", font=("Arial", 14), bg="#FFFFFF").grid(row=0, column=0, padx=10, pady=10)
        self.login_phone_entry = Entry(self.login_frame, font=("Arial", 14))
        self.login_phone_entry.grid(row=0, column=1, padx=10, pady=10)
        Label(self.login_frame, text="PIN:", font=("Arial", 14), bg="#FFFFFF").grid(row=1, column=0, padx=10, pady=10)
        self.login_pin_entry = Entry(self.login_frame, show="*", font=("Arial", 14))
        self.login_pin_entry.grid(row=1, column=1, padx=10, pady=10)

        Button(self.login_frame, text="Login", font=('Arial', 12), bg='#C2E7B1', fg='#FFFFFF', command=self.login).grid(
            row=2, column=1, pady=10)
        Button(self.login_frame, text="Back", font=('Arial', 12), command=self.go_back_to_main).grid(row=2, column=0,
                                                                                                     pady=10)

    def timestamp_decorator(action_description):
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                result = func(self, *args, **kwargs)
                if self.current_user_data:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                    self.current_user_data["transactions"].append(f"{timestamp} - {action_description}")
                return result

            return wrapper

        return decorator

    def change_phone_number(self):
        new_phone = simpledialog.askstring("Change Phone Number", "Enter new phone number:")

        if not new_phone or not self.is_valid_phone(new_phone):
            messagebox.showerror("Error", "Invalid phone number format!")
            return

        if new_phone in self.users:
            messagebox.showerror("Error", "Phone number is already associated with another account!")
            return

        old_phone = self.current_user_data["phone"]
        self.users[new_phone] = self.users.pop(old_phone)
        self.users[new_phone]["phone"] = new_phone
        self.save_data()

        messagebox.showinfo("Success", f"Phone number changed to {new_phone} successfully!")
        self.show_user_details()

    def show_user_details(self):
        if hasattr(self, 'user_details_frame'):
            self.user_details_frame.pack_forget()

        self.user_details_frame = Frame(self.master, bg="#D3D3D3", padx=20, pady=20)
        self.user_details_frame.pack(pady=20)

        Label(self.user_details_frame, text=f"Name: {self.current_user_data['name']}", font=('Arial', 14),
              bg="#D3D3D3").pack()
        Label(self.user_details_frame, text=f"Balance: {self.current_user_data['balance']}", font=('Arial', 14),
              bg="#D3D3D3").pack(pady=5)
        Label(self.user_details_frame, text=f"Loan Amount: {self.current_user_data.get('loan_amount', 0):.2f}",
              font=('Arial', 14), bg="#D3D3D3").pack(pady=5)


