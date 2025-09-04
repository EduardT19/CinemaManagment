import tkinter as tk
from tkinter import ttk, messagebox
from Windows.films_windows import FilmsCatalog
from Windows.session_windows import SessionCatalog
from Windows.сinema_hall_windows import HallsCatalog


class AdminWindow:
    def __init__(self, root):
        self.root = tk.Toplevel()
        self.root.title("Admin Panel")
        self.root.geometry("600x400")

        self.label = ttk.Label(self.root, text="Добро пожаловать, Admin! "
                                               "Выбери таблицу для работы: ")
        self.label.pack(pady=20)

        self.films_button = ttk.Button(self.root, text="Фильмы", command=FilmsCatalog)
        self.films_button.pack(pady=10)

        self.halls_button = ttk.Button(self.root, text="Кинозалы", command=HallsCatalog)
        self.halls_button.pack(pady=10)

        self.sessons_button = ttk.Button(self.root, text="Киносеансы", command=SessionCatalog)
        self.sessons_button.pack(pady=10)

        self.logout_button = ttk.Button(self.root, text="Выйти", command=self.logout)
        self.logout_button.pack(pady=10)

    def manage_users(self):
        # Реализация управления пользователями
        messagebox.showinfo("Manage Users", "User  management functionality goes here.")

    def view_reports(self):
        # Реализация просмотра отчетов
        messagebox.showinfo("View Reports", "Report viewing functionality goes here.")

    def logout(self):
        self.root.destroy()