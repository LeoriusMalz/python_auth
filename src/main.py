#!/usr/bin/env python3
"""
@file main.py
@brief Простое приложение аутентификации с GUI на tkinter
@author vovuas2003
@date 2026
@version 1.0

@details
Приложение предоставляет простой интерфейс для аутентификации пользователей.
Поддерживает два режима: отладочный (с консолью) и релизный (только GUI).
Хранит пароли в виде SHA-256 хешей для безопасности.

@section features Основные функции
- Графический интерфейс на tkinter
- Хеширование паролей алгоритмом SHA-256
- Ограничение количества попыток входа
- Два режима работы: debug и release
- Валидация ввода пользователя

@section usage Использование
Запустите приложение и введите логин/пароль.
В отладочном режиме видны дополнительные сообщения в консоли.

@note В отладочном режиме пароли выводятся в консоль для тестирования!
"""

import tkinter as tk
from hashlib import sha256

# @var DEBUG
# @brief Флаг отладочного режима
# @details True - отладочный режим (с консолью), False - релизный режим
DEBUG = False

# @var START_ATTEMPTS
# @brief Начальное количество попыток входа
# @details Минимальное значение: 1, максимальное: 10 (см. build.sh)
START_ATTEMPTS = 3

# @var ATTEMPTS
# @brief Текущее количество оставшихся попыток
# @details Уменьшается при каждой неудачной попытке входа
ATTEMPTS = START_ATTEMPTS

# @var DATABASE
# @brief Словарь для хранения пользователей и их хешированных паролей
# @details Ключ - логин, значение - SHA-256 хеш пароля
DATABASE = dict()


def myhash(s):
    """
    @brief Вычисляет SHA-256 хеш строки
    @param s Входная строка для хеширования
    @return HEX-строка с хешем длиной 64 символа

    @details
    Функция использует стандартную библиотеку hashlib.
    Хеш возвращается в шестнадцатеричном формате.
    """
    return sha256(s.encode('utf-8')).hexdigest()


# Инициализация базы данных в зависимости от режима
if DEBUG:
    # @var title
    # @brief Заголовок окна в отладочном режиме
    title = "Версия для отладки"
    print(title)
    DATABASE["root"] = myhash("toor")
    DATABASE["user"] = myhash("1234")
    print(f"DATABASE = {DATABASE}")
else:
    # @var title
    # @brief Заголовок окна в релизном режиме
    title = "Релизная версия"
    DATABASE["admin"] = ("a35c5f63916fff41369754c7a01cc4a8"
                         "2e9e3e5f1e05628791b5f5770435d6b0")  # @dm1n
    DATABASE["vovuas"] = ("77459b9b941bcb4714d0c121313c900e"
                          "cf30541d158eb2b9b178cdb8eca6457e")  # 2003

# @var window
# @brief Главное окно приложения
window = tk.Tk()
window.title(title)

# @var frame_buttons
# @brief Фрейм для размещения кнопок
frame_buttons = tk.Frame(window)
frame_buttons.pack(side=tk.TOP,
                   fill=tk.X)


def mymessagebox(fontsize, butsize, mytitle, mytext):
    """
    @brief Создает всплывающее окно с сообщением
    @param fontsize Размер шрифта текста сообщения
    @param butsize Размер шрифта кнопки
    @param mytitle Заголовок окна
    @param mytext Текст сообщения

    @details
    Создает модальное окно с текстом сообщения и кнопкой "Закрыть".
    Окно позиционируется относительно главного окна приложения.
    """
    toplevel = tk.Toplevel(window)
    toplevel.title(mytitle)
    toplevel.geometry(f"180x120+{window.winfo_x()+8}+{window.winfo_y()+3}")
    toplevel.resizable(False, False)
    lab = tk.Label(toplevel,
                   text=mytext,
                   font=("TkDefaultFont", fontsize))
    lab.pack()
    b = tk.Button(toplevel,
                  text="Закрыть",
                  command=toplevel.destroy,
                  width=10,
                  font=("TkDefaultFont", butsize))
    b.pack()


def show_error():
    """
    @brief Показывает окно с сообщением об ошибке
    @details Используется для обработки непредвиденных исключений
    """
    mymessagebox(12, 12, "Ошибка!", "Что-то пошло\nне так.")


def show_good_login():
    """
    @brief Показывает окно успешной аутентификации
    @details Вызывается при корректном вводе логина и пароля
    """
    mymessagebox(15, 15, "Успех!", "Доступ\nразрешён!")


def show_bad_login():
    """
    @brief Показывает окно неудачной аутентификации
    @details Вызывается при неверном логине/пароле или исчерпании попыток
    """
    mymessagebox(15, 15, "Неудача!", "Доступ\nзапрещён!")


def login():
    """
    @brief Выполняет аутентификацию пользователя
    @details Проверяет логин и пароль, управляет количеством попыток

    @par Алгоритм работы:
    1. Получает логин и пароль из полей ввода
    2. Хеширует пароль
    3. Проверяет наличие логина в базе данных
    4. Сравнивает хеши паролей
    5. Обрабатывает результат с учетом оставшихся попыток

    @note В отладочном режиме выводит подробную информацию в
    консоль, а также восстанавливает количество доступных попыток
    """
    global ATTEMPTS
    login = entry0.get()
    password = entry1.get()
    p_hash = myhash(password)
    if DEBUG:
        print(f"login = {login}, password = {password}, hash = {p_hash}")
    res = False
    reason = "login found and hash is right"
    try:
        real_hash = DATABASE[login]
        if p_hash != real_hash:
            reason = f"wrong password hash and right = {real_hash}"
        else:
            res = True
    except KeyError as e:
        if DEBUG:
            print(f"database KeyError, key {e} not found")
        reason = "login not found in database"
    except Exception:
        if DEBUG:
            print("Unexpected exception during login!")
        raise
    if ATTEMPTS == 0:
        if DEBUG:
            print(f"ATTEMPTS == 0, real result of auth = {res}, "
                  f"reason = {reason};"
                  f"ATTEMPTS = {START_ATTEMPTS} (refreshing)")
            ATTEMPTS = START_ATTEMPTS
        show_bad_login()
    else:
        if res:
            if DEBUG:
                print(f"good auth, reason = {reason}")
            show_good_login()
        else:
            ATTEMPTS -= 1
            if DEBUG:
                print(f"bad auth, reason = {reason}")
            show_bad_login()


def clear_fields():
    """
    @brief Очищает поля ввода логина и пароля
    """
    entry0.delete(0, tk.END)
    entry1.delete(0, tk.END)


def show_help():
    """
    @brief Показывает окно с помощью
    @details Отображает инструкцию по
    использованию и количество оставшихся попыток
    """
    mymessagebox(11,
                 11,
                 "Помощь",
                 f"Первая строка - логин,"
                 f"\nвторая строка - пароль."
                 f"\nОсталось попыток: {ATTEMPTS}.")


def button0_click():
    """
    @brief Обработчик нажатия кнопки "войти"
    @details Вызывает функцию login() с обработкой исключений
    """
    try:
        login()
    except Exception as e:
        if DEBUG:
            print(f"button0_click error:\n{e}")
        show_error()


def button1_click():
    """
    @brief Обработчик нажатия кнопки "очистка полей"
    @details Вызывает функцию clear_fields() с обработкой исключений
    """
    try:
        clear_fields()
    except Exception as e:
        if DEBUG:
            print(f"button1_click error:\n{e}")
        show_error()


def button2_click():
    """
    @brief Обработчик нажатия кнопки "помощь"
    @details Вызывает функцию show_help() с обработкой исключений
    """
    try:
        show_help()
    except Exception as e:
        if DEBUG:
            print(f"button2_click error:\n{e}")
        show_error()


# @var buttons
# @brief Список кнопок интерфейса
buttons = []

# @var but_names
# @brief Тексты для кнопок интерфейса
but_names = ["    войти    ", "    очистка полей    ", "    помощь    "]

# @var but_com
# @brief Список функций-обработчиков для кнопок
but_com = [button0_click, button1_click, button2_click]

# Создание и размещение кнопок
for i in range(3):
    buttons.append(tk.Button(frame_buttons,
                             text=but_names[i],
                             command=but_com[i]))

for button in buttons:
    button.pack(side=tk.LEFT)

# @var entry0
# @brief Поле ввода для логина
entry0 = tk.Entry(window,
                  width=30)

# @var entry1
# @brief Поле ввода для пароля (замена символов на звёздочки)
entry1 = tk.Entry(window,
                  width=30,
                  show="*")

entry0.pack()
entry1.pack()

window.resizable(False, False)
window.mainloop()
