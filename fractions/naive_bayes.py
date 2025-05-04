from collections import defaultdict, Counter

data = [
    {"Цвят": "зелен", "Размер": "голям", "Клас": "Б"},
    {"Цвят": "зелен", "Размер": "малък", "Клас": "А"},
    {"Цвят": "червен", "Размер": "голям", "Клас": "Б"},
    {"Цвят": "червен", "Размер": "малък", "Клас": "А"}
]

target = "Клас"
attributes = [key for key in data[0] if key != target]

# Стъпка 1: P(Клас)
class_counts = Counter(row[target] for row in data)
total = len(data)
class_probs = {cls: count / total for cls, count in class_counts.items()}

# Стъпка 2: P(Атрибут=стойност | Клас)
cond_probs = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

for row in data:
    cls = row[target]
    for attr in attributes:
        val = row[attr]
        cond_probs[attr][val][cls] += 1

# Нормализиране
for attr in cond_probs:
    for val in cond_probs[attr]:
        for cls in cond_probs[attr][val]:
            cond_probs[attr][val][cls] /= class_counts[cls]


# Функция за сметка
def predict_verbose(example):
    print(f"👉 Пример: {example}")
    probs = {}
    for cls in class_probs:
        prob = class_probs[cls]
        class_frac = f"{class_counts[cls]}/{total}"
        print(f"\n📦 Клас {cls}:")
        print(f"   P({cls}) = {class_frac} = {prob:.4f}")

        steps = [prob]
        step_strs = [f"{class_frac}"]

        for attr in attributes:
            val = example[attr]
            count = cond_probs[attr][val].get(cls, 0) * class_counts[cls]
            denom = class_counts[cls]
            if count == 0:
                # Лаплас за избягване на 0
                frac = "1/1000000"
                p = 1e-6
            else:
                frac = f"{int(count)}/{denom}"
                p = cond_probs[attr][val][cls]
            print(f"   P({attr}={val} | {cls}) = {frac} = {p:.4f}")
            steps.append(p)
            step_strs.append(frac)

        final_prob = 1
        for s in steps:
            final_prob *= s
        probs[cls] = final_prob
        print(f"   => Обща сметка: P={' * '.join(step_strs)} = {final_prob:.6f}")
    best = max(probs, key=probs.get)
    print(f"\n✅ Най-вероятен клас: {best}")
    return best, probs


# Тест
new_example = {"Цвят": "червен", "Размер": "малък"}
predict_verbose(new_example)
