import json
from collections import defaultdict, Counter
import tkinter as tk
from tkinter import simpledialog, messagebox


def load_data():
    with open("data.json", "r", encoding="utf-8") as f:
        return json.load(f)


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


def classify(example, best_attr, best_rules, target):
    val = example[best_attr]
    prediction = best_rules.get(val, "неизвестно")
    log = f"\n🔍 Класификация за пример:\n"
    log += f" - Стойност на {best_attr}: {val}\n"
    log += f" - Предсказан {target}: {prediction}\n"
    return log


def main():
    try:
        data = load_data()
        target = list(data[0].keys())[-1]

        best_attr, best_rules, log = train_one_r_verbose(data, target)

        # Избор на индекс за тестов ред
        root = tk.Tk()
        root.withdraw()
        test_index = simpledialog.askinteger("Избор на ред", f"Въведи номер на ред за тест (0 - {len(data)-1}):")
        if test_index is None or test_index < 0 or test_index >= len(data):
            messagebox.showerror("Грешка", "Невалиден индекс!")
            return

        example = data[test_index]
        example_no_target = {k: v for k, v in example.items() if k != target}

        log += classify(example_no_target, best_attr, best_rules, target)

        # Показване на резултата
        messagebox.showinfo("Резултат", log)

    except Exception as e:
        messagebox.showerror("Грешка", f"⚠️ Възникна грешка:\n{e}")


if __name__ == "__main__":
    main()
