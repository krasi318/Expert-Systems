import json

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from collections import Counter, defaultdict
import math

# 📌 Форматира дроб за изхода
def format_fraction(numerator, denominator):
    return f"{numerator}/{denominator}"

# 📌 Формула за ентропия като текст (без сметки)
def entropy_expression(class_counts, target_attr):
    total = sum(class_counts.values())
    parts = []
    for cls, count in class_counts.items():
        frac = format_fraction(count, total)
        parts.append(f"-{frac} log2 {frac}")
    joined = " ".join(parts)
    return f"Entr({target_attr}) = {joined}"

# 📌 Функция за изчисляване на ентропия
def calculate_entropy(class_counts):
    total = sum(class_counts.values())
    entropy = 0
    for count in class_counts.values():
        frac = count / total
        entropy -= frac * math.log2(frac) if frac > 0 else 0
    return entropy

# 📌 Намира атрибута с най-висока IG
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
    return best_attr

# 📌 Рисуваме дървото
def draw_decision_tree(data, target_attr):
    best_attr = find_best_attribute(data, target_attr)

    # Създаване на фигура и оси
    fig, ax = plt.subplots(figsize=(8, 6))

    # Създаване на кръгче за корена
    circle = patches.Circle((0.5, 0.8), 0.1, edgecolor='black', facecolor='lightblue', lw=2)
    ax.add_patch(circle)
    ax.text(0.5, 0.8, best_attr, horizontalalignment='center', verticalalignment='center', fontsize=12, color='black')

    # Получаваме възможните стойности на атрибута
    attribute_values = sorted(set(row[best_attr] for row in data))

    # Стрелки и таблици за всяка стойност на атрибута
    x_offset = 0.2
    for i, value in enumerate(attribute_values):
        # Добавяме стрелка
        ax.annotate('', xy=(x_offset + i*0.6, 0.6), xytext=(0.5, 0.7), arrowprops=dict(facecolor='black', shrink=0.05))

        # Изчисляваме класовете за текущата стойност
        matching_classes = [row[target_attr] for row in data if row[best_attr] == value]
        class_counts = Counter(matching_classes)
        class_labels = '\n'.join(f"{label}: {count}" for label, count in class_counts.items())

        # Пишем текста за стойността
        ax.text(x_offset + i*0.6, 0.6, value, horizontalalignment='center', verticalalignment='center', fontsize=10, color='black')

        # Добавяме таблицата за текущата стойност
        ax.add_patch(patches.Rectangle((x_offset + i*0.6 - 0.1, 0.4), 0.2, 0.2, linewidth=1, edgecolor='black', facecolor='lightgray'))
        ax.text(x_offset + i*0.6, 0.5, class_labels, horizontalalignment='center', verticalalignment='center', fontsize=10, color='black')

    # Настройки за графиката
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')

    # Показваме графиката
    plt.show()

# 📌 Данни
try:
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:
    result = f"⚠️ Грешка: {e}"

# 📌 Изпълнение
draw_decision_tree(data, target_attr="bites")

# 📌 Принтиране на текстовото изражение
best_attr = find_best_attribute(data, target_attr="bites")
print(f"Най-добрият атрибут: {best_attr}")
