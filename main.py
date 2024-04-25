from tkinter import *
import pandas
from tkinter import messagebox
import random
import pyperclip
import json

to_learn = {}
current_card = {}

# ---------------------------- UI SETUP ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# ----------CARD UI----------- #
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR)
front_card = PhotoImage(file="images/card_front.png")
back_card = PhotoImage(file="images/card_back.png")
canvas_bg = canvas.create_image(412, 275, image=front_card)
language = canvas.create_text(400, 150, text="French", fill="black", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 253, text="trouve", fill="black", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# ---------------------------- FUNCTIONS & 9 ------------------------------- #

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def shuffle_cards():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(canvas_bg, image=front_card)
    canvas.itemconfig(language, text='French', fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    flip_timer = window.after(3000, card_flip)


def card_flip():
    canvas.itemconfig(canvas_bg, image=back_card)
    canvas.itemconfig(language, fill='white', text='English')
    canvas.itemconfig(card_word, fill='white', text=current_card["English"])


def is_known():
    to_learn.remove(current_card)
    print(len(to_learn))
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv")
    shuffle_cards()


# ----------BUTTON UI----------- #
incorrect_img = PhotoImage(file="images/wrong.png")
correct_img = PhotoImage(file="images/right.png")

incorrect_but = Button(image=incorrect_img, highlightthickness=0, command=shuffle_cards)
correct_but = Button(image=correct_img, highlightthickness=0, command=is_known)

incorrect_but.grid(column=0, row=2)
correct_but.grid(column=1, row=2)

flip_timer = window.after(3000, card_flip)

shuffle_cards()

window.mainloop()
