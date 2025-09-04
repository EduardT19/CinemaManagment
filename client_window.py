from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from db import get_films, get_session, add_ticket, get_client_id, get_client_tickets


class Table(tk.Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)

        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table["columns"] = headings
        table["displaycolumns"] = headings

        for head in headings:
            table.heading(head, text=head, anchor=tk.CENTER)
            table.column(head, anchor=tk.CENTER)

        for row in rows:
            table.insert('', tk.END, values=tuple(row))

        scrolltable = tk.Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        table.pack(expand=tk.YES, fill=tk.BOTH)

class ClientWindow:
    def __init__(self, root, email):
        self.root = tk.Toplevel()
        self.root.title("Client Panel")
        self.root.geometry("600x500")
        self.login = str(email)

        self.label = ttk.Label(self.root, text="Welcome, Client!")
        self.label.pack(pady=20)

        self.view_movies_button = ttk.Button(self.root, text="Показать фильмы", command=self.view_movies)
        self.view_movies_button.pack(pady=10)

        self.view_sessions_button = ttk.Button(self.root, text="Показать сеансы", command=self.view_sessions)
        self.view_sessions_button.pack(pady=10)

        self.book_ticket_button = ttk.Button(self.root, text="Купить билет", command=self.buy_ticket)
        self.book_ticket_button.pack(pady=10)

        self.logout_button = ttk.Button(self.root, text="Выйти", command=self.logout)
        self.logout_button.pack(pady=10)

    def view_movies(self):
        movie_window = tk.Toplevel()
        movie_window.title("Фильмы")

        self.movie_title_var = tk.StringVar()
        title_label = ttk.Label(movie_window, text="Название фильма:")
        title_label.pack(pady=5)
        title_entry = ttk.Entry(movie_window, textvariable=self.movie_title_var)
        title_entry.pack(pady=5)

        self.sort_var = tk.StringVar()
        sort_label = ttk.Label(movie_window, text="Сортировать по:")
        sort_label.pack(pady=5)
        sort_options = ["name", "genre", "film_director", "year_release", "rating"]
        sort_combobox = ttk.Combobox(movie_window, textvariable=self.sort_var, values=sort_options)
        sort_combobox.pack(pady=5)

        search_button = ttk.Button(movie_window, text="Поиск", command=self.search_movies)
        search_button.pack(pady=10)

        data = get_films()
        self.table = Table(movie_window, headings=(
            'ID_фильма', 'Название', 'Жанр', 'Режиссер', 'Продолжительность', 'Возрастное ограничение', 'Страна',
            'Рейтинг', 'Год выпуска'), rows=data)
        self.table.pack(expand=tk.YES,fill=tk.BOTH)

    def search_movies(self):
        title = self.movie_title_var.get()
        sort_by = self.sort_var.get()

        data = get_films(title=title, sort_by=sort_by)
        if not data:
            messagebox.showinfo("Результаты поиска", "Фильмы не найдены.")
            return

        if hasattr(self, 'table'):
            self.table.destroy()

        # Создаем новую таблицу с отфильтрованными данными
        self.table = Table(self.table.master, headings=(
            'ID_фильма', 'Название', 'Жанр', 'Режиссер', 'Продолжительность', 'Возрастное ограничение', 'Страна',
            'Рейтинг', 'Год выпуска' ), rows=data)
        self.table.pack(expand=tk.YES, fill=tk.BOTH)

    def view_sessions(self):
        session_window = tk.Toplevel()
        session_window.title("Киносеансы")

        self.session_film_var = tk.StringVar()
        film_label = ttk.Label(session_window, text="Фильм сеанса:")
        film_label.pack(pady=5)
        film_entry = ttk.Entry(session_window, textvariable=self.session_film_var)
        film_entry.pack(pady=5)

        self.session_date_var = tk.StringVar()
        date_label = ttk.Label(session_window, text="Дата начала сеанса:")
        date_label.pack(pady=5)
        time_entry = ttk.Entry(session_window, textvariable=self.session_date_var)
        time_entry.pack(pady=5)

        self.sort_session_var = tk.StringVar()
        sort_label = ttk.Label(session_window, text="Сортировать по:")
        sort_label.pack(pady=5)
        sort_options = ["session_time", "session_date", "cinema_hall_id"]
        sort_combobox = ttk.Combobox(session_window, textvariable=self.sort_session_var, values=sort_options)
        sort_combobox.pack(pady=5)

        search_button = ttk.Button(session_window, text="Поиск", command=self.search_sessions)
        search_button.pack(pady=10)

        data = get_session()  # Получаем все сеансы
        self.table = Table(session_window, headings=(
            "ID_сеанса", "ID_фильма", "ID_зала", "время_начала", "дата"), rows=data)
        self.table.pack(expand=tk.YES, fill=tk.BOTH)

    def search_sessions(self):
        film_id = self.session_film_var.get()
        date = self.session_date_var.get()
        sort_by = self.sort_session_var.get()

        data = get_session(film_id=film_id, date=date, sort_by=sort_by)
        if not data:
            messagebox.showinfo("Результаты поиска", "Сеансы не найдены.")
            return

        if hasattr(self, 'table'):
            self.table.destroy()

        # Создаем новую таблицу с отфильтрованными данными
        self.table = Table(self.table.master, headings=(
            "ID_сеанса", "ID_фильма", "время_начала", "дата", "ID_зала"), rows=data)
        self.table.pack(expand=tk.YES, fill=tk.BOTH)

    def buy_ticket(self):
        def submit_ticket():
            try:
                price = float(price_entry.get())
                seat = seat_entry.get()
                film_session_id = int(film_session_id_entry.get())
                purchase_date = datetime.now().strftime('%Y-%m-%d')
                client_id = get_client_id(self.login)
                # Добавляем билет в базу данных
                add_ticket(price, seat, film_session_id, purchase_date, client_id)

                # Получаем данные о билетах клиента
                tickets_data = get_client_tickets(client_id)

                # Создаем таблицу
                tickets_table = Table(ticket_window, headings=(
                    'ID_билета', 'Цена', 'Место', 'ID_сеанса', 'Дата покупки', 'Имя покупателя'), rows=tickets_data)

                # Размещаем таблицу в окне
                tickets_table.pack(expand=tk.YES, fill=tk.BOTH)

            except ValueError as e:
                messagebox.showerror("Ошибка", f"Пожалуйсто, проверьте правильность введенных данных: {e}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Произошла ошибка при добавлении билета: {e}")

        # Создание окна для ввода данных билета
        ticket_window = tk.Toplevel()
        ticket_window.title("Покупка билета")


        price_label = ttk.Label(ticket_window, text="Цена:")
        price_label.pack()
        price_entry = ttk.Entry(ticket_window)
        price_entry.pack(pady=5)

        seat_label = ttk.Label(ticket_window, text="Место:")
        seat_label.pack()
        seat_entry = ttk.Entry(ticket_window)
        seat_entry.pack(pady=5)

        film_session_id_label = ttk.Label(ticket_window, text="ID сессии:")
        film_session_id_label.pack()
        film_session_id_entry = ttk.Entry(ticket_window)
        film_session_id_entry.pack(pady=5)

        submit_button = ttk.Button(ticket_window, text="Купить билет", command=submit_ticket)
        submit_button.pack(pady=10)

    def logout(self):
        self.root.destroy()
