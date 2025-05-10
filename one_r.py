import json
from collections import defaultdict, Counter
import tkinter as tk
from tkinter import scrolledtext

def load_data():
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def train_one_r_verbose(data, target):
    attributes = [key for key in data[0] if key != target]
    best_attr = None
    best_rules = {}
    lowest_error = float('inf')

    full_log = ""

    for attr in attributes:
        full_log += f"\n📂 Анализ на атрибута: {attr}\n"
        rules = {}
        error = 0
        grouped = defaultdict(list)

        for row in data:
            grouped[row[attr]].append(row[target])

        for val, targets in grouped.items():
            counter = Counter(targets)
            most_common, count = counter.most_common(1)[0]
            total = len(targets)
            errors = total - count
            rules[val] = most_common
            error += errors

            full_log += f" - {val}: {most_common} -> {errors}/{total} грешки\n"

        full_log += f" 🧮 Общо грешки за {attr}: {error}\n"

        if error < lowest_error:
            lowest_error = error
            best_attr = attr
            best_rules = rules

    full_log += f"\n✅ Най-добър атрибут според OneR:\n"
    full_log += f" 👉 {best_attr} с {lowest_error} общи грешки\n"
    full_log += f"📜 Генерирани правила:\n"
    for val, pred in best_rules.items():
        full_log += f" - Ако {best_attr} = {val}, тогава {target} = {pred}\n"

    return best_attr, best_rules, full_log

def display_results(log):
    # Създаване на графичен прозорец
    root = tk.Tk()
    root.title("Резултати от OneR")

    # Добавяне на скролваща текстова област
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=30)
    text_area.grid(row=0, column=0, padx=10, pady=10)
    text_area.insert(tk.END, log)
    text_area.config(state=tk.DISABLED)

    # Запуск на GUI
    root.mainloop()

def main():
    try:
        data = load_data()
        target = list(data[0].keys())[-1]  # Вземаме последния ключ като целева променлива

        best_attr, best_rules, log = train_one_r_verbose(data, target)

        # Показване на резултатите в GUI прозорец
        display_results(log)

    except Exception as e:
        print(f"⚠️ Възникна грешка:\n{e}")

if __name__ == "__main__":
    main()
