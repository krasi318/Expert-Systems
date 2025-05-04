from collections import Counter

# 📌 Форматира дроб като текст
def format_fraction(numerator, denominator):
    return f"{numerator}/{denominator}"

# 📌 Генерира пълен текстов израз за ентропия (напр. -3/4 log2 3/4 -1/4 log2 1/4)
def detailed_entropy_expression(class_counts):
    total = sum(class_counts.values())
    parts = []
    for count in class_counts.values():
        frac = format_fraction(count, total)
        parts.append(f"-{frac} log2 {frac}")
    return " ".join(parts)

# 📌 Генерира главния израз за ентропия Entr(Клас)
def entropy_expression(class_counts, target_attr):
    total = sum(class_counts.values())
    parts = []
    for count in class_counts.values():
        frac = format_fraction(count, total)
        parts.append(f"-{frac} log2 {frac}")
    joined = " ".join(parts)
    return f"Entr({target_attr}) = {joined}"

# 📌 Основна функция за израза за Information Gain
def information_gain_expression(data, target_attr, attribute):
    # 1. Главната ентропия
    class_counts = Counter(row[target_attr] for row in data)
    total_entropy_expr = entropy_expression(class_counts, target_attr)

    # 2. Частите за IG
    attribute_values = Counter(row[attribute] for row in data)
    subsets_expr = []          # Изрази с Entr(...)
    expanded_subsets_expr = [] # Същите, но с разширена ентропия

    for value, count in attribute_values.items():
        subset = [row for row in data if row[attribute] == value]
        subset_class_counts = Counter(row[target_attr] for row in subset)
        frac = format_fraction(count, len(data))

        # Ентропия като съкратен израз
        ent_short = f"Entr({format_fraction(subset_class_counts.get('Да', 0), sum(subset_class_counts.values()))}*{format_fraction(subset_class_counts.get('Не', 0), sum(subset_class_counts.values()))})"
        subsets_expr.append(f"{frac} * {ent_short}")

        # Ентропия като разгърнат израз
        detailed_ent = detailed_entropy_expression(subset_class_counts)
        expanded_subsets_expr.append(f"{frac} * ({detailed_ent})")

    # 3. IG израз – първо кратък
    subsets_joined = " + ".join(subsets_expr)
    ig_expr = f"IG({attribute}) = {total_entropy_expr} - ({subsets_joined})"

    # 4. Добавяме и разширения израз
    expanded_joined = " + ".join(expanded_subsets_expr)
    full_expr = f"{ig_expr} = {total_entropy_expr} - ({expanded_joined})"

    return full_expr

# 📌 Данни за тест
data = [
    {"Цвят": "червен", "Форма": "кръг", "Клас": "Да"},
    {"Цвят": "зелен", "Форма": "кръг", "Клас": "Не"},
    {"Цвят": "червен", "Форма": "триъгълник", "Клас": "Да"},
    {"Цвят": "жълт", "Форма": "кръг", "Клас": "Да"},
    {"Цвят": "зелен", "Форма": "квадрат", "Клас": "Не"},
    {"Цвят": "жълт", "Форма": "триъгълник", "Клас": "Не"},
    {"Цвят": "червен", "Форма": "квадрат", "Клас": "Да"},
    {"Цвят": "червен", "Форма": "квадрат", "Клас": "Не"},
    {"Цвят": "жълт", "Форма": "квадрат", "Клас": "Да"},
    {"Цвят": "жълт", "Форма": "квадрат", "Клас": "Да"},
]

# 📌 Стартиране
print(information_gain_expression(data, target_attr="Клас", attribute="Цвят"))
