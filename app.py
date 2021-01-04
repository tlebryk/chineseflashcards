import tkinter as tk
import db
import card
import ebisu
from tkinter import ttk
from random import randint, shuffle
from datetime import date, timedelta, datetime
import spaced_rep

max_reviews = 15
max_new = 10
today = date.today()
conn = db.connect('vocab.db')


# append rows of cursor into list of cards 
def unpackcursor(cursor, card_list):
    for row in cursor: 
        c1 = {}
        for i in range(len(card.Card.fields)):
            c1[card.Card.fields[i][0]] = row[i]
        card_list.append(card.Card(**c1))
    return card_list

# takes a database connection and returns shuffled list of new and (lowest P(recall)) review cards. 
def todayscards():
    fields_text=", ".join([c[0] for c in card.Card.fields])
    cursor = conn.execute('''SELECT id, alpha, beta, t, last FROM vocabulary 
    WHERE learning = true and last IS NOT NULL''')
    counter = 0
    ls = []
    for row in cursor: 
        prior = (row[1], row[2], row[3]) 
        tnow= (today - datetime.strptime(row[4], "%Y-%m-%d").date()).days
        ls.append((row[0], ebisu.predictRecall(prior=prior, tnow= tnow)))
        counter+=1
    if counter < max_reviews: 
        cursor = conn.execute('''Select * FROM vocabulary 
        WHERE ID in ({});'''.format(', '.join(['?'] * counter)), 
        [el[0] for el in ls])
    else: 
        ls.sort(key=lambda x: x[1])
        cursor = conn.execute('''Select * FROM vocabulary 
        WHERE ID in ({});'''.format(', '.join(['?'] * max_reviews)), 
        [el[0] for el in ls[:max_reviews]])
    card_list = unpackcursor(cursor, [])
    cursor = conn.execute('''SELECT * FROM vocabulary 
        WHERE learning = false
        ORDER BY id''')
        # LIMIT (?);''', (max_new,))
    card_list = unpackcursor(cursor, card_list)
    shuffle(card_list)
    return card_list

class Root(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Flashcard app")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand="True")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.card_list = todayscards()
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
        w=self.card_list.pop(self.index) 
        if w.learning: 
            w.alpha, w.beta, w.t = ebisu.updateRecall(prior=(w.alpha, w.beta, w.t), successes = 0, total = 1, tnow = (w.last-today).days+.1)
        if not w.learning: 
            w.learning = True
            w.alpha,w.beta,w.t = spaced_rep.a_wrong, spaced_rep.b_wrong, spaced_rep.t_wrong
        w.last = today
        self.card_list.insert((self.index + len(self.card_list))//2, w)
        self.frames[Back].update(self.card_list[self.index])
        self.frames[Front].update(self.card_list[self.index])
        self.show_frame(Front)

    def right(self): 
        r= self.card_list[self.index]
        if not r.learning or not r.last: 
            r.last = today
            r.learning = True
            r.alpha, r.beta, r.t = spaced_rep.a_right,spaced_rep.b_right, spaced_rep.t_right 
        
        ebisu.updateRecall(prior=(r.alpha, r.beta, r.t), successes = 1, total = 1, tnow = (today-r.last).days+.1)
        self.card_list[self.index]=r
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
for c in main.card_list: 
    fields = [el for el in c.edited_fields if el in [f[0] for f in card.Card.fields]]
    if not fields: 
        continue 
    ls = []
    s=""
    for f in fields: 
        s+=f+"=?,"
        ls.append(getattr(c,f))
    s=s[:-1]
    ls.append(c.id)
    command = '''UPDATE vocabulary 
        SET {}
        WHERE id = (?);'''.format(s)
    print(command)
    conn.execute(command, ls)
   


conn.commit()
conn.close()