import threading
import time
import customtkinter as ctk
import keyboard

# --- State ---
running = False

# --- Spam Thread ---
def spam_e(interval=0.03):
    """Continuously spam 'e' when running==True."""
    while True:
        if running:
            keyboard.send('e')
        time.sleep(interval)

# --- Toggle Function ---
def toggle_spam():
    global running
    running = not running
    btn_toggle.configure(
        text="Stop Spamming" if running else "Start Spamming"
    )

# --- Register F7 Hotkey ---
keyboard.add_hotkey('f7', toggle_spam)

# --- Start background thread ---
threading.Thread(target=spam_e, daemon=True).start()

# --- CustomTkinter UI Setup ---
ctk.set_appearance_mode("System")  # Mode: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Theme: "blue" (default), "green", "dark-blue"

app = ctk.CTk()
app.title("E-Key Spammer")
app.geometry("300x150")

# Toggle button
btn_toggle = ctk.CTkButton(
    master=app,
    text="Start Spamming",
    width=200,
    height=40,
    command=toggle_spam
)
btn_toggle.pack(pady=(30, 10))

# Info label
lbl_info = ctk.CTkLabel(
    master=app,
    text="Or press F7 to toggle spamming",
    text_color="#888888"
)
lbl_info.pack()

app.mainloop()
