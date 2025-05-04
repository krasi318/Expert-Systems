import tkinter as tk

win = tk.Tk()
win.title("Цяло дърво")
win.geometry("400x200")
tk.Label(win, text="Тук ще се покаже цялото дърво на решението", font=("Arial", 14)).pack(pady=50)
win.mainloop()
