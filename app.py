import tkinter as tk
import card
from tkinter import ttk
from random import randint
from datetime import datetime
import sqlite3

# s = ttk.Style()
max_cards = 100

today = datetime.today()
conn = sqlite3.connect('vocab.db')

cursor = conn.execute('''SELECT id, chars, pinyin, english, example_ch,
example_eng, last, ease, next, learning
 from vocabulary
where next <=(?)
limit (?)''', (today.strftime("%Y=%m-%d"), str(max_cards)))

cursor.fetchone()

cards = []
class card:
    def __init__(self, row):
        self.id =  row[0]
        self.chars = row[1]
        self.pinyin = row[2]
        self.english = row[3]
        self.example_ch = row[4]
        self.example_eng = row[5]
        self.last = row[6]
        self.next = row[8]
        self.ease = row[7]
        self.learning = row[9]
        self.baseline = row[8] - row[6]


for row in cursor:
    cards.append(card(row))

# keep old cards around to 
# be able to control Z 
completed_cards = []
def wrong(cards):
    w=cards.pop() 
    w.baseline = 0
    cards.insert((len(cards)//2), w)

# ease matching: 0 = hard, 0.5 = medium, 1 = hard
def right(cards, ease): 
    w= cards.pop()
    w.baseline = w.baseline + w.baseline * ease
    completed_cards.append(w)

class Root(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Flashcard app")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand="True")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, Front, Back):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, controller):
        frame = self.frames[controller]
        frame.tkraise()


class StartPage(ttk.Frame):
    def __init__(self, parent, controller):
        #
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Start Page", font=("Verdana", 12))
        # label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text="Start Studying",
                             command=lambda: controller.show_frame(Front))
        button1.pack()


class Front(ttk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        Quiz = ttk.Label(self, text=cards[0].chars)
        Quiz.grid(column=1, row=0)
        flip_but = ttk.Button(self, text="flip card",
                              command=lambda: controller.show_frame(Back))
        flip_but.grid(column=1, row=1)


class Back(ttk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        eng = ttk.Label(self, text=cards[0].english)
        eng.grid(column=1, row=0)
        pin = ttk.Label(self, text=cards[0].pinyin)
        pin.grid(column=1, row=1)
        ex = ttk.Label(self, text=cards[0].example)
        ex.grid(column=0, columnspan=3, row=2)
        flip_but = ttk.Button(self, text="flip card",
                              command=lambda: controller.show_frame(Front))
        flip_but.grid(column=1, row=1)
        flip_but = ttk.Button(self, text="flip card",
                              command=lambda: controller.show_frame(Front))
        again = ttk.Button(self, text="Again",
                              command=lambda: controller.show_frame(Front))
        easy = ttk.Button(self, text="Easy",
                              command=lambda: controller.show_frame(Front))


main = Root()
main.mainloop()
conn.close()