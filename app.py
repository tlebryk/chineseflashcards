import tkinter as tk
import db
import card
from tkinter import ttk
from random import randint
from datetime import datetime

# s = ttk.Style()
max_cards = 5
today = datetime.today()
fields_text=", ".join([c[0] for c in card.Card.fields])
conn = db.connect('vocab.db')
print(fields_text)
cursor = conn.execute(
    '''SELECT {f} FROM vocabulary 
    WHERE next <= {day}
    ORDER BY id
    LIMIT {lim}; 
    '''.format(f= fields_text, day = today.strftime("%Y=%m-%d"), lim=str(max_cards)))

class Root(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Flashcard app")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand="True")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.card_list = []
        for row in cursor: 
            c1 = card.Card()
            for i in range(len(card.Card.fields)):
                setattr(c1, card.Card.fields[i][0], row[i])
            self.card_list.append(c1)

        self.index = 0
        self.frames = {}
        for F in (StartPage, Front, Back):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, controller):
        frame = self.frames[controller]
        frame.tkraise()

    def wrong(self):
        w=self.card_list.pop(0) 
        w.interval = 0
        self.card_list.insert((self.index + len(self.card_list))//2, w)
        self.frames[Back].update(self.card_list[self.index])
        self.frames[Front].update(self.card_list[self.index])
        self.show_frame(Front)

    def right(self): 
        r= self.card_list[self.index]
        self.card_list[self.index].interval = 1+r.interval + r.interval * r.ease 
        self.index +=1
        if self.index < len(self.card_list):
            self.frames[Back].update(self.card_list[self.index])
            self.frames[Front].update(self.card_list[self.index])
            self.show_frame(Front)
        else: 
            self.show_frame(StartPage)


class StartPage(ttk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Start Page", font=("Verdana", 12))
        button1 = ttk.Button(self, text="Start Studying",
                             command=lambda: controller.show_frame(Front))
        button1.pack()


class Front(ttk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.Quiz = ttk.Label(self, text=controller.card_list[controller.index].chars)
        self.Quiz.grid(column=1, row=0)
        flip_but = ttk.Button(self, text="flip card",
                              command=lambda: controller.show_frame(Back))
        flip_but.grid(column=1, row=1)

    def update(self, cd):
        self.card = cd
        self.Quiz.config(text = cd.chars)


class Back(ttk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.eng = ttk.Label(self, text=controller.card_list[controller.index].english)
        self.eng.grid(column=1, row=0)
        self.pin = ttk.Label(self, text=controller.card_list[controller.index].pinyin)
        self.pin.grid(column=1, row=1)
        self.ex = ttk.Label(self, text=controller.card_list[controller.index].example_ch0)
        self.ex.grid(column=0, columnspan=3, row=2)
        flip_but = ttk.Button(self, text="flip card",
                              command=lambda: controller.show_frame(Front))
        flip_but.grid(column=1, row=3)
        flip_but = ttk.Button(self, text="flip card",
                              command=lambda: controller.show_frame(Front))
        again_but = ttk.Button(self, text="Again",
                              command=lambda: controller.wrong())
        again_but.grid(column=2, row=3)
        easy_but = ttk.Button(self, text="Easy",
                              command=lambda: controller.right())
        easy_but.grid(column=3, row=3)
    
    def update(self, cd): 
        # self.card = cd
        self.eng.config(text=cd.english)
        self.pin.config(text=cd.pinyin)
        self.ex.config(text=cd.example_ch0)




main = Root()
main.mainloop()
print("outof loop")
for field in card.Card.fields:
    print(str(field[0]) + "= " + str(getattr(main.card_list[0], field[0])) + ", ")
# conn.execute('''
#     UPDATE vocabulary set {updates} where 
#     id = {id}'''.format(atts = , new = , id = )


# )
conn.close()