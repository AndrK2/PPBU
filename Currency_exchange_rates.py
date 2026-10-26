from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
import requests
# Импорт bottle, json, pprint — не используются


def update_currency_label(event):
    code = target_combobox.get()
    name = currencies[code]
    target_label.config(text=name)


def update_base_label(event):
    code = base_combobox.get()
    name = currencies[code]
    base_label.config(text=name)


def update_second_base_label(event):
    code = second_base_combobox.get()
    name = currencies[code]
    second_base_label.config(text=name)


def exchange():
    target_code = target_combobox.get().strip()
    base_code = base_combobox.get().strip()
    second_base_code = second_base_combobox.get().strip()

    if not target_code or not base_code or not second_base_code:
        mb.showwarning('Внимание', 'Выберите все валюты')
        return

    if target_code == base_code or target_code == second_base_code:
        mb.showwarning('Внимание', 'Целевая валюта должна отличаться от базовых')
        return

    try:
        response = requests.get(f'https://open.er-api.com/v6/latest/{base_code}')
        response.raise_for_status()
        data = response.json()

        if target_code not in data['rates']:
            mb.showerror('Ошибка', f'Валюта {target_code} не найдена')
            return

        rate1 = data['rates'][target_code]
        rate2 = None

        if second_base_code != base_code:
            sec_response = requests.get(f'https://open.er-api.com/v6/latest/{second_base_code}')
            sec_response.raise_for_status()
            sec_data = sec_response.json()
            if target_code in sec_data['rates']:
                rate2 = sec_data['rates'][target_code]
            else:
                mb.showerror('Ошибка', f'Валюта {target_code} не найдена для {second_base_code}')
                return

        base1 = currencies[base_code]
        base2 = currencies[second_base_code]
        target = currencies[target_code]

        result = f'Курс обмена:\n1 {base1} = {rate1:.2f} {target}\n'
        if rate2 is not None:
            result += f'1 {base2} = {rate2:.2f} {target}'

        mb.showinfo('Курс обмена', result)

    except Exception as er:
        mb.showerror('Ошибка', er)


currencies = {
    'EUR': 'Евро',
    'USD': 'Доллар США',
    'JPY': 'Японская йена',
    'GBP': 'Фунт стерлингов',
    'AUD': 'Австралийский доллар',
    'CAD': 'Канадский доллар',
    'CHF': 'Швейцарский франк',
    'CNY': 'Китайский юань',
    'RUB': 'Российский рубль',
    'KZT': 'Казахстанский тенге',
    'UZS': 'Узбекский сум'

}

root = Tk()
root.title('Курсы обмена валют')
root.geometry('360x250')

Label(root, text='Базовая валюта').pack()
base_combobox = ttk.Combobox(root, values=list(currencies.keys()))
base_combobox.pack(pady=3, padx=10)
base_combobox.bind('<<ComboboxSelected>>', update_base_label)
base_label = ttk.Label()
base_label.pack()

Label(root, text='Вторая базовая валюта').pack()
second_base_combobox = ttk.Combobox(root, values=list(currencies.keys()))
second_base_combobox.pack(pady=3, padx=10)
second_base_combobox.bind('<<ComboboxSelected>>', update_second_base_label)
second_base_label = ttk.Label()
second_base_label.pack()

Label(root, text='Целевая валюта').pack(padx=10)
target_combobox = ttk.Combobox(root, values=list(currencies.keys()))
target_combobox.pack(pady=3, padx=10)
target_combobox.bind('<<ComboboxSelected>>', update_currency_label)

target_label = ttk.Label()
target_label.pack()

Button(text='Получить курс обмена',
       command=exchange).pack(pady=10, padx=10)


root.mainloop()