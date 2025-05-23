from collections import defaultdict, Counter

# Примерна таблица от задачата (като списък от речници)
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

target = "одобрение"


def train_one_r_verbose(data, target):
    attributes = [key for key in data[0] if key != target]
    best_attr = None
    best_rules = {}
    lowest_error = float('inf')

    for attr in attributes:
        print(f"\n📂 Анализ на атрибута: {attr}")
        rules = {}
        error = 0
        grouped = defaultdict(list)

        # Групира по стойности на атрибута
        for row in data:
            grouped[row[attr]].append(row[target])

        for val, targets in grouped.items():
            counter = Counter(targets)
            most_common, count = counter.most_common(1)[0]
            total = len(targets)
            errors = total - count
            rules[val] = most_common
            error += errors

            print(f" - {val}: {most_common} -> {errors}/{total} грешки")

        print(f" 🧮 Общо грешки за {attr}: {error}")

        if error < lowest_error:
            lowest_error = error
            best_attr = attr
            best_rules = rules

    print("\n✅ Най-добър атрибут според OneR:")
    print(f" 👉 {best_attr} с {lowest_error} общи грешки")
    print("📜 Генерирани правила:")
    for val, pred in best_rules.items():
        print(f" - Ако {best_attr} = {val}, тогава {target} = {pred}")


# Стартирай
train_one_r_verbose(data, target)