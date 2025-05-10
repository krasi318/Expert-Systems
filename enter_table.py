import tkinter as tk
from tkinter import messagebox
import json

class TableApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Вкарай таблица")
        self.master.geometry("800x500")

        self.rows = []
        self.num_cols = 3  # Начален брой колони

        # Основна рамка
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill="both", expand=True)

        # Лява рамка за таблицата
        self.table_frame = tk.Frame(self.main_frame)
        self.table_frame.pack(side="left", fill="both", expand=True)

        # Платно за скролиране
        self.canvas = tk.Canvas(self.table_frame)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.v_scroll = tk.Scrollbar(self.table_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.v_scroll.set)

        self.v_scroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Дясна рамка за бутоните
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(side="right", fill="y", padx=10)

        tk.Button(self.button_frame, text="Добави ред", command=self.add_row).pack(pady=5)
        tk.Button(self.button_frame, text="Премахни ред", command=self.remove_row).pack(pady=5)
        tk.Button(self.button_frame, text="Добави колона", command=self.add_column).pack(pady=5)
        tk.Button(self.button_frame, text="Премахни колона", command=self.remove_column).pack(pady=5)
        tk.Button(self.button_frame, text="Запази таблица", command=self.save_table).pack(pady=5)
        tk.Button(self.button_frame, text="Изчисти таблица", command=self.clear_table).pack(pady=5)
        tk.Button(self.button_frame, text="Зареди таблица", command=self.load_table).pack(pady=20)

        self.add_row()  # първи ред

    def add_row(self):
        row = []
        row_index = len(self.rows)
        for col in range(self.num_cols):
            entry = tk.Entry(self.scrollable_frame, width=15)
            entry.grid(row=row_index, column=col, padx=5, pady=5)
            row.append(entry)
        self.rows.append(row)

    def remove_row(self):
        if self.rows:
            last_row = self.rows.pop()
            for widget in last_row:
                widget.destroy()

    def add_column(self):
        self.num_cols += 1
        for i, row in enumerate(self.rows):
            entry = tk.Entry(self.scrollable_frame, width=15)
            entry.grid(row=i, column=self.num_cols - 1, padx=5, pady=5)
            row.append(entry)

    def remove_column(self):
        if self.num_cols <= 1:
            return  # Поне една колона
        self.num_cols -= 1
        for row in self.rows:
            entry = row.pop()
            entry.destroy()

    def save_table(self):
        data = []
        for row in self.rows:
            row_data = [entry.get() for entry in row]
            if any(cell.strip() for cell in row_data):  # пропуска празни редове
                data.append(row_data)

        if not data:
            messagebox.showwarning("Внимание", "Таблицата е празна.")
            return

        # Първият ред приема ролята на заглавия (хедъри)
        headers = data[0]
        records = data[1:]  # останалите редове са реални записи

        dict_data = [dict(zip(headers, row)) for row in records]

        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(dict_data, f, ensure_ascii=False, indent=2)

        messagebox.showinfo("Успех", "Таблицата е запазена в data.json")

    def clear_table(self):
        """Изчистване на всички редове и колони."""
        for row in self.rows:
            for widget in row:
                widget.destroy()
        self.rows.clear()
        self.num_cols = 3
        self.add_row()

    def load_table(self):
        """Зареждане на таблицата от файла data.json."""
        try:
            with open("data.json", "r", encoding="utf-8") as f:
                dict_data = json.load(f)

            if not dict_data:
                messagebox.showwarning("Внимание", "Таблицата е празна.")
                return

            # Първият ред е заглавията (хедъри)
            headers = list(dict_data[0].keys())
            self.clear_table()  # Изчистваме съществуващата таблица

            # Добавяме колоните и заглавията (първи ред)
            self.num_cols = len(headers)
            for i, header in enumerate(headers):
                entry = tk.Entry(self.scrollable_frame, width=15)
                entry.insert(tk.END, header)  # Вмъкване на заглавието в първия ред
                entry.grid(row=0, column=i, padx=5, pady=5)  # Позиционираме заглавието

            # Добавяме данните (останалите редове)
            for row_index, row_data in enumerate(dict_data):
                row = []
                for col_index, header in enumerate(headers):
                    entry = tk.Entry(self.scrollable_frame, width=15)
                    entry.insert(tk.END, row_data.get(header, ''))
                    entry.grid(row=row_index + 1, column=col_index, padx=5, pady=5)  # Позиционираме данните
                    row.append(entry)
                self.rows.append(row)  # Добавяме реда в self.rows

            # След добавяне на всички данни, обновяваме таблицата
            self.update_table()

        except Exception as e:
            messagebox.showerror("Грешка", f"Не може да зареди файла: {e}")

    def update_table(self):
        """Обновяване на таблицата (поставяне на стойностите в редовете)."""
        for i, row in enumerate(self.rows):
            for j, entry in enumerate(row):
                entry.grid(row=i, column=j, padx=5, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = TableApp(root)
    root.mainloop()
