from collections import Counter, defaultdict

# 📌 Извеждане на дървото на решения
def print_decision_tree(data, target_attr, depth=0):
    indent = "  " * depth

    # 📌 Проверка дали всички примери са от един клас
    class_counts = Counter(row[target_attr] for row in data)
    if len(class_counts) == 1:
        single_class = next(iter(class_counts))
        print(f"{indent}Клас: {single_class}")
        return

    # 📌 Избор на най-добър атрибут (с най-много IG, но без сметки)
    attributes = [attr for attr in data[0].keys() if attr != target_attr]
    best_attr = find_best_attribute_simple(data, attributes, target_attr)

    print(f"{indent}{best_attr}:")
    values = sorted(set(row[best_attr] for row in data))
    for val in values:
        print(f"{indent}  {val} →")
        subset = [row for row in data if row[best_attr] == val]
        if subset:
            print_decision_tree(subset, target_attr, depth + 2)
        else:
            print(f"{indent}    Клас: неизвестен")

# 📌 Намери най-добър атрибут по честота на разделяне (заместител на IG без сметки)
def find_best_attribute_simple(data, attributes, target_attr):
    max_splits = -1
    best_attr = None
    for attr in attributes:
        splits = len(set(row[attr] for row in data))
        if splits > max_splits:
            max_splits = splits
            best_attr = attr
    return best_attr

# 📌 Данни
data = [
    {"Цвят": "червен", "Форма": "кръг", "Клас": "Да"},
    {"Цвят": "зелен", "Форма": "кръг", "Клас": "Не"},
    {"Цвят": "червен", "Форма": "триъгълник", "Клас": "Да"},
    {"Цвят": "жълт", "Форма": "кръг", "Клас": "Да"},
    {"Цвят": "зелен", "Форма": "квадрат", "Клас": "Не"},
    {"Цвят": "жълт", "Форма": "триъгълник", "Клас": "Не"},
    {"Цвят": "червен", "Форма": "квадрат", "Клас": "Да"},
    {"Цвят": "жълт", "Форма": "квадрат", "Клас": "Да"},
]

# 📌 Изпълнение
print("Решаващо дърво:")
print_decision_tree(data, target_attr="Клас")
