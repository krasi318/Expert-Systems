import tkinter as tk
import subprocess

def open_page(script_name):
    subprocess.Popen(["python", script_name])

root = tk.Tk()
root.title("Решаване на задачи по ЕС")
root.geometry("800x600")  # Set a larger default size
root.configure(bg="gray")

# Make the window resizable
root.resizable(True, True)

# Label at the top
tk.Label(root, text="Решаване на задачи по ЕС", font=("Arial", 20), bg="gray").grid(row=0, column=0, columnspan=3, pady=20)

# Add the first button in the first row, centered across all columns
tk.Button(root, text="Вкарай таблица", width=20, height=2, command=lambda: open_page("enter_table.py")).grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

# Button list and layout in a grid with multiple rows and columns (excluding "Вкарай таблица" and "помощ")
buttons = [
    ("ONE R", "one_r.py"),
    ("НАИВЕН БЕЙС", "naiven_bayes.py"),
    ("ЕНТРОПИЯ", "entropiq.py"),
    ("IG", "ig.py"),
    ("корен на дърво", "tree_root.py"),
    ("дърво с рисунка (beta)", "tree_root_draw.py"),
    ("Цяло дърво beta", "whole_tree.py"),
    ("тази функ ще се добави скоро!", None),
    ("тази функ ще се добави скоро!", None),

]

# Use grid layout for buttons (adjust for multiple columns and rows)
for idx, (text, script) in enumerate(buttons):
    row = (idx // 3) + 2  # Start from row 2, as row 1 is taken by the first button
    col = idx % 3  # This will distribute buttons into columns
    tk.Button(root, text=text, width=20, height=2, command=lambda s=script: open_page(s)).grid(row=row, column=col, padx=10, pady=10, sticky="ew")

# Add the "помощ" button in the bottom-left corner, with the same size as "Вкарай таблица"
tk.Button(root, text="помощ", width=20, height=2, command=lambda: open_page("help.py")).grid(row=row + 1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

# Make the columns resize dynamically when the window is resized
for col in range(3):
    root.grid_columnconfigure(col, weight=1)

root.mainloop()
