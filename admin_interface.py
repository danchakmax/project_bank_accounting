from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
class AdminInterface:
    def __init__(self, master, user_manager, main_screen_callback):
        self.master = master
        self.user_manager = user_manager
        self.main_screen_callback = main_screen_callback
        self.master.title("Bank Management System")
        self.master.geometry("500x600")


    def show_admin_login(self):
        self.clear_screen()

        self.admin_login_frame = Frame(self.master, bg="#FFFFFF")
        self.admin_login_frame.pack(pady=10)

        Label(self.admin_login_frame, text="Admin PIN:", font=("Arial", 14), bg="#FFFFFF").grid(row=0, column=0,
                                                                                                padx=10, pady=10)
        self.admin_pin_entry = Entry(self.admin_login_frame, show="*", font=("Arial", 14))
        self.admin_pin_entry.grid(row=0, column=1, padx=10, pady=10)

        Button(self.admin_login_frame, text="Login", font=('Arial', 12), bg='#FF5733', fg='#FFFFFF',
               command=self.admin_login, width=20).grid(row=1, column=1, pady=10)
        Button(self.admin_login_frame, text="Back", font=('Arial', 12), command=self.go_back_to_main, width=10, bg='#ec5353').grid(row=1,
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

        Button(self.admin_dashboard_frame, text="View All Accounts", font=('Arial', 12),
               command=self.show_all_accounts,width=25).pack(pady=10)

        Button(self.admin_dashboard_frame, text="Salary Distribution Chart", font=('Arial', 12),
               command=self.salary_distribution_chart,width=25).pack(pady=10)
        Button(self.admin_dashboard_frame, text="Balance statistics", font=('Arial', 12),
               command=self.balance_statistics,width=25).pack(pady=10)
        Button(self.admin_dashboard_frame, text="Export User Data to CSV", font=('Arial', 12),
               command=self.export_user_data_to_csv,width=25).pack(pady=10)
        Button(self.admin_dashboard_frame, text="Balance vs Age Chart", font=('Arial', 12), 
               command=self.balance_vs_age_chart,width=25).pack(pady=10)
        Button(self.admin_dashboard_frame, text="Age Distribution Histogram", font=('Arial', 12), command=self.age_histogram,width=25).pack(pady=10)
        Button(self.admin_dashboard_frame, text="Credit Distribution Chart", font=('Arial', 12),command=self.credit_distribution_chart,width=25).pack(pady=10)
        Button(self.admin_dashboard_frame, text="Back", font=('Arial', 12), bg="#ec5353", command=self.go_back_to_main,width=25).pack(pady=10)

    def show_all_accounts(self):
        self.clear_screen()

        self.admin_accounts_frame = Frame(self.master, bg="#FFFFFF", padx=20, pady=20)
        self.admin_accounts_frame.pack(pady=20)

        Label(self.admin_accounts_frame, text="All User Accounts", font=("Arial", 16), bg="#FFFFFF").pack(pady=10)

        for phone, data in self.user_manager.users.items():
            Label(self.admin_accounts_frame, text=f"Phone: {phone}, Name: {data['name']}, Balance: {data['balance']}",
                  font=("Arial", 12), bg="#FFFFFF").pack(pady=5)

        Button(self.admin_accounts_frame, text="Back", font=('Arial', 12), command=self.show_admin_dashboard, bg='#ec5353', width=20).pack(pady=10)

    def go_back_to_main(self):
        self.clear_screen()
        self.main_screen_callback()

    def clear_screen(self):
        for widget in self.master.winfo_children():
            widget.pack_forget()

    def salary_distribution_chart(self):
        data = []
        for phone, user_data in self.user_manager.users.items():
            data.append({
                "Phone": phone,
                "Name": user_data.get("name"),
                "Salary": user_data.get("salary", 0)
            })

        df = pd.DataFrame(data)

        if df.empty:
            messagebox.showerror("Error", "Немає даних про заробітні плати.")
            return

        salary_ranges = pd.cut(df['Salary'], bins=[0, 1000, 3000, 5000, 10000, 20000, np.inf], labels=[
            '0-1000', '1000-3000', '3000-5000', '5000-10000', '10000-20000', '20000+'])

        salary_distribution = salary_ranges.value_counts()

        plt.figure(figsize=(8, 6))
        salary_distribution.plot(kind='pie', autopct='%1.1f%%', startangle=90, colormap='tab10')
        plt.title("Розподіл користувачів за рівнями заробітної плати")
        plt.ylabel("")
        plt.show()

    def balance_statistics(self):
        balances = np.array([user_data.get("balance", 0) for user_data in self.user_manager.users.values()])

        if balances.size == 0:
            messagebox.showerror("Error", "Немає даних про баланс користувачів.")
            return

        average_balance = np.mean(balances)
        median_balance = np.median(balances)
        std_dev_balance = np.std(balances)
        min_balance = np.min(balances)
        max_balance = np.max(balances)

        report = (
            f"Середній баланс: {average_balance:.2f}\n"
            f"Медіанний баланс: {median_balance:.2f}\n"
            f"Стандартне відхилення: {std_dev_balance:.2f}\n"
            f"Мінімальний баланс: {min_balance:.2f}\n"
            f"Максимальний баланс: {max_balance:.2f}"
        )

        messagebox.showinfo("Баланс Користувачів - Статистика", report)

    def export_user_data_to_csv(self):
        data = []
        for phone, user_data in self.user_manager.users.items():
            data.append({
                "Phone": phone,
                "Name": user_data.get("name", "N/A"),
                "Balance": user_data.get("balance", 0),
                "Loan Amount": user_data.get("loan_amount", 0),
                "Salary": user_data.get("salary", 0),
                "Age": user_data.get("age", "N/A")
            })

        if not data:
            messagebox.showerror("Error", "Немає даних для експорту.")
            return

        df = pd.DataFrame(data)

        file_path = "user_data_report.csv"
        df.to_csv(file_path, index=False, encoding='utf-8-sig')

        messagebox.showinfo("Success", f"Дані користувачів експортовані до файлу '{file_path}' успішно.")

    def balance_vs_age_chart(self):
        data = []
        for phone, user_data in self.user_manager.users.items():
            if "age" in user_data and "balance" in user_data:
                data.append({
                    "Age": user_data["age"],
                    "Balance": user_data["balance"]
                })

        if not data:
            messagebox.showerror("Error", "No data available to generate the chart.")
            return

        df = pd.DataFrame(data)

        age_bins = [18, 25, 35, 50, 65, 100]
        labels = ['18-25', '26-35', '36-50', '51-65', '65+']
        df["Age Group"] = pd.cut(df["Age"], bins=age_bins, labels=labels)

        avg_balance = df.groupby("Age Group")["Balance"].mean()

        plt.figure(figsize=(10, 6))
        avg_balance.plot(kind="bar", color=['blue', 'green', 'orange', 'purple', 'red'], alpha=0.7, edgecolor='black')

        plt.title("Average Balance by Age Groups", fontsize=14, fontweight='bold')
        plt.xlabel("Age Groups", fontsize=12)
        plt.ylabel("Average Balance", fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()

    def age_histogram(self):
        data = []
        for phone, user_data in self.user_manager.users.items():
            data.append({
                "Phone": phone,
                "Name": user_data.get("name"),
                "Age": user_data.get("age", None)
            })

        df = pd.DataFrame(data)

        # Ensure age data is numeric and drop NaN values
        if 'Age' not in df or df['Age'].dropna().empty:
            messagebox.showerror("Error", "No information about the age of Users.")
            return

        df['Age'] = pd.to_numeric(df['Age'], errors='coerce').dropna()

        plt.figure(figsize=(8, 6))
        plt.hist(df['Age'], bins=range(int(df['Age'].min()), int(df['Age'].max()) + 2), color='skyblue',
                 edgecolor='black')
        plt.title("Histogram of User age")
        plt.xlabel("Age")
        plt.ylabel("Number of Users")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()

    def credit_distribution_chart(self):
        # Підготовка даних
        has_credit = 0
        no_credit = 0

        for user_data in self.user_manager.users.values():
            if user_data.get("loan_amount", 0) > 0:
                has_credit += 1
            else:
                no_credit += 1

        if has_credit == 0 and no_credit == 0:
            messagebox.showerror("Error", "No User credit data.")
            return

        # Дані для кругової діаграми
        labels = ["Users with credits", "Users without credits"]
        values = [has_credit, no_credit]
        colors = ['#FF9999', '#66B3FF']

        # Побудова кругової діаграми
        plt.figure(figsize=(8, 6))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, explode=(0.1, 0))
        plt.title("Distribution of users according to availability of credits")
        plt.show()
