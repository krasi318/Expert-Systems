import tkinter as tk

win = tk.Tk()
win.title("Помощ")
win.geometry("400x200")
tk.Label(win, text="Тук ще бъде помощ и инструкции за ползване", font=("Arial", 14)).pack(pady=50)
win.mainloop()
