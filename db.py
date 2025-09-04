from datetime import datetime

import psycopg2
from psycopg2 import sql, Error


def connect_db():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="edvard19",
        host="localhost",
        port="5432"
    )
    return conn

def register_client(name, surname, birthday,phone_number, email, password, role):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO client (name, surname, birthday,phone_number, email, role, password) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (name, surname, birthday,phone_number, email, role, password)
    )
    conn.commit()
    cursor.close()
    conn.close()

def login_client(email, password, role):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM client WHERE email = %s AND password = %s AND role = %s", (email, password, role))
    client = cursor.fetchone()
    cursor.close()
    conn.close()

    # Проверяем, соответствует ли роль ожидаемой роли
    expected_roles = ['Администратор', 'Клиент']
    if role not in expected_roles:
        return None, "Invalid role selected!"
    if not client:
        return None, "Проверьте все поля, возможно смените роль !"
    return client, None

def get_client_id(email):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM client WHERE email = %s", (email,))  # Передаем email как кортеж
    client_id = cursor.fetchone()
    cursor.close()
    conn.close()
    # Проверяем, что client_id не None и возвращаем только id
    return client_id[0] if client_id else None

def get_client_tickets(client_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT t.id, t.price, t.seat, t.film_session_id, t.purchase_date, client.name FROM ticket t INNER JOIN "
                   f"client ON t.client_id = client.id  WHERE t.client_id = {client_id}")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_films(title=None, sort_by=None):
    conn = connect_db()
    if conn:
        try:
            query = "SELECT * FROM films f"
            params = []
            if title:
                query += " WHERE f.name LIKE %s"
                params.append(f"{title}")
            # Сортировка
            if sort_by:
                query += f" ORDER BY {sort_by} ASC"

            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except Error as e:
            print(f"Ошибка при получении списка фильмов: {e}")
        finally:
            conn.close()
    return []

def get_session(film_id=None, date=None, sort_by=None):
    conn = connect_db()
    if conn:
        try:
            query = "SELECT * FROM film_session fs"
            params = []
            if film_id:
                query += " WHERE fs.film_id = %s"
                params.append(film_id)
            if date:
                query += " AND fs.session_date = %s" if film_id else " WHERE fs.session_date = %s"
                params.append(date)
            # Сортировка
            if sort_by:
                query += f" ORDER BY {sort_by} ASC"

            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except Error as e:
            print(f"Ошибка при получении списка сеансов: {e}")
        finally:
            conn.close()
    return []

def get_cinema_hall():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cinema_halls")
    halls = cursor.fetchall()
    cursor.close()
    conn.close()
    return halls

def get_film_id_by_name(film_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM films WHERE name = %s", (film_name,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0]  if result else None

def update_film(film_id, title, genre, director, duration, age_limit, country, year_release, rating):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        # Обновляем все поля фильма
        cursor.execute("""
                UPDATE films
                SET name = %s, genre = %s, film_director = %s, duration = %s,
                    age_limit = %s, country = %s, rating = %s, year_release = %s
                WHERE id = %s
            """, (title, genre, director, duration, age_limit, country, rating, year_release, film_id))

        conn.commit()
        print(f"Фильм с ID {film_id} успешно обновлен.")
    except Exception as e:
        print(f"Ошибка при обновлении фильма: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def update_cinema_hall(cinema_hall_id, number_seats, type_hall):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        # Обновляем все поля фильма
        cursor.execute("""
                    UPDATE cinema_halls SET number_seats = %s, type_hall = %s
                    WHERE id = %s
                """, (number_seats, type_hall, cinema_hall_id))

        conn.commit()
        print(f"Зал с ID {cinema_hall_id} успешно обновлен.")
    except Exception as e:
        print(f"Ошибка при обновлении зала: {e}")
        conn.rollback()
    finally:
        cursor.close()

def add_film(name: str, genre, director, duration, age_limit, country, year_release, rating):
    # Логика добавления фильма в базу данных
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO films (name, genre, film_director, duration, age_limit, country, rating, year_release) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (name, genre, director, duration, age_limit, country, rating, year_release))
    conn.commit()
    cursor.close()
    conn.close()

def add_session(film_id: int, cinema_hall_id: int, session_date: str, session_time: str):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO film_session (film_id, cinema_hall_id, session_date, session_time)
            VALUES (%s, %s, %s, %s)
        """, (film_id, cinema_hall_id, session_date, session_time))

        conn.commit()
        print(f"Сеанс с ID {film_id} в зале {cinema_hall_id} успешно добавлен.")
    except Exception as e:
        print(f"Ошибка при добавлении сеанса: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def add_cinema_hall(number_seats, type_hall):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
                INSERT INTO cinema_halls (number_seats, type_hall)
                VALUES (%s, %s)
            """, (number_seats, type_hall))
        conn.commit()
        print("Кинозал успешно добавлен.")
    except Exception as e:
        print(f"Ошибка при добавлении кинозала: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def delete_session(film_id, cinema_hall_id):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM film_session WHERE film_id = %s AND cinema_hall_id = %s",
                       (film_id, cinema_hall_id))
        if cursor.rowcount > 0:
            conn.commit()
            print(f"Сеанс с ID {film_id} в зале {cinema_hall_id} успешно удален.")
        else:
            print(f"Сеанс с ID {film_id} в зале {cinema_hall_id} не найден для удаления.")
    except Exception as e:
        print(f"Ошибка при удалении сеанса: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def delete_cinema_hall(cinema_hall_id):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(f"DELETE FROM cinema_halls WHERE id = {cinema_hall_id}")
        if cursor.rowcount > 0:
            conn.commit()
            print(f"Зал с id {cinema_hall_id} успешно удален.")
        else:
            print(f"Зал с ID {cinema_hall_id} не найден для удаления.")
    except Exception as e:
        print(f"Ошибка при удалении сеанса: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def delete_film(film_id):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM films WHERE id = %s", (film_id,))

        if cursor.rowcount > 0:
            conn.commit()
            print(f"Фильм с ID {film_id} успешно удален.")
        else:
            print(f"Фильм с ID {film_id} не найден для удаления.")
    except Exception as e:
        print(f"Ошибка при удалении фильма: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def add_ticket(price, seat, film_session_id, purchase_date, client_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO ticket (price, seat, film_session_id, purchase_date, client_id) VALUES (%s, %s, %s, %s, %s)",
        (price, seat, film_session_id, purchase_date, client_id)
    )
    conn.commit()
    cursor.close()
    conn.close()



