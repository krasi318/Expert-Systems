import json
import tkinter as tk
from collections import defaultdict, Counter
from tkinter import simpledialog, messagebox

# 📌 Зарежда и обработва JSON

def load_data():
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

# 📌 Наивен Байес с избираеми атрибути и потребителски вход

def predict_verbose(data, example, selected_attrs):
    if len(data) < 2:
        return "Няма достатъчно данни."

    target = list(data[0].keys())[-1]

    class_counts = Counter(row[target] for row in data)
    total = len(data)
    class_probs = {cls: count / total for cls, count in class_counts.items()}

    cond_probs = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    for row in data:
        cls = row[target]
        for attr in selected_attrs:
            val = row[attr]
            cond_probs[attr][val][cls] += 1

    for attr in cond_probs:
        for val in cond_probs[attr]:
            for cls in cond_probs[attr][val]:
                cond_probs[attr][val][cls] /= class_counts[cls]

    output = [f"👉 Пример: {example}"]
    probs = {}

    for cls in class_probs:
        prob = class_probs[cls]
        class_frac = f"{class_counts[cls]}/{total}"
        output.append(f"\n📦 Клас {cls}:")
        output.append(f"   P({cls}) = {class_frac} = {prob:.4f}")

        steps = [prob]
        step_strs = [class_frac]

        for attr in selected_attrs:
            val = example[attr]
            count = cond_probs[attr][val].get(cls, 0) * class_counts[cls]
            denom = class_counts[cls]
            if count == 0:
                frac = "1/1000000"
                p = 1e-6
            else:
                frac = f"{int(count)}/{denom}"
                p = cond_probs[attr][val][cls]
            output.append(f"   P({attr}={val} | {cls}) = {frac} = {p:.4f}")
            steps.append(p)
            step_strs.append(frac)

        final_prob = 1
        for s in steps:
            final_prob *= s
        probs[cls] = final_prob
        output.append(f"   => Обща сметка: P = {' * '.join(step_strs)} = {final_prob:.6f}")

    best = max(probs, key=probs.get)
    output.append(f"\n✅ Най-вероятен клас: {best}")
    return "\n".join(output)

# 📌 Показване на резултат

def show_custom_prediction():
    data = load_data()
    headers = list(data[0].keys())
    target_attr = headers[-1]
    attributes = [k for k in headers if k != target_attr]

    selected_attrs = []
    for attr in attributes:
        if messagebox.askyesno("Избор на атрибути", f"Да използваме атрибута '{attr}'?"):
            selected_attrs.append(attr)

    if not selected_attrs:
        messagebox.showerror("Грешка", "Не са избрани атрибути.")
        return

    example = {}
    for attr in selected_attrs:
        value = simpledialog.askstring("Вход", f"Въведи стойност за '{attr}':")
        if value is None:
            return  # отказан вход
        example[attr] = value

    try:
        result = predict_verbose(data, example, selected_attrs)
    except Exception as e:
        result = f"⚠️ Грешка: {e}"

    result_window = tk.Toplevel()
    result_window.title("Резултат от Naive Bayes")
    text = tk.Text(result_window, wrap="word", font=("Consolas", 12))
    text.insert("1.0", result)
    text.pack(padx=20, pady=20, expand=True, fill="both")

# 📌 Основен прозорец с избор

def main():
    data = load_data()

    window = tk.Tk()
    window.title("Избор на пример за Naive Bayes")

    label = tk.Label(window, text="Избери ред за класификация:", font=("Arial", 12))
    label.pack(pady=(10, 0))

    listbox = tk.Listbox(window, width=80, height=10, font=("Consolas", 11))
    for i, row in enumerate(data[1:]):
        values = ', '.join(f"{k}={v}" for k, v in row.items())
        listbox.insert(tk.END, f"[{i}] {values}")
    listbox.pack(padx=10, pady=10)

    def on_select():
        selected = listbox.curselection()
        if selected:
            index = selected[0]
            headers = data[0]
            target_attr = list(headers.keys())[-1]
            row = data[index + 1]
            example = {k: v for k, v in row.items() if k != target_attr}
            result = predict_verbose(data, example, list(example.keys()))

            result_window = tk.Toplevel()
            result_window.title("Резултат от Naive Bayes")
            text = tk.Text(result_window, wrap="word", font=("Consolas", 12))
            text.insert("1.0", result)
            text.pack(padx=20, pady=20, expand=True, fill="both")

    btn = tk.Button(window, text="Анализирай избран ред", command=on_select)
    btn.pack(pady=(0, 10))

    custom_btn = tk.Button(window, text="Създай собствен пример", command=show_custom_prediction)
    custom_btn.pack(pady=(0, 10))

    window.mainloop()

if __name__ == "__main__":
    main()
