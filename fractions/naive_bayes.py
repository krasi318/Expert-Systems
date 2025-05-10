from collections import defaultdict, Counter

# Данни
data = [
  {
    "стил": "гръндж",
    "гледана преди": "да",
    "времетраене": "20",
    "одобрение": "не"
  },
  {
    "стил": "рнб",
    "гледана преди": "да",
    "времетраене": "20",
    "одобрение": "не"
  },
  {
    "стил": "гръндж",
    "гледана преди": "не",
    "времетраене": "20",
    "одобрение": "не"
  },
  {
    "стил": "бритпоп",
    "гледана преди": "не",
    "времетраене": "20",
    "одобрение": "не"
  },
  {
    "стил": "бритпоп",
    "гледана преди": "не",
    "времетраене": "20",
    "одобрение": "да"
  },
  {
    "стил": "гръндж",
    "гледана преди": "не",
    "времетраене": "30",
    "одобрение": "да"
  },
  {
    "стил": "рнб",
    "гледана преди": "не",
    "времетраене": "20",
    "одобрение": "да"
  },
  {
    "стил": "рнб",
    "гледана преди": "да",
    "времетраене": "30",
    "одобрение": "да"
  }
]

# Целева променлива
target = "одобрение"

# 👉 Потребителски избор на атрибути
available_attributes = [key for key in data[0] if key != target]
print("Налични атрибути:", ', '.join(available_attributes))
chosen_attrs = input("Избери атрибути, разделени със запетая (например: стил,времетраене): ").strip().split(',')
attributes = [attr.strip() for attr in chosen_attrs if attr.strip() in available_attributes]

if not attributes:
    print("❌ Не са избрани валидни атрибути. Прекратяване.")
    exit()

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

# Предикция с обяснение
def predict_verbose(example):
    print(f"\n👉 Пример за класифициране: {example}")
    probs = {}
    for cls in class_probs:
        prob = class_probs[cls]
        class_frac = f"{class_counts[cls]}/{total}"
        print(f"\n📦 Клас {cls}:")
        print(f"   P({cls}) = {class_frac} = {prob:.4f}")

        steps = [prob]
        step_strs = [class_frac]

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
        print(f"   => Обща вероятност: {' * '.join(step_strs)} = {final_prob:.8f}")

    best = max(probs, key=probs.get)
    print(f"\n✅ Най-вероятен клас: {best}")
    return best, probs


# 👉 Подаване на нов пример
example_input = {}
for attr in attributes:
    value = input(f"Въведи стойност за '{attr}': ").strip()
    example_input[attr] = value

predict_verbose(example_input)
