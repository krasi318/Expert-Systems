from collections import Counter

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

# 📌 Ентропия само като формула
def print_entropy_expression(data, target_attr):
    class_counts = Counter(row[target_attr] for row in data)
    print(f"\n📊 Класове по {target_attr}: {dict(class_counts)}")
    expression = entropy_expression(class_counts, target_attr)
    print(f"🎯 Ентропията на {target_attr} е:\n{expression}")

# 📌 Примерни данни
data = [
    {"Цвят": "зелен", "Форма": "кръг", "Клас": "А"},
    {"Цвят": "червен", "Форма": "кръг", "Клас": "Б"},
    {"Цвят": "зелен", "Форма": "триъгълник", "Клас": "Б"},
    {"Цвят": "жълт", "Форма": "кръг", "Клас": "А"},
    {"Цвят": "червен", "Форма": "триъгълник", "Клас": "Б"},
    {"Цвят": "червен", "Форма": "триъгълник", "Клас": "Б"},
]

# 📌 Стартиране
print_entropy_expression(data, target_attr="Клас")
