import json
from collections import Counter
import tkinter as tk
from tkinter import messagebox

# 📌 Форматира дроб за изхода
def format_fraction(numerator, denominator):
    return f"{numerator}/{denominator}"

# 📌 Формула за ентропия като текст
def entropy_expression(class_counts, target_attr):
    total = sum(class_counts.values())
    parts = []
    for cls, count in class_counts.items():
        frac = format_fraction(count, total)
        parts.append(f"-{frac} log2 {frac}")
    joined = " ".join(parts)
    return f"Entr({target_attr}) = {joined}"

# 📌 Ентропия само като формула
def calculate_entropy(data):
    if not data or len(data) < 2:
        return "Няма достатъчно данни за изчисление."

    # Пропускаме първия ред (предполага се, че е "заглавен")
    data_without_header = data[1:]

    # Вземаме последната колона по ключ
    target_attr = list(data[0].keys())[-1]

    class_counts = Counter(row[target_attr] for row in data_without_header)
    expression = entropy_expression(class_counts, target_attr)

    summary = f"📊 Класове по {target_attr}: {dict(class_counts)}\n🎯 Ентропията на {target_attr} е:\n{expression}"
    return summary

# 📌 Интерфейс
def show_entropy_result():
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        result = calculate_entropy(data)
    except Exception as e:
        result = f"⚠️ Грешка: {e}"

    # Покажи резултата в прозорец
    window = tk.Tk()
    window.title("Ентропия")
    text = tk.Text(window, wrap="word", font=("Arial", 12))
    text.insert("1.0", result)
    text.pack(padx=20, pady=20, expand=True, fill="both")
    window.mainloop()

# 📌 Стартиране
if __name__ == "__main__":
    show_entropy_result()
