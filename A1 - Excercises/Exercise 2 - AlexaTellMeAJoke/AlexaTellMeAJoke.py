import tkinter as tk
import random
import os

# Load jokes
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "randomJokes.txt")
jokes = []
current_punchline = ""

try:
    with open(file_path, "r", encoding="utf-8-sig") as file:
        for line in file:
            if "?" in line:
                setup, punchline = line.strip().split("?", 1)
                if setup.strip() and punchline.strip():
                    jokes.append((setup.strip() + "?", punchline.strip()))
except FileNotFoundError:
    print("randomJokes.txt not found!")


# Button functions
def tell_joke():
    global current_punchline

    if jokes:
        setup, current_punchline = random.choice(jokes)
        setup_label.config(text=setup)
        punchline_label.config(text="Tap Show Punchline to reveal it.")
        status_label.config(text="Your joke is ready!")
    else:
        setup_label.config(text="No jokes available!")
        punchline_label.config(text="")


def show_punchline():
    if current_punchline:
        punchline_label.config(text=current_punchline)
        status_label.config(text="Hope that made you smile!")
    else:
        status_label.config(text="Choose a joke first!")


def quit_app():
    root.destroy()


# Main window
root = tk.Tk()
root.title("Alexa Joke Assistant")
root.geometry("420x760")
root.configure(bg="#dfe5ee")
root.resizable(False, False)

# iPhone body and screen
phone = tk.Frame(root, bg="#17191e", padx=6, pady=6)
phone.place(relx=0.5, rely=0.5, anchor="center", width=370, height=735)

screen = tk.Frame(phone, bg="#f7f8fc")
screen.pack(fill="both", expand=True)

# Status bar
bar = tk.Frame(screen, bg="#f7f8fc")
bar.pack(fill="x", padx=18, pady=(5, 2))

tk.Label(bar, text="9:41", font=("Arial", 9, "bold"),
         bg="#f7f8fc", fg="#17191e").pack(side="left")

tk.Label(bar, text="●  Wi-Fi  ▰", font=("Arial", 8, "bold"),
         bg="#f7f8fc", fg="#17191e").pack(side="right")

# Notch
notch = tk.Frame(screen, bg="#17191e", width=90, height=13)
notch.pack()
notch.pack_propagate(False)

# Header
header = tk.Frame(screen, bg="#f7f8fc")
header.pack(fill="x", padx=20, pady=(12, 8))

tk.Label(header, text="ALEXA", font=("Arial", 11, "bold"),
         bg="#f7f8fc", fg="#3478f6").pack(anchor="w")

tk.Label(header, text="Let's have a laugh!",
         font=("Arial", 21, "bold"), bg="#f7f8fc",
         fg="#182235").pack(anchor="w", pady=3)

tk.Label(header, text="Your personal joke assistant.",
         font=("Arial", 9), bg="#f7f8fc",
         fg="#7c8799").pack(anchor="w")

# Joke card
card = tk.Frame(screen, bg="white",
                highlightbackground="#e4e8ef",
                highlightthickness=1, height=235)
card.pack(fill="x", padx=18, pady=7)
card.pack_propagate(False)

tk.Label(card, text="😂  RANDOM JOKE",
         font=("Arial", 9, "bold"), bg="white",
         fg="#3478f6").pack(anchor="w", padx=15, pady=(12, 5))

setup_label = tk.Label(
    card, text="Press the button below to hear a joke!",
    font=("Arial", 15, "bold"), bg="white",
    fg="#182235", wraplength=290, justify="center", height=3
)
setup_label.pack(fill="x", padx=12, pady=4)

tk.Frame(card, bg="#edf0f5", height=1).pack(
    fill="x", padx=15, pady=5
)

tk.Label(card, text="PUNCHLINE", font=("Arial", 9, "bold"),
         bg="white", fg="#8994a6").pack(anchor="w", padx=15, pady=3)

punchline_label = tk.Label(
    card, text="Your punchline will appear here.",
    font=("Arial", 11), bg="white", fg="#43516a",
    wraplength=290, justify="center", height=3
)
punchline_label.pack(fill="x", padx=12, pady=3)

# Status
status_label = tk.Label(screen, text=str(len(jokes)) + " jokes loaded!",
                        font=("Arial", 9), bg="#f7f8fc",
                        fg="#8994a6")
status_label.pack(pady=7)


# Button design
def make_button(parent, text, command, colour, text_colour):
    return tk.Button(
        parent, text=text, command=command,
        font=("Arial", 10, "bold"), bg=colour,
        fg=text_colour, activebackground=colour,
        activeforeground=text_colour, relief="flat",
        cursor="hand2", bd=0, height=2
    )


# Button layout
button_area = tk.Frame(screen, bg="#f7f8fc")
button_area.pack(fill="x", padx=20, pady=5)

make_button(button_area, "🎤  Alexa, Tell Me a Joke",
            tell_joke, "#3478f6", "white").pack(fill="x", pady=(0, 9))

small_buttons = tk.Frame(button_area, bg="#f7f8fc")
small_buttons.pack(fill="x", pady=(0, 9))
small_buttons.columnconfigure((0, 1), weight=1)

make_button(small_buttons, "Show Punchline", show_punchline,
            "#e9efff", "#3478f6").grid(row=0, column=0, sticky="ew", padx=(0, 5))

make_button(small_buttons, "Next Joke  →", tell_joke,
            "#e9efff", "#3478f6").grid(row=0, column=1, sticky="ew", padx=(5, 0))

make_button(button_area, "✕  Quit", quit_app,
            "#ffe8e8", "#d74747").pack(fill="x")

# iPhone home indicator
tk.Frame(screen, bg="#17191e", width=75, height=4).pack(
    side="bottom", pady=7
)

# Start application
root.mainloop()
