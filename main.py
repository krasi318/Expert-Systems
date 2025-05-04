import tkinter as tk
import subprocess

def open_page(script_name):
    subprocess.Popen(["python3", script_name])

root = tk.Tk()
root.title("Решаване на задачи по ЕС")
root.geometry("600x400")
root.configure(bg="gray")

tk.Label(root, text="Решаване на задачи по ЕС", font=("Arial", 20), bg="gray").pack(pady=20)

buttons = [
    ("Вкарай таблица", "enter_table.py"),
    ("ONE R", "one_r.py"),
    ("НАИВЕН БЕЙС", "naiven_bayes.py"),
    ("ЕНТРОПИЯ", "entropiq.py"),
    ("IG", "ig.py"),
    ("корен на дърво", "tree_root.py"),
    ("Цяло дърво", "whole_tree.py"),
    ("помощ", "help.py")
]

for text, script in buttons:
    tk.Button(root, text=text, width=20, height=2, command=lambda s=script: open_page(s)).pack(pady=5)

root.mainloop()
