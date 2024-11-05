from tkinter import messagebox
import json

class BankSystem:
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