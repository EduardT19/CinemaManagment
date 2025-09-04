import tkinter as tk
from tkinter import ttk, messagebox
from db import get_session, add_session, delete_session, get_film_id_by_name
from Windows.films_windows import Table

class SessionCatalog:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Каталог сеансов")

        # Поля ввода
        self.film_id_var = tk.StringVar()
        self.cinema_hall_id_var = tk.StringVar()
        self.session_date_var = tk.StringVar()
        self.session_time_var = tk.StringVar()

        # Создание интерфейса
        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        # Метки и поля ввода
        labels = ['Название фильма', 'ID зала', 'Дата сеанса', 'Время сеанса']
        variables = [self.film_id_var, self.cinema_hall_id_var, self.session_date_var, self.session_time_var]

        for i, (label, var) in enumerate(zip(labels, variables)):
            tk.Label(self.root, text=label).grid(row=i, column=0, padx=10, pady=5)
            tk.Entry(self.root, textvariable=var).grid(row=i, column=1, padx=10, pady=5)

        # Кнопки
        tk.Button(self.root, text="Добавить", command=self.add_session).grid(row=len(labels), column=0, padx=7, pady=5)
        tk.Button(self.root, text="Удалить", command=self.delete_session).grid(row=len(labels), column=1, padx=7, pady=5)
        tk.Button(self.root, text="Выйти", command=self.logout).grid(row=len(labels), column=2, padx=7, pady=5)

        # Таблица для отображения сеансов
        self.table_frame = tk.Frame(self.root)
        self.table_frame.grid(row=len(labels) + 1, column=0, columnspan=3, padx=10, pady=5)
        self.table = None

    def refresh_table(self):
        if self.table:
            self.table.destroy()

        data = get_session()
        self.table = Table(self.table_frame, headings=(
            'ID сеанса', 'ID фильма', 'ID зала', 'Дата сеанса', 'Время сеанса'), rows=data)
        self.table.pack(expand=tk.YES, fill=tk.BOTH)

    def add_session(self):
        film_name = self.film_id_var.get()
        cinema_hall_id = int(self.cinema_hall_id_var.get())
        session_date = self.session_date_var.get()
        session_time = self.session_time_var.get()

        if not all([film_name, cinema_hall_id, session_date, session_time]):
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все обязательные поля!")
            return

        try:
            # Получаем ID фильма
            film_id = get_film_id_by_name(film_name)
            if not film_id:
                messagebox.showerror("Ошибка", "Фильм не найдены.")
                return

            # Добавляем сеанс в базу данных
            add_session(film_id, cinema_hall_id, session_date, session_time)
            messagebox.showinfo("Успех", "Сеанс успешно добавлен!")
            self.refresh_table()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить сеанс: {e}")

    def delete_session(self):
        selected_item = self.table.get_selected_item()
        if not selected_item:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите сеанс для удаления.")
            return

        item_values = self.table.get_item_values()
        if item_values:
            film_id = int(item_values[1])
            cinema_hall_id = int(item_values[2])

            if messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить сеанс с ID {film_id} в зале {cinema_hall_id}?"):
                try:
                    delete_session(film_id, cinema_hall_id)
                    messagebox.showinfo("Успех", "Сеанс успешно удален!")
                    self.refresh_table()
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Не удалось удалить сеанс: {e}")
        else:
            messagebox.showerror("Ошибка", "Невозможно получить данные выбранного сеанса.")

    def logout(self):
        self.root.destroy()