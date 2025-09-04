import tkinter as tk
from tkinter import ttk, messagebox

from Admin_window import AdminWindow
from client_window import ClientWindow
from db import login_client, register_client  # Импортируйте другие функции по мере необходимости

class CinemaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Система управления кинотеатром")
        self.root.geometry("550x500+400+200")
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_frame()
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20)

        self.label = ttk.Label(self.main_frame, text="Welcome to Cinema Management System")
        self.label.pack()

        self.login_button = ttk.Button(self.main_frame, text="Войти", command=self.show_login)
        self.login_button.pack(pady=5)

        self.register_button = ttk.Button(self.main_frame, text="Зарегестрироваться", command=self.show_registration)
        self.register_button.pack(pady=5)

    def show_login(self):
        self.clear_frame()
        self.login_frame = ttk.Frame(self.root)
        self.login_frame.pack(pady=20)

        self.email_label = ttk.Label(self.login_frame, text="Email")
        self.email_label.pack()
        self.email_entry = ttk.Entry(self.login_frame)
        self.email_entry.pack()
        self.password_label = ttk.Label(self.login_frame, text="Password")
        self.password_label.pack()
        self.password_entry = ttk.Entry(self.login_frame, show='*')
        self.password_entry.pack()

        self.role_label = ttk.Label(self.login_frame, text="Выберите роль:")
        self.role_label.pack()
        self.role_combobox = ttk.Combobox(self.login_frame, values=["Администратор", "Клиент"])
        self.role_combobox.pack(pady=5)
        self.role_combobox.current(0)

        self.login_button = ttk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.pack(pady=(50, 20))

        self.back_button = ttk.Button(self.login_frame, text="Back", command=self.create_main_menu)
        self.back_button.pack(pady=5)

    def show_registration(self):
        self.clear_frame()
        self.registration_frame = tk.Frame(self.root)
        self.registration_frame.pack(pady=20)

        self.name_label = ttk.Label(self.registration_frame, text="Name")
        self.name_label.pack()
        self.name_entry = ttk.Entry(self.registration_frame)
        self.name_entry.pack()

        self.surname_label = ttk.Label(self.registration_frame, text="Surname")
        self.surname_label.pack()
        self.surname_entry = ttk.Entry(self.registration_frame)
        self.surname_entry.pack()

        self.birthday_label = ttk.Label(self.registration_frame, text="Birthday (YYYY-MM-DD)")
        self.birthday_label.pack()
        self.birthday_entry = ttk.Entry(self.registration_frame)
        self.birthday_entry.pack()

        self.phone_number_label = ttk.Label(self.registration_frame, text="Phone_number")
        self.phone_number_label.pack()
        self.phone_number_entry = ttk.Entry(self.registration_frame)
        self.phone_number_entry.pack()

        self.email_label = ttk.Label(self.registration_frame, text="Email")
        self.email_label.pack()
        self.email_entry = ttk.Entry(self.registration_frame)
        self.email_entry.pack()
        self.password_label = ttk.Label(self.registration_frame, text="Password")
        self.password_label.pack()
        self.password_entry = ttk.Entry(self.registration_frame, show='*')
        self.password_entry.pack()

        self.role_label = ttk.Label(self.registration_frame, text="Выберите роль:")
        self.role_label.pack()
        self.role_combobox = ttk.Combobox(self.registration_frame, values=["Администратор", "Клиент"])
        self.role_combobox.pack(pady=5)
        self.role_combobox.current(0)

        self.register_button = ttk.Button(self.registration_frame, text="Register", command=self.register)
        self.register_button.pack(pady=5)

        self.back_button = ttk.Button(self.registration_frame, text="Back", command=self.create_main_menu)
        self.back_button.pack(pady=5)

    def register(self):
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        phone = self.phone_number_entry.get()
        email = self.email_entry.get()
        birthday = self.birthday_entry.get()
        password = self.password_entry.get()
        role = str(self.role_combobox.get())

        # Проверка на заполненность полей
        if not all([name, surname, birthday, phone, email, password, role]):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            register_client(name, surname, birthday, phone, email, password, role)
            messagebox.showinfo("Success", "Registration successful!")
            self.create_main_menu()  # Возврат в главное меню после успешной регистрации
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        role = self.role_combobox.get()

        if not email and not password:
            messagebox.showerror("Error", "Email and password is required!")
            return

        result, error_message = login_client(email, password, role)

        if error_message:
            messagebox.showerror("Error", error_message)
        else:
            if role == "Администратор":
                AdminWindow(self.root)
            elif role == "Клиент":
                ClientWindow(self.root, email)
            else:
                messagebox.showerror("Error", "Invalid role selected!")

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

