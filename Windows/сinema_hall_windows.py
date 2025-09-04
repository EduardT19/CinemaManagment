import tkinter as tk
from tkinter import ttk, messagebox

from Windows.films_windows import Table
from db import get_cinema_hall, add_cinema_hall, delete_cinema_hall, update_cinema_hall

class HallsCatalog:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Каталог залов")

        # Поля ввода
        self.number_seats_var = tk.StringVar()
        self.type_hall_var = tk.StringVar()

        # Создание интерфейса
        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        # Метки и поля ввода
        labels = ['Количество мест', 'Тип зала']
        variables = [self.number_seats_var, self.type_hall_var]

        for i, (label, var) in enumerate(zip(labels, variables)):
            tk.Label(self.root, text=label).grid(row=i, column=0, padx=10, pady=5)
            tk.Entry(self.root, textvariable=var).grid(row=i, column=1, padx=10, pady=5)

        # Кнопки
        tk.Button(self.root, text="Добавить", command=self.add_cinema_hall).grid(row=len(labels), column=0, padx=7, pady=5)
        tk.Button(self.root, text="Обновить", command=self.update_cinema_hall).grid(row=len(labels), column=1, padx=7, pady=5)
        tk.Button(self.root, text="Удалить", command=self.delete_cinema_hall).grid(row=len(labels), column=2, padx=7, pady=5)
        tk.Button(self.root, text="Выйти", command=self.logout).grid(row=len(labels), column=3, padx=7, pady=5)

        # Таблица для отображения залов
        self.table_frame = tk.Frame(self.root)
        self.table_frame.grid(row=len(labels) + 1, column=0, columnspan=3, padx=10, pady=5)
        self.table = None

    def refresh_table(self):
        if self.table:
            self.table.destroy()

        data = get_cinema_hall()
        self.table = Table(self.table_frame, headings=(
            'ID', 'Количество мест', 'Тип зала'), rows=data)
        self.table.pack(expand=tk.YES, fill=tk.BOTH)

    def add_cinema_hall(self):
        number_seats = self.number_seats_var.get()
        type_hall = self.type_hall_var.get()

        if not all([number_seats, type_hall]):
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все обязательные поля!")
            return

        try:
            add_cinema_hall(int(number_seats), type_hall)
            messagebox.showinfo("Успех", "Зал успешно добавлен!")
            self.refresh_table()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить зал: {e}")

    def update_cinema_hall(self):
        selected_item = self.table.get_selected_item()
        if not selected_item:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите зал для обновления.")
            return

        item_values = self.table.get_item_values()
        if item_values:
            number_seats = item_values[1]
            type_hall = item_values[2]

            # Открываем новое окно для ввода данных зала
            update_window = tk.Toplevel(self.root)
            update_window.title("Обновление зала")

            # Создаем переменные для хранения значений из полей ввода
            self.number_seats_var_update = tk.StringVar()
            self.type_hall_var_update = tk.StringVar()

            tk.Label(update_window, text="Количество мест").grid(row=1, column=0)
            tk.Entry(update_window, textvariable=self.number_seats_var_update).grid(row=1, column=1)

            tk.Label(update_window, text="Тип зала").grid(row=2, column=0)
            tk.Entry(update_window, textvariable=self.type_hall_var_update).grid(row=2, column=1)

            # Создаем кнопку "Изменить"
            update_button = tk.Button(update_window, text="Изменить", command=self.save_changes)
            update_button.grid(row=3, column=0, columnspan=2)

            # Заполняем поля текущими данными зала
            self.number_seats_var_update.set(number_seats)
            self.type_hall_var_update.set(type_hall)

        else:
            messagebox.showerror("Ошибка", "Невозможно получить данные выбранного зала.")

    def save_changes(self):
        if all([self.number_seats_var_update.get(),
                self.type_hall_var_update.get()]):
            try:
                cinema_hall_id = self.table.get_item_values()[0]
                number_seats = self.number_seats_var_update.get()
                type_hall = self.type_hall_var_update.get()

                update_cinema_hall(cinema_hall_id, number_seats, type_hall)
                messagebox.showinfo("Успех", "Зал успешно обновлен!")

                # Обновляем таблицу в основном окне
                self.refresh_table()

                # Закрываем окно обновления
                update_window = tk.Toplevel()
                update_window.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось обновить зал: {e}")
        else:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все обязательные поля.")

    def delete_cinema_hall(self):
        selected_item = self.table.get_selected_item()
        if not selected_item:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите зал для удаления.")
            return

        item_values = self.table.get_item_values()
        if item_values:
            cinema_hall_id = int(item_values[0])

            if messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить зал с ID {cinema_hall_id} ?"):
                try:
                    delete_cinema_hall(cinema_hall_id)
                    messagebox.showinfo("Успех", "Зал успешно удален!")
                    self.refresh_table()
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Не удалось удалить зал: {e}")
        else:
            messagebox.showerror("Ошибка", "Невозможно получить данные выбранного зала.")

    def logout(self):
        self.root.destroy()