from tkinter import *
from tkinter import messagebox

class AdminInterface:
    def init(self, master, user_manager, main_screen_callback):
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
