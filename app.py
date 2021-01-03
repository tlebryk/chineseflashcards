import tkinter as tk
import db
import card
from tkinter import ttk
from random import randint
from datetime import date
from datetime import timedelta
import ebisu
from sortedcontainers import SortedList

# s = ttk.Style()
max_cards = 15
max_new = 10
# today = date.today()
# fields_text=", ".join([c[0] for c in card.Card.fields])
# conn = db.connect('vocab.db')
# print(fields_text)
# cursor = conn.execute(
#     '''SELECT {f} FROM vocabulary 
#     WHERE next <= {day}
#     ORDER BY id
#     LIMIT {lim}; 
#     '''.format(f= fields_text, day = today.strftime("%Y=%m-%d"), lim=str(max_cards-new_cards)))

# #review cards
# cursor = conn.execute(
#     '''SELECT {f} FROM vocabulary 
#     WHERE Learning = true
#     ORDER BY id
#     LIMIT {lim}; 
#     '''.format(f= fields_text, lim=str(max_cards-max_new)))


# for row in cursor: 


# # new cards

# cursor = conn.execute(
#     '''SELECT {f} FROM vocabulary 
#     WHERE Learning = false
#     ORDER BY id
#     LIMIT {lim}; 
#     '''.format(f= fields_text, day = today.strftime("%Y=%m-%d"), lim=str(max_new)))

# class Root(tk.Tk):
#     def __init__(self, *args, **kwargs):
#         tk.Tk.__init__(self, *args, **kwargs)
#         self.title("Flashcard app")
#         container = tk.Frame(self)
#         container.pack(side="top", fill="both", expand="True")
#         container.grid_rowconfigure(0, weight=1)
#         container.grid_columnconfigure(0, weight=1)
        
#         self.card_list = []
#         for row in cursor: 
#             c1 = card.Card()
#             for i in range(len(card.Card.fields)):
#                 setattr(c1, card.Card.fields[i][0], row[i])
#             self.card_list.append(c1)

#         self.index = 0
#         self.frames = {}
#         for F in (StartPage, Front, Back):
#             frame = F(container, self)
#             self.frames[F] = frame
#             frame.grid(row=0, column=0, sticky="nsew")
#         self.show_frame(StartPage)

#     def show_frame(self, controller):
#         frame = self.frames[controller]
#         frame.tkraise()

#     def wrong(self):
#         w=self.card_list.pop(self.index) 
#         if w.learning: 
#             w.alpha, w.beta, w.t = ebisu.updateRecall(prior=(w.alpha, w.beta, w.t), successes = 0, total = 1, tnow = w.last-today)
#         if not w.learning: 
#             w.learning = True
#             w.last = today

        
        
#         self.card_list.insert((self.index + len(self.card_list))//2, w)
#         self.frames[Back].update(self.card_list[self.index])
#         self.frames[Front].update(self.card_list[self.index])
#         self.show_frame(Front)

#     def right(self): 
#         r= self.card_list[self.index]
#         self.card_list[self.index].interval = 1+r.interval + (r.interval * r.ease)
#         self.card_list[self.index].next = today + timedelta(days = self.card_list[self.index].interval)
#         self.index +=1
#         if self.index < len(self.card_list):
#             self.frames[Back].update(self.card_list[self.index])
#             self.frames[Front].update(self.card_list[self.index])
#             self.show_frame(Front)
#         else: 
#             self.show_frame(StartPage)


# class StartPage(ttk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         label = ttk.Label(self, text="Start Page", font=("Verdana", 12))
#         button1 = ttk.Button(self, text="Start Studying",
#                              command=lambda: controller.show_frame(Front))
#         button1.pack()


# class Front(ttk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.Quiz = ttk.Label(self, text=controller.card_list[controller.index].chars)
#         self.Quiz.grid(column=1, row=0)
#         flip_but = ttk.Button(self, text="flip card",
#                               command=lambda: controller.show_frame(Back))
#         flip_but.grid(column=1, row=1)

#     def update(self, cd):
#         self.card = cd
#         self.Quiz.config(text = cd.chars)


# class Back(ttk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.eng = ttk.Label(self, text=controller.card_list[controller.index].english)
#         self.eng.grid(column=1, row=0)
#         self.pin = ttk.Label(self, text=controller.card_list[controller.index].pinyin)
#         self.pin.grid(column=1, row=1)
#         self.ex = ttk.Label(self, text=controller.card_list[controller.index].example_ch0)
#         self.ex.grid(column=0, columnspan=3, row=2)
#         flip_but = ttk.Button(self, text="flip card",
#                               command=lambda: controller.show_frame(Front))
#         flip_but.grid(column=1, row=3)
#         flip_but = ttk.Button(self, text="flip card",
#                               command=lambda: controller.show_frame(Front))
#         again_but = ttk.Button(self, text="Again",
#                               command=lambda: controller.wrong())
#         again_but.grid(column=2, row=3)
#         easy_but = ttk.Button(self, text="Easy",
#                               command=lambda: controller.right())
#         easy_but.grid(column=3, row=3)
    
#     def update(self, cd): 
#         # self.card = cd
#         self.eng.config(text=cd.english)
#         self.pin.config(text=cd.pinyin)
#         self.ex.config(text=cd.example_ch0)




# main = Root()
# main.mainloop()
# for c in main.card_list: 
#     update = ""
#     for field in card.Card.fields:
#         if getattr(c, field[0]) or getattr(c, field[0]) == 0: 
#             update += str(field[0]) + " = " + str(getattr(c, field[0])) + ", "
#         else: 
#             update += str(field[0]) + " = " + "NULL, " 
#     update = update[:-2]
#     conn.execute(
#         '''UPDATE vocabulary 
#         SET chars = (?), pinyin= (?), english= (?), 
#         example_eng0= (?), example_eng1= (?), example_eng2= (?),
#         example_ch0= (?), example_ch1= (?), example_ch2= (?), 
#         interval= (?), next= (?), ease= (?), learning= (?)
#         WHERE id = (?);''', (getattr(c, 'chars'), getattr(c, 'pinyin'), getattr(c, 'english'),
#         getattr(c, 'example_eng0'), getattr(c, 'example_eng1'), getattr(c, 'example_eng2'),
#         getattr(c, 'example_ch0'), getattr(c, 'example_ch1'), getattr(c, 'example_ch2'), 
#         getattr(c, 'interval'), getattr(c, 'next'), getattr(c, 'ease'), getattr(c, 'learning'), getattr(c, 'id')))


# conn.commit()
# conn.close()