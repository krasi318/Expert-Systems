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

# 📌 Пълния израз за Information Gain (без изчисления, с разгъване)
def information_gain_expression(data, target_attr, attribute):
    class_counts = Counter(row[target_attr] for row in data)
    total_entropy_expr = entropy_expression(class_counts, target_attr)
    total_entropy = calculate_entropy(class_counts)

    attribute_values = Counter(row[attribute] for row in data)
    subsets_expr = []
    expanded_parts = []

    for value, count in attribute_values.items():
        subset = [row for row in data if row[attribute] == value]
        subset_class_counts = Counter(row[target_attr] for row in subset)
        subset_total = sum(subset_class_counts.values())

        frac = format_fraction(count, len(data))
        inner_parts = []
        for cls, cls_count in subset_class_counts.items():
            cls_frac = format_fraction(cls_count, subset_total)
            inner_parts.append(f"-{cls_frac} log2 {cls_frac}")
        expanded_entropy_expr = " ".join(inner_parts)

        subsets_expr.append(f"{frac} * Entr({expanded_entropy_expr})")

    subsets_expr_joined = " + ".join(subsets_expr)
    ig_expr = f"IG({attribute}) = {total_entropy_expr} - ({subsets_expr_joined})"

    return ig_expr

# 📌 Намира атрибута с най-висока IG (без сметки) и показва разпределението по класове
def find_best_attribute(data, target_attr):
    attributes = [attr for attr in data[0].keys() if attr != target_attr]
    ig_expressions = {}
    ig_values = {}

    for attr in attributes:
        # Изчисляваме IG стойността за избор (не се показва)
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

    # Взимаме най-добрия атрибут
    best_attr = max(ig_values, key=ig_values.get)

    # 📌 Извеждаме изхода
    print(f"Корена на дървото ще бъде : {best_attr}\n")
    for value in sorted(set(row[best_attr] for row in data)):
        matching_classes = [row[target_attr] for row in data if row[best_attr] == value]
        joined = ",".join(matching_classes)
        print(f"{value}: {joined}")

# 📌 Данни
data = [
    {"Цвят": "червен", "Форма": "кръг", "Клас": "Да"},
    {"Цвят": "зелен", "Форма": "кръг", "Клас": "Да"},
    {"Цвят": "червен", "Форма": "триъгълник", "Клас": "Да"},
    {"Цвят": "жълт", "Форма": "кръг", "Клас": "Да"},
    {"Цвят": "зелен", "Форма": "квадрат", "Клас": "Не"},
    {"Цвят": "жълт", "Форма": "триъгълник", "Клас": "Да"},
    {"Цвят": "червен", "Форма": "квадрат", "Клас": "Да"},
    {"Цвят": "жълт", "Форма": "квадрат", "Клас": "Да"},
]

# 📌 Изпълнение
find_best_attribute(data, target_attr="Клас")
