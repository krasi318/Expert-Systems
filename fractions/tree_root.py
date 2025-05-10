from collections import Counter, defaultdict
import math
import tkinter as tk
from tkinter import ttk, scrolledtext

def format_fraction(numerator, denominator):
    return f"{numerator}/{denominator}"

def entropy_expression(class_counts, target_attr):
    total = sum(class_counts.values())
    parts = []
    for cls, count in class_counts.items():
        frac = format_fraction(count, total)
        parts.append(f"-{frac} log2 {frac}")
    joined = " ".join(parts)
    return f"Entr({target_attr}) = {joined}"

def calculate_entropy(class_counts):
    total = sum(class_counts.values())
    entropy = 0
    for count in class_counts.values():
        frac = count / total
        entropy -= frac * math.log2(frac) if frac > 0 else 0
    return entropy

def find_best_attribute(data, target_attr):
    attributes = [attr for attr in data[0].keys() if attr != target_attr]
    ig_values = {}

    for attr in attributes:
        attr_class_counts = defaultdict(Counter)
        for row in data:
            attr_class_counts[row[attr]][row[target_attr]] += 1
        weighted_entropy = 0
        total = len(data)
        for val in attr_class_counts:
            subset_total = sum(attr_class_counts[val].values())
            weighted_entropy += (subset_total / total) * calculate_entropy(attr_class_counts[val])
        total_entropy = calculate_entropy(Counter(row[target_attr] for row in data))
        ig = total_entropy - weighted_entropy
        ig_values[attr] = ig

    best_attr = max(ig_values, key=ig_values.get)

    output = f"Корена на дървото ще бъде : {best_attr}\n\n"
    for value in sorted(set(row[best_attr] for row in data)):
        matching_classes = [row[target_attr] for row in data if row[best_attr] == value]
        joined = ",".join(matching_classes)
        output += f"{value}: {joined}\n"
    return output

# 📌 Данни
data = [
  {"heavy": "no", "smelly": "no", "big": "no", "growling": "no", "bites": "no"},
  {"heavy": "no", "smelly": "no", "big": "yes", "growling": "no", "bites": "no"},
  {"heavy": "yes", "smelly": "yes", "big": "no", "growling": "yes", "bites": "no"},
  {"heavy": "yes", "smelly": "no", "big": "no", "growling": "yes", "bites": "yes"},
  {"heavy": "no", "smelly": "yes", "big": "yes", "growling": "no", "bites": "yes"},
  {"heavy": "no", "smelly": "no", "big": "yes", "growling": "yes", "bites": "yes"},
  {"heavy": "no", "smelly": "no", "big": "no", "growling": "yes", "bites": "yes"},
  {"heavy": "yes", "smelly": "yes", "big": "no", "growling": "no", "bites": "yes"}
]

# 📌 Създаване на GUI
def run_gui():
    root = tk.Tk()
    root.title("Откриване на корен на дърво (Information Gain)")

    label = ttk.Label(root, text="Резултат:")
    label.pack(padx=10, pady=(10, 0))

    output_text = scrolledtext.ScrolledText(root, width=60, height=15, font=("Courier", 10))
    output_text.pack(padx=10, pady=10)

    result = find_best_attribute(data, target_attr="bites")
    output_text.insert(tk.END, result)
    output_text.configure(state='disabled')  # само за четене

    root.mainloop()

# 📌 Стартиране на GUI
run_gui()
