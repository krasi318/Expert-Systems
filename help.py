import tkinter as tk

# Create the main window
win = tk.Tk()
win.title("Помощ")
win.geometry("820x250")

# Add a label with the description of the app
description = "Това приложение помага с различни задачи и предоставя ресурси за учене.\n\n" \
              "Ако имате въпроси или искате да обсъждате, можете да се присъедините към нашия Discord сървър."

tk.Label(win, text=description, font=("Arial", 12), justify="center").pack(pady=20)

# Add the Discord invite link label
discord_label = tk.Label(win, text="Присъединете се към нашия Discord: https://discord.gg/uBTAT2fRzf",
                         font=("Arial", 12, "italic"), fg="blue", cursor="hand2")
discord_label.pack(pady=20)

# Make the Discord label clickable to open the link in the browser
def open_discord():
    import webbrowser
    webbrowser.open("https://discord.gg/uBTAT2fRzf")

discord_label.bind("<Button-1>", lambda e: open_discord())

# Start the Tkinter event loop
win.mainloop()
