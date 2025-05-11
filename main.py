import tkinter as tk
import subprocess
import sys
import os

def resource_path(relative_path):
    """Get the absolute path to the resource, whether running as an executable or not."""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller bundles files in _MEIPASS during runtime
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

def open_page(script_name):
    """Opens the selected script using subprocess."""
    if script_name:
        # Get the full path to the script
        full_path = resource_path(script_name)
        # Open the Python script using subprocess
        subprocess.Popen([sys.executable, full_path])

root = tk.Tk()
root.title("Решаване на задачи по ЕС")
root.geometry("800x600")  # Set a larger default size
root.configure(bg="gray")

# Make the window resizable
root.resizable(True, True)

# Label at the top
tk.Label(root, text="Решаване на задачи по ЕС", font=("Arial", 20), bg="gray").grid(row=0, column=0, columnspan=3, pady=20)

# Add the first button in the first row, centered across all columns
tk.Button(root, text="Вкарай таблица", width=20, height=2,
          command=lambda: open_page("enter_table.py")).grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

# Buttons list
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

# Use grid layout for buttons
for idx, (text, script) in enumerate(buttons):
    row = (idx // 3) + 2  # Start from row 2
    col = idx % 3
    tk.Button(root, text=text, width=20, height=2,
              command=lambda s=script: open_page(s)).grid(row=row, column=col, padx=10, pady=10, sticky="ew")

# Add the "помощ" button
tk.Button(root, text="помощ", width=20, height=2,
          command=lambda: open_page("help.py")).grid(row=row + 1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

# Allow columns to resize dynamically
for col in range(3):
    root.grid_columnconfigure(col, weight=1)

root.mainloop()
