import tkinter as tk
import db
import card
from tkinter import ttk
from random import randint
from datetime import datetime

# s = ttk.Style()
max_cards = 10

today = datetime.today()
conn = db.connect('vocab.db')

fields_text=", ".join([c[0] for c in card.Card.fields])

cursor = conn.execute(
    '''SELECT {f} FROM vocabulary 
    WHERE next <= {day}
    ORDER BY id
    LIMIT {lim}; 
    '''.format(f= fields_text, day = today.strftime("%Y=%m-%d"), lim=str(max_cards)))

# [print(row) for row in cursor]  


card_list = []
for row in cursor: 
    c1 = card.Card()
    for i in range(len(card.Card.fields)):
        setattr(c1, card.Card.fields[i][0], row[i])
    card_list.append(c1)



# for row in cursor:
#     cards.append(card(row))

# keep old cards around to 
# be able to control Z 
# completed_cards = []
# def wrong(cards):
#     w=cards.pop() 
#     w.baseline = 0
#     cards.insert((len(cards)//2), w)

# # ease matching: 0 = hard, 0.5 = medium, 1 = hard
# def right(cards, ease): 
#     w= cards.pop()
#     w.baseline = w.baseline + w.baseline * ease
#     completed_cards.append(w)

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
        button1 = ttk.Button(self, text="Start Studying",
                             command=lambda: controller.show_frame(Front))
        button1.pack()


class Front(ttk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        Quiz = ttk.Label(self, text=card_list[0].chars)
        Quiz.grid(column=1, row=0)
        flip_but = ttk.Button(self, text="flip card",
                              command=lambda: controller.show_frame(Back))
        flip_but.grid(column=1, row=1)


class Back(ttk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        eng = ttk.Label(self, text=card_list[0].english)
        eng.grid(column=1, row=0)
        pin = ttk.Label(self, text=card_list[0].pinyin)
        pin.grid(column=1, row=1)
        ex = ttk.Label(self, text=card_list[0].example_ch0)
        ex.grid(column=0, columnspan=3, row=2)
        flip_but = ttk.Button(self, text="flip card",
                              command=lambda: controller.show_frame(Front))
        flip_but.grid(column=1, row=3)
        flip_but = ttk.Button(self, text="flip card",
                              command=lambda: controller.show_frame(Front))
        again_but = ttk.Button(self, text="Again",
                              command=lambda: controller.show_frame(Front))
        again_but.grid(column=2, row=3)

        easy_but = ttk.Button(self, text="Easy",
                              command=lambda: controller.show_frame(Front))
        easy_but.grid(column=3, row=3)



main = Root()
main.mainloop()
conn.close()