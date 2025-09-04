import tkinter as tk
from tkinter import ttk, messagebox
from db import get_films, add_film, delete_film, update_film  # Убедитесь, что эти функции правильно импортированы

class Table(tk.Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)

        self.tree = ttk.Treeview(self, show="headings", selectmode="browse")
        self.tree["columns"] = headings
        self.tree["displaycolumns"] = headings

        for head in headings:
            self.tree.heading(head, text=head, anchor=tk.CENTER)
            self.tree.column(head, anchor=tk.CENTER)

        for row in rows:
            self.tree.insert('', tk.END, values=row)

        scrolltable = tk.Scrollbar(self, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(expand=tk.YES, fill=tk.BOTH)

        self.selection = self.tree.selection

    def get_selected_item(self):
        return self.tree.selection()[0] if self.tree.selection() else None

    def get_item_values(self):
        selected_item = self.get_selected_item()
        if selected_item:
            item = self.tree.item(selected_item)
            return item['values']
        return None


class FilmsCatalog:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Каталог фильмов")

        # Поля ввода
        self.title_var = tk.StringVar()
        self.genre_var1 = tk.StringVar()
        self.director_var1 = tk.StringVar()
        self.duration_var1 = tk.StringVar()
        self.age_limit_var1 = tk.StringVar()
        self.country_var1 = tk.StringVar()
        self.year_var = tk.StringVar()
        self.rating_var1 = tk.StringVar()

        # Создание интерфейса
        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        # Метки и поля ввода
        labels = ['Название', 'Жанр', 'Режиссер', 'Продолжительность', 'Возрастное ограничение', 'Страна', 'Рейтинг', 'Год выпуска']
        variables = [self.title_var, self.genre_var1, self.director_var1, self.duration_var1, self.age_limit_var1, self.country_var1, self.rating_var1, self.year_var]

        for i, (label, var) in enumerate(zip(labels, variables)):
            tk.Label(self.root, text=label).grid(row=i, column=0, padx=10, pady=5)
            tk.Entry(self.root, textvariable=var).grid(row=i, column=1, padx=10, pady=5)

        # Кнопки
        tk.Button(self.root, text="Добавить", command=self.do_film).grid(row=len(labels), column=0, padx=7, pady=5)
        tk.Button(self.root, text="Изменить", command=self.update_film).grid(row=len(labels), column=1, padx=7, pady=5)
        tk.Button(self.root, text="Удалить", command=self.delete_film).grid(row=len(labels), column=2, padx=7, pady=5)
        tk.Button(self.root, text="Выйти", command=self.logout).grid(row=len(labels), column=3, padx=7, pady=5)

        # Таблица для отображения фильмов
        self.table_frame = tk.Frame(self.root)
        self.table_frame.grid(row=len(labels) + 1, column=0, columnspan=3, padx=10, pady=5)
        self.table = None

    def refresh_table(self):
        # Удаляем старую таблицу, если она существует
        if self.table:
            self.table.destroy()

        data = get_films()
        self.table = Table(self.table_frame, headings=(
            'ID_фильма', 'Название', 'Жанр', 'Режиссер', 'Продолжительность', 'Возрастное ограничение', 'Страна',
            'Рейтинг', 'Год выпуска'), rows=data)
        self.table.pack(expand=tk.YES, fill=tk.BOTH)

    def do_film(self):
        name = self.title_var.get()
        genre = self.genre_var1.get()
        director = self.director_var1.get()
        duration = self.duration_var1.get()
        age_limit = self.age_limit_var1.get()
        country = self.country_var1.get()
        year_release = self.year_var.get()
        rating = self.rating_var1.get()

        if not all([name, genre, director, duration, age_limit, country, year_release, rating]):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            add_film(name, genre, director, duration, age_limit, country, year_release, rating)
            messagebox.showinfo("Успех", "Фильм добавлен!")
            self.refresh_table()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить фильм: {e}")

    def update_film(self):
        selected_item = self.table.get_selected_item()
        if not selected_item:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите фильм для обновления.")
            return

        item_values = self.table.get_item_values()
        if item_values:
            film_id = int(item_values[0])

            # Открываем новое окно для ввода данных фильма
            update_window = tk.Toplevel(self.root)
            update_window.title("Обновление фильма")

            # Создаем переменные для хранения значений из полей ввода
            self.name_var1 = tk.StringVar()
            self.genre_var1 = tk.StringVar()
            self.director_var1 = tk.StringVar()
            self.duration_var1 = tk.StringVar()
            self.age_limit_var1 = tk.StringVar()
            self.country_var1 = tk.StringVar()
            self.year_release_var1 = tk.StringVar()
            self.rating_var1 = tk.StringVar()

            # Создаем поля ввода
            tk.Label(update_window, text="Название").grid(row=0, column=0)
            tk.Entry(update_window, textvariable=self.name_var1).grid(row=0, column=1)

            tk.Label(update_window, text="Жанр").grid(row=1, column=0)
            tk.Entry(update_window, textvariable=self.genre_var1).grid(row=1, column=1)

            tk.Label(update_window, text="Режиссер").grid(row=2, column=0)
            tk.Entry(update_window, textvariable=self.director_var1).grid(row=2, column=1)

            tk.Label(update_window, text="Продолжительность").grid(row=3, column=0)
            tk.Entry(update_window, textvariable=self.duration_var1).grid(row=3, column=1)

            tk.Label(update_window, text="Возрастное ограничение").grid(row=4, column=0)
            tk.Entry(update_window, textvariable=self.age_limit_var1).grid(row=4, column=1)

            tk.Label(update_window, text="Страна").grid(row=5, column=0)
            tk.Entry(update_window, textvariable=self.country_var1).grid(row=5, column=1)

            tk.Label(update_window, text="Год выпуска").grid(row=6, column=0)
            tk.Entry(update_window, textvariable=self.year_release_var1).grid(row=6, column=1)

            tk.Label(update_window, text="Рейтинг").grid(row=7, column=0)
            tk.Entry(update_window, textvariable=self.rating_var1).grid(row=7, column=1)

            # Создаем кнопку "Изменить"
            update_button = tk.Button(update_window, text="Изменить", command=self.save_changes)
            update_button.grid(row=8, column=0, columnspan=2)

            # Заполняем поля текущими данными фильма
            self.name_var1.set(item_values[1])
            self.genre_var1.set(item_values[2])
            self.director_var1.set(item_values[3])
            self.duration_var1.set(item_values[4])
            self.age_limit_var1.set(item_values[5])
            self.country_var1.set(item_values[6])
            self.year_release_var1.set(item_values[8])
            self.rating_var1.set(item_values[7])

        else:
            messagebox.showerror("Ошибка", "Невозможно получить данные выбранного фильма.")

    def save_changes(self):
        if all([self.name_var1.get(), self.genre_var1.get(),
                self.director_var1.get(), self.duration_var1.get(),
                self.age_limit_var1.get(), self.country_var1.get(),
                self.year_release_var1.get(), self.rating_var1.get()]):
            try:
                film_id = int(self.table.get_item_values()[0])
                update_film(film_id,
                            self.name_var1.get(),
                            self.genre_var1.get(),
                            self.director_var1.get(),
                            self.duration_var1.get(),
                            self.age_limit_var1.get(),
                            self.country_var1.get(),
                            self.year_release_var1.get(),
                            self.rating_var1.get())
                messagebox.showinfo("Успех", "Фильм успешно обновлен!")

                # Обновляем таблицу в основном окне
                self.refresh_table()

                # Закрываем окно обновления
                update_window = tk.Toplevel()
                update_window.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось обновить фильм: {e}")
        else:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все обязательные поля.")
    def delete_film(self):
        selected_item = self.table.get_selected_item()
        if not selected_item:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите фильм для обновления.")
            return

        item_values = self.table.get_item_values()
        if item_values:
            try:
                film_id = int(item_values[0])
                if messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить фильм с ID {film_id}?"):
                    delete_film(film_id)
                    messagebox.showinfo("Успех", "Фильм успешно удален!")
                    self.refresh_table()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить фильм: {e}")
        else:
            messagebox.showerror("Ошибка", "Невозможно получить данные выбранного фильма.")

    def logout(self):
        self.root.destroy()
