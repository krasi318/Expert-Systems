import json
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from collections import Counter

# 📌 Форматира дроб като текст
def format_fraction(numerator, denominator):
    return f"{numerator}/{denominator}"

# 📌 Генерира пълен текстов израз за ентропия
def detailed_entropy_expression(class_counts):
    total = sum(class_counts.values())
    parts = []
    for count in class_counts.values():
        frac = format_fraction(count, total)
        parts.append(f"-{frac} log2 {frac}")
    return " ".join(parts)

# 📌 Главната ентропия
def entropy_expression(class_counts, target_attr):
    total = sum(class_counts.values())
    parts = []
    for count in class_counts.values():
        frac = format_fraction(count, total)
        parts.append(f"-{frac} log2 {frac}")
    joined = " ".join(parts)
    return f"Entr({target_attr}) = {joined}"

# 📌 IG израз
def information_gain_expression(data, target_attr, attribute):
    class_counts = Counter(row[target_attr] for row in data)
    total_entropy_expr = entropy_expression(class_counts, target_attr)

    attribute_values = Counter(row[attribute] for row in data)
    subsets_expr = []
    expanded_subsets_expr = []

    for value, count in attribute_values.items():
        subset = [row for row in data if row[attribute] == value]
        subset_class_counts = Counter(row[target_attr] for row in subset)
        frac = format_fraction(count, len(data))

        fractions = [format_fraction(subset_class_counts[c], sum(subset_class_counts.values()))
                     for c in subset_class_counts.keys()]
        ent_short = f"Entr({'*'.join(fractions)})"
        subsets_expr.append(f"{frac} * {ent_short}")

        detailed_ent = detailed_entropy_expression(subset_class_counts)
        expanded_subsets_expr.append(f"{frac} * ({detailed_ent})")

    subsets_joined = " + ".join(subsets_expr)
    ig_expr = f"IG({attribute}) = {total_entropy_expr} - ({subsets_joined})"

    expanded_joined = " + ".join(expanded_subsets_expr)
    full_expr = f"{ig_expr} = {total_entropy_expr} - ({expanded_joined})"

    return full_expr

# 📌 Данни
try:
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:
    result = f"⚠️ Грешка: {e}"

# 📌 GUI логика
def run_analysis():
    selected_attr = attr_combo.get()

    if not selected_attr:
        messagebox.showerror("Грешка", "Моля избери атрибут.")
        return

    target_attr = list(data[0].keys())[-1]
    if selected_attr == target_attr:
        messagebox.showwarning("Внимание", "Избраният атрибут е същият като целевия!")
        return

    expression = information_gain_expression(data, target_attr, selected_attr)
    text_area.config(state=tk.NORMAL)
    text_area.delete("1.0", tk.END)
    text_area.insert(tk.END, expression)
    print(expression)
    text_area.config(state=tk.DISABLED)

def create_gui():
    global attr_combo, text_area

    root = tk.Tk()
    root.title("IG Израз Генератор")

    tk.Label(root, text="Избери атрибут за IG анализ (целта е последната колона):").pack(pady=5)

    attr_combo = ttk.Combobox(root, state="readonly", width=40)
    keys = list(data[0].keys())
    target = keys[-1]
    attr_combo['values'] = [key for key in keys if key != target]
    attr_combo.pack(pady=5)

    tk.Button(root, text="Генерирай израз", command=run_analysis).pack(pady=10)

    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=25)
    text_area.pack(padx=10, pady=10)
    text_area.config(state=tk.DISABLED)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
