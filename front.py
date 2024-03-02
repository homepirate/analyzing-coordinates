import tkinter as tk
from tkinter import filedialog
import datetime

from back import start

file_A_value = ""
file_B_value = ""
number_value = ""


def browse_file_A(file):
    global file_A_value
    filename = filedialog.askopenfilename()
    file.delete(0, tk.END)
    file.insert(0, filename)
    file_A_value = filename


def browse_file_B(file):
    global file_B_value
    filename = filedialog.askopenfilename()
    file.delete(0, tk.END)
    file.insert(0, filename)
    file_B_value = filename


def save_result(entry_number, info_label):
    global number_value

    now = datetime.datetime.now()
    timestamp = now.strftime("%d-%m-%Y_%H-%M-%S")
    filename_res = filedialog.askdirectory()
    filename_res += f'/result_{timestamp}.xlsx'

    try:
        number_value = int(entry_number.get())
    except:
        info_label.config(text="Ошибка: Введите только числа")
        return

    if file_A_value and file_B_value:
        try:
            info_label.config(text="В работе", fg="green")
            start(file_A_value, file_B_value, filename_res, number_value)
            info_label.config(text="Готово!", fg="green")
        except:
            info_label.config(text="Ошибка: Возникла проблема с файлами\nФормат файлов: csv, xlsx, xls\nФормат данных в файлах: Название, координаты через запятную", fg="red")
    else:
        info_label.config(text="Выберите файл А и файл В", fg="red")


def make_window():
    # Создаем главное окно
    root = tk.Tk()
    root.geometry("600x350")
    root.resizable(width=False, height=False)
    root.title("Анализ данных")

    # Поле выбора файла А
    label_file_A = tk.Label(root, text="Файл А:")
    label_file_A.pack()
    entry_file_A = tk.Entry(root, width=50)
    entry_file_A.pack()
    btn_browse_file_A = tk.Button(root, text="Выбрать файл А", command=lambda: browse_file_A(entry_file_A))
    btn_browse_file_A.pack()

    # Поле выбора файла B
    label_file_B = tk.Label(root, text="Файл B:")
    label_file_B.pack()
    entry_file_B = tk.Entry(root, width=50)
    entry_file_B.pack()
    btn_browse_file_B = tk.Button(root, text="Выбрать файл B", command=lambda: browse_file_B(entry_file_B))
    btn_browse_file_B.pack()


    # Поле для ввода числа
    label_number = tk.Label(root, text="Введите число:")
    label_number.pack()
    entry_number = tk.Entry(root)
    entry_number.pack()


    # Кнопка для сохранения результата
    btn_save = tk.Button(root, text="Сохранить результат", command=lambda: save_result(entry_number, info_label))
    btn_save.pack()


     # Поле для вывода текста ошибок и статуса
    info_label = tk.Label(root, text="", fg="red")  # Цвет текста можно настроить на свой вкус
    info_label.pack()

    root.mainloop()
