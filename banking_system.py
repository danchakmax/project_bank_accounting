from tkinter import messagebox, simpledialog
from datetime import datetime, timedelta
from tkinter import *
import json
from admin_interface import AdminInterface

class UserManager:
    def __init__(self, file_path="bank_data.jsonl"):
        self.file_path = file_path
        self.users = self.load_data()
    @staticmethod
    def load_data():
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

class UserInterface:
    def __init__(self, master, user_manager, bank_system):
        self.master = master
        self.user_manager = user_manager
        self.bank_system = bank_system

    @staticmethod
    def is_valid_phone(value):
        if (value.startswith('+380') and len(value) == 13 and value[4:].isdigit()) or \
                (value.startswith('0') and len(value) == 10 and value.isdigit()):
            return True
        return False

    @staticmethod
    def is_positive_integer( value):
        return value.isdigit() and int(value) > 0

    @staticmethod
    def check_age( age):
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

        if phone in self.user_manager.users:
            messagebox.showerror("Error", "Account with this phone number already exists!")
            return

        self.user_manager.users[phone] = {
            'name': name,
            'phone': phone,
            'age': int(age),
            'salary': int(salary),
            'balance': 100,
            'pin': pin,
            'loan_amount': 0,
            'transactions': ["Account created with initial bonus: +100"]
        }
        self.user_manager.save_data()
        messagebox.showinfo("Success", "Account created successfully with a bonus of 100!")

        self.create_account_frame.pack_forget()
        self.bank_system.init_main_screen()

    def login(self):
        phone = self.login_phone_entry.get().strip()
        pin = self.login_pin_entry.get().strip()

        if not phone:
            messagebox.showerror("Error", "Please enter your phone number!")
            self.login_phone_entry.delete(0, END)
            return
        if not pin:
            messagebox.showerror("Error", "Please enter your PIN!")
            self.login_pin_entry.delete(0, END)
            return
        if phone not in self.user_manager.users:
            messagebox.showerror("Error", "Account with this phone number does not exist!")
            self.login_phone_entry.delete(0, END)
            self.login_pin_entry.delete(0, END)
            return
        if self.user_manager.users[phone]["pin"] != pin:
            messagebox.showerror("Error", "Incorrect PIN!")
            self.login_pin_entry.delete(0, END)
            return
        else:
            self.current_user_data = self.user_manager.users[phone]
            self.login_phone_entry.delete(0, END)
            self.login_pin_entry.delete(0, END)
            self.login_frame.pack_forget()
            self.show_user_details()

    def go_back_to_main(self):
        if hasattr(self, 'create_account_frame'):
            self.create_account_frame.pack_forget()
        if hasattr(self, 'login_frame'):
            self.login_frame.pack_forget()
        if hasattr(self, 'user_details_frame'):
            self.user_details_frame.pack_forget()

        self.bank_system.init_main_screen()

    def show_login(self):
        self.clear_screen()

        self.login_frame = Frame(self.master, bg="#FFFFFF")
        self.login_frame.pack(pady=20)

        Label(self.login_frame, text="Phone:", font=("Arial", 14), bg="#FFFFFF").grid(row=0, column=0, padx=10, pady=10)
        self.login_phone_entry = Entry(self.login_frame, font=("Arial", 14))
        self.login_phone_entry.grid(row=0, column=1, padx=10, pady=10)
        Label(self.login_frame, text="PIN:", font=("Arial", 14), bg="#FFFFFF").grid(row=1, column=0, padx=10, pady=10)
        self.login_pin_entry = Entry(self.login_frame, show="*", font=("Arial", 14))
        self.login_pin_entry.grid(row=1, column=1, padx=10, pady=10)

        Button(self.login_frame, text="Login", font=('Arial', 12), bg='#4CAF50', fg='#FFFFFF', command=self.login).grid(
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

        if new_phone in self.user_manager.users:
            messagebox.showerror("Error", "Phone number is already associated with another account!")
            return

        old_phone = self.current_user_data["phone"]
        self.user_manager.users[new_phone] = self.user_manager.users.pop(old_phone)
        self.user_manager.users[new_phone]["phone"] = new_phone
        self.user_manager.save_data()

        messagebox.showinfo("Success", f"Phone number changed to {new_phone} successfully!")
        self.show_user_details()

    def change_password(self):
        new_pin = self.new_pin_entry.get().strip()
        confirm_new_pin = self.confirm_new_pin_entry.get().strip()

        if not new_pin.isdigit() or len(new_pin) != 4:
            messagebox.showerror("Error", "PIN must consist of 4 digits!")
            return

        if new_pin != confirm_new_pin:
            messagebox.showerror("Error", "PIN codes do not match!")
            return

        if new_pin == self.current_user_data['pin']:
            messagebox.showerror("Error", "The new PIN code must be different from the old one!")
            return

        self.current_user_data['pin'] = new_pin
        self.user_manager.save_data()
        messagebox.showinfo("Success", "PIN code successfully changed!")

        self.change_password_frame.pack_forget()
        self.show_user_details()

    def back_to_user_details(self):
        self.change_password_frame.pack_forget()
        self.show_user_details()

    def show_change_password(self):
        self.user_details_frame.pack_forget()

        self.change_password_frame = Frame(self.master, bg="#FFFFFF")
        self.change_password_frame.pack(pady=20)

        Label(self.change_password_frame, text="New PIN:", font=("Arial", 14), bg="#FFFFFF").grid(row=0, column=0,
                                                                                                  padx=10,
                                                                                                  pady=10)
        self.new_pin_entry = Entry(self.change_password_frame, show="*", font=("Arial", 14))
        self.new_pin_entry.grid(row=0, column=1, padx=10, pady=10)

        Label(self.change_password_frame, text="Confirm new PIN:", font=("Arial", 14), bg="#FFFFFF").grid(row=1,
                                                                                                          column=0,
                                                                                                          padx=10,
                                                                                                          pady=10)
        self.confirm_new_pin_entry = Entry(self.change_password_frame, show="*", font=("Arial", 14))
        self.confirm_new_pin_entry.grid(row=1, column=1, padx=10, pady=10)

        Button(self.change_password_frame, text="Save", font=('Arial', 12), bg='#C2E7B1', fg='#FFFFFF',
               command=self.change_password).grid(row=2, column=1, pady=10)
        Button(self.change_password_frame, text="Back", font=('Arial', 12), command=self.back_to_user_details).grid(
            row=2,
            column=0,
            pady=10)

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

        Button(self.user_details_frame, text="Change Phone Number", font=('Arial', 12), bg='#FFDDC1',
               command=self.change_phone_number).pack(pady=5)
        Button(self.user_details_frame, text="Change PIN", font=('Arial', 12), bg='#FFDDC1',
               command=self.show_change_password).pack(pady=5)
        Button(self.user_details_frame, text="Apply for Loan", command=self.apply_for_loan).pack(
            pady=5)
        Button(self.user_details_frame, text="Repay Loan", command=self.repay_loan).pack(pady=5)
        Button(self.user_details_frame, text="Back", font=('Arial', 12), command=self.go_back_to_main).pack(pady=10)


    def show_create_account(self):
        self.clear_screen()

        self.create_account_frame = Frame(self.master, bg='#F0F0F0')
        self.create_account_frame.pack(pady=20)

        Label(self.create_account_frame, text="Name:", font=('Arial', 12), bg='#F0F0F0').grid(row=0, column=0, padx=10, pady=10)
        Label(self.create_account_frame, text="Phone:", font=('Arial', 12), bg='#F0F0F0').grid(row=1, column=0, padx=10, pady=10)
        Label(self.create_account_frame, text="Age:", font=('Arial', 12), bg='#F0F0F0').grid(row=2, column=0, padx=10, pady=10)
        Label(self.create_account_frame, text="Salary:", font=('Arial', 12), bg='#F0F0F0').grid(row=3, column=0,padx=10, pady=10)
        Label(self.create_account_frame, text="PIN:", font=('Arial', 12), bg='#F0F0F0').grid(row=4, column=0, padx=10, pady=10)
        Label(self.create_account_frame, text="Confirm PIN:", font=('Arial', 12), bg='#F0F0F0').grid(row=5, column=0, padx=10, pady=10)

        self.name_entry = Entry(self.create_account_frame, font=('Arial', 12))
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)
        self.phone_entry = Entry(self.create_account_frame, font=('Arial', 12))
        self.phone_entry.grid(row=1, column=1, padx=10, pady=10)
        self.age_entry = Entry(self.create_account_frame, font=('Arial', 12))
        self.age_entry.grid(row=2, column=1, padx=10, pady=10)
        self.salary_entry = Entry(self.create_account_frame, font=('Arial', 12))
        self.salary_entry.grid(row=3, column=1, padx=10, pady=10)
        self.pin_entry = Entry(self.create_account_frame, show="*", font=('Arial', 12))
        self.pin_entry.grid(row=4, column=1, padx=10, pady=10)
        self.confirm_pin_entry = Entry(self.create_account_frame, show="*", font=('Arial', 12))
        self.confirm_pin_entry.grid(row=5, column=1, padx=10, pady=10)

        Button(self.create_account_frame, text="Create Account", font=('Arial', 12), bg='#4CAF50', fg='#FFFFFF', command=self.create_account).grid(row=6, column=1, pady=20)
        Button(self.create_account_frame, text="Back", font=('Arial', 12), command=self.go_back_to_main).grid(row=6, column=0, pady=20)

    def clear_screen(self):
        for widget in self.master.winfo_children():
            widget.pack_forget()

    def apply_for_loan(self):

        if self.current_user_data.get("loan_amount", 0) > 0:
            messagebox.showerror("Loan Denied",
                                 "You already have an active loan. Please repay it before applying for a new one.")
            return

        max_loan_amount = int(self.current_user_data["salary"])
        loan_amount = simpledialog.askinteger("Loan Application", f"Enter loan amount (Max {max_loan_amount}):")

        if loan_amount is None or loan_amount <= 0:
            messagebox.showerror("Error", "Invalid loan amount!")
            return

        if loan_amount > max_loan_amount:
            messagebox.showerror("Loan Denied", f"Loan amount exceeds limit! Maximum loan amount is {max_loan_amount}.")
            return

        loan_term_days = simpledialog.askinteger("Loan Term", "Enter loan term in days (e.g., 7, 14, 30):",
                                                 initialvalue=7)
        if loan_term_days not in [7, 14, 30]:
            messagebox.showerror("Error", "Invalid loan term! Unfortunately, we do not have such a credit plan.")
            return

        interest_rate = 1.01 if loan_term_days == 7 else 1.03 if loan_term_days == 14 else 1.05

        self.current_user_data["loan_amount"] = loan_amount
        self.current_user_data["balance"] += loan_amount
        self.current_user_data["loan_start_date"] = datetime.now().strftime("%Y-%m-%d")
        self.current_user_data["loan_due_date"] = (datetime.now() + timedelta(days=loan_term_days)).strftime("%Y-%m-%d")
        self.current_user_data["interest_rate"] = interest_rate
        self.current_user_data["transactions"].append(f"Loan granted: +{loan_amount}")

        self.user_manager.save_data()
        messagebox.showinfo("Success", f"Loan of {loan_amount} granted successfully!")
        self.show_user_details()

    def repay_loan(self):
        loan_amount = self.current_user_data.get("loan_amount", 0)
        if loan_amount <= 0:
            messagebox.showinfo("No Active Loan", "You have no active loan to repay.")
            return

        amount_to_repay = simpledialog.askinteger("Repay Loan",
                                                  f"Enter amount to repay (Outstanding loan: {loan_amount}):")
        if amount_to_repay is None:
            return

        if amount_to_repay <= 0:
            messagebox.showerror("Error", "The repayment amount must be positive!")
            return

        if amount_to_repay > self.current_user_data["balance"]:
            messagebox.showerror("Error", "Insufficient funds to make this repayment.")
            return

        if amount_to_repay >= loan_amount:
            self.current_user_data["balance"] -= loan_amount
            self.current_user_data["loan_amount"] = 0
            self.current_user_data["transactions"].append(f"Loan fully repaid: -{loan_amount}")
            messagebox.showinfo("Loan Repayment", "Your loan has been fully repaid!")
        else:
            self.current_user_data["balance"] -= amount_to_repay
            self.current_user_data["loan_amount"] -= amount_to_repay
            self.current_user_data["transactions"].append(f"Partial loan repayment: -{amount_to_repay}")
            messagebox.showinfo("Loan Repayment", f"Paid {amount_to_repay} towards loan.")

        self.user_manager.save_data()
        self.show_user_details()

    def update_loan_interest(self):

        loan_amount = self.current_user_data.get("loan_amount", 0)
        if loan_amount <= 0:
            return

        loan_start_date = datetime.strptime(self.current_user_data["loan_start_date"], "%Y-%m-%d")
        loan_due_date = datetime.strptime(self.current_user_data["loan_due_date"], "%Y-%m-%d")
        current_date = datetime.now()

        is_overdue = current_date > loan_due_date
        overdue_days = (current_date - loan_due_date).days if is_overdue else 0
        days_since_start = (current_date - loan_start_date).days

        interest_rate = self.current_user_data.get("interest_rate", 1.01)

        updated_loan_amount = loan_amount * (interest_rate ** days_since_start)

        if is_overdue:
            penalty_rate = 1.1
            updated_loan_amount *= penalty_rate ** overdue_days
            self.current_user_data["transactions"].append(f"Penalty added for {overdue_days} overdue days.")

        self.current_user_data["loan_amount"] = round(updated_loan_amount, 2)
        self.user_manager.save_data()


class BankSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("Bank Management System")
        self.master.geometry("500x500")

        self.user_manager = UserManager()
        self.user_interface = UserInterface(master, self.user_manager, self)
        self.admin_interface = AdminInterface(self, self.user_manager)

        self.init_main_screen()

    def init_main_screen(self):
        self.clear_screen()
        self.main_screen_frame = Frame(self.master, bg="#FFFFFF", padx=20, pady=20)
        self.main_screen_frame.pack(pady=20)

        Label(self.main_screen_frame, text="Bank Management System", font=("Arial", 16), bg="#FFFFFF").pack(pady=10)

        Button(self.main_screen_frame, text="Create Account", font=('Arial', 14), bg='#4CAF50', fg='#FFFFFF',
               command=self.user_interface.show_create_account).pack(pady=10)
        Button(self.main_screen_frame, text="Login", font=('Arial', 14), bg='#4CAF50', fg='#FFFFFF',
               command=self.user_interface.show_login).pack(pady=10)
        Button(self.main_screen_frame, text="Admin Login", font=('Arial', 14), bg='#FF5733', fg='#FFFFFF',
               command=self.admin_interface.show_admin_login).pack(pady=10)

    def clear_screen(self):
        for widget in self.master.winfo_children():
            widget.pack_forget()

def main():
    root = Tk()
    bank_system = BankSystem(root)
    root.mainloop()

if __name__ == '__main__':
    main()
