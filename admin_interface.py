from tkinter import *
from tkinter import messagebox

class AdminInterface:
    def __init__(self, master, user_manager, main_screen_callback):
        self.master = master
        self.user_manager = user_manager
        self.main_screen_callback = main_screen_callback
        self.master.title("Bank Management System")
        self.master.geometry("500x500")


    def show_admin_login(self):
        self.clear_screen()

        self.admin_login_frame = Frame(self.master, bg="#FFFFFF")
        self.admin_login_frame.pack(pady=20)

        Label(self.admin_login_frame, text="Admin PIN:", font=("Arial", 14), bg="#FFFFFF").grid(row=0, column=0,
                                                                                                padx=10, pady=10)
        self.admin_pin_entry = Entry(self.admin_login_frame, show="*", font=("Arial", 14))
        self.admin_pin_entry.grid(row=0, column=1, padx=10, pady=10)

        Button(self.admin_login_frame, text="Login", font=('Arial', 12), bg='#FF5733', fg='#FFFFFF',
               command=self.admin_login).grid(row=1, column=1, pady=10)
        Button(self.admin_login_frame, text="Back", font=('Arial', 12), command=self.go_back_to_main).grid(row=1,
                                                                                              column=0, pady=10)
        
    def admin_login(self):
        admin_pin = self.admin_pin_entry.get().strip()
        correct_pin = "1234"

        if admin_pin == correct_pin:
            messagebox.showinfo("Success", "Admin login successful!")
            self.show_admin_dashboard()
        else:
            messagebox.showerror("Error", "Incorrect Admin PIN!")
            self.admin_pin_entry.delete(0, END)

    def show_admin_dashboard(self):
        self.clear_screen()

        self.admin_dashboard_frame = Frame(self.master, bg="#FFFFFF", padx=20, pady=20)
        self.admin_dashboard_frame.pack(pady=20)

        Label(self.admin_dashboard_frame, text="Admin Dashboard", font=("Arial", 16), bg="#FFFFFF").pack(pady=10)

        Button(self.admin_dashboard_frame, text="View All Accounts", font=('Arial', 12), bg='#4CAF50', fg='#FFFFFF',
               command=self.show_all_accounts).pack(pady=10)

        Button(self.admin_dashboard_frame, text="Back", font=('Arial', 12), command=self.go_back_to_main).pack(pady=10)

    def show_all_accounts(self):
        self.clear_screen()

        self.admin_accounts_frame = Frame(self.master, bg="#FFFFFF", padx=20, pady=20)
        self.admin_accounts_frame.pack(pady=20)

        Label(self.admin_accounts_frame, text="All User Accounts", font=("Arial", 16), bg="#FFFFFF").pack(pady=10)

        for phone, data in self.user_manager.users.items():
            Label(self.admin_accounts_frame, text=f"Phone: {phone}, Name: {data['name']}, Balance: {data['balance']}",
                  font=("Arial", 12), bg="#FFFFFF").pack(pady=5)

        Button(self.admin_accounts_frame, text="Back", font=('Arial', 12), command=self.show_admin_dashboard).pack(pady=10)

    def go_back_to_main(self):
        self.clear_screen()
        self.main_screen_callback()

    def clear_screen(self):
        for widget in self.master.winfo_children():
            widget.pack_forget()
