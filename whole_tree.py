import json
from collections import Counter, defaultdict
import math
import tkinter as tk
from tkinter import scrolledtext

# 📌 Изчисляване на ентропия
def calculate_entropy(class_counts):
    total = sum(class_counts.values())
    entropy = 0
    for count in class_counts.values():
        frac = count / total
        entropy -= frac * math.log2(frac) if frac > 0 else 0
    return entropy


# 📌 Намиране на най-добрия атрибут по информация
def find_best_attribute(data, target_attr):
    attributes = [attr for attr in data[0].keys() if attr != target_attr]
    ig_values = {}

    for attr in attributes:
        # Разделяме данните по стойностите на атрибута
        attr_class_counts = defaultdict(Counter)
        for row in data:
            attr_class_counts[row[attr]][row[target_attr]] += 1

        # Изчисляваме претеглената ентропия
        weighted_entropy = 0
        total = len(data)
        for val in attr_class_counts:
            subset_total = sum(attr_class_counts[val].values())
            weighted_entropy += (subset_total / total) * calculate_entropy(attr_class_counts[val])

        # Изчисляваме общата ентропия на целевия атрибут
        total_entropy = calculate_entropy(Counter(row[target_attr] for row in data))

        # Информация на атрибута
        ig = total_entropy - weighted_entropy
        ig_values[attr] = ig

    # Връщаме атрибута с най-висока информация
    best_attr = max(ig_values, key=ig_values.get)
    return best_attr


# 📌 Извеждане на дървото на решения
def print_decision_tree(data, target_attr, depth=0, output_box=None):
    indent = "  " * depth

    # 📌 Проверка дали всички примери са от един клас
    class_counts = Counter(row[target_attr] for row in data)
    if len(class_counts) == 1:
        single_class = next(iter(class_counts))
        if output_box:
            output_box.insert(tk.END, f"{indent}Клас: {single_class}\n")
        return

    # 📌 Избор на най-добър атрибут (с най-много IG)
    best_attr = find_best_attribute(data, target_attr)

    if output_box:
        output_box.insert(tk.END, f"{indent}{best_attr}:\n")

    values = sorted(set(row[best_attr] for row in data))
    for val in values:
        if output_box:
            output_box.insert(tk.END, f"{indent}  {val} →\n")
        subset = [row for row in data if row[best_attr] == val]
        if subset:
            print_decision_tree(subset, target_attr, depth + 2, output_box=output_box)
        else:
            if output_box:
                output_box.insert(tk.END, f"{indent}    Клас: неизвестен\n")


# 📌 Данни
try:
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:
     print(f"⚠️ Грешка: {e}")


# 📌 GUI с tkinter
def show_decision_tree_gui():
    # Създаване на прозорец
    window = tk.Tk()
    window.title("Решаващо Дърво")

    # Създаване на текстово поле с възможност за превъртане
    output_box = scrolledtext.ScrolledText(window, width=80, height=20)
    output_box.pack(padx=10, pady=10)

    # Изпълнение на алгоритъма за дървото на решения
    output_box.insert(tk.END, "Решаващо дърво:\n")
    print_decision_tree(data, target_attr="bites", output_box=output_box)

    # Показване на прозореца
    window.mainloop()


# 📌 Стартиране на GUI
show_decision_tree_gui()
