import tkinter as tk
from tkinter import ttk

chars = "char"
english = "english"
pinyin = "pinyin"
example = "example"
# s = ttk.Style()

class Root(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Flashcard app")
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = "True")
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {}
        for F in (StartPage, Front, Back):
            frame = F(container,self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, controller):
        frame = self.frames[controller]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        #
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font = ("Verdana", 12))
        label.pack(pady=10, padx=10)
        button1 = tk.Button(self, text= "Start Studying",
            command = lambda: controller.show_frame(Front))
        button1.pack()

class Front(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        Quiz = tk.Label(self, text = chars)
        Quiz.grid(column=1, row=0)
        flip_but = ttk.Button(self, text = "flip card",
            command= lambda: controller.show_frame(Back))
        flip_but.grid(column=1, row=1)

class Back(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        eng = tk.Label(self, text = english)
        eng.grid(column=1, row=0)
        pin = tk.Label(self, text =pinyin)
        pin.grid(column=1, row=1)
        ex = tk.Label(self, text = example)
        ex.grid(column=0, columnspan = 3, row=2)
        flip_but = tk.Button(self, text = "flip card",
            command= lambda: controller.show_frame(Front))
        flip_but.grid(column=1, row=1)
# class card:
#     def __init__(self, chars, english, pinyin, example):
#         self.chars= chars
#         self.english = english
#         self.pinyin = pinyin
#         self.example = example

# c1=card(chars, english, pinyin, example)

main = Root()
main.mainloop()

# menu stuff to be commented in later

# def quit(root=root):
#     root.destroy()
#
#
# menu = tk.Menu(root)
# root.config(menu=menu)
# file_menu = tk.Menu(menu)
# menu.add_cascade(label = "File", menu=file_menu)
# file_menu.add_command(label="Exit", command=quit)




# class Flashcard:
#     def __init__(self, root, card):
#         self.card=card
#
#     def render_front(self):
#         Quiz = ttk.Label(self.mainframe, text = self.card.chars)
#         Quiz.grid(column=1, row=0)
#         flip_but = ttk.Button(self.bottomframe, text = "flip card") #, command=flipcard)
#         flip_but.grid(column=1, row=1)
#
#     def render_back(self):
#         english = ttk.Label(self.mainframe, text = self.card.english)
#         english.grid(column=1, row=0)
#         pin = ttk.Label(self.mainframe, text = self.card.pinyin)
#         pin.grid(column=1, row=1)
#         ex = ttk.Label(mainframe, text = self.card.example)
#         ex.grid(column=0, columnspan = 3, row=2)
#
#
#
#
# root = tk.Tk()
# root.columnconfigure(0, weight =1)
# root.rowconfigure(0,weight=1)
# root.title("Flashcard app")
# grey = '#D3D3D3'
# s.configure("Frame1.TFrame", background = grey)
# mainframe = ttk.Frame(root, padding="3 3 12 12")
# mainframe.grid(column=0, row=1)
# bottomframe = ttk.Frame(root, style="Frame1.TFrame")
# bottomframe['padding']= (3,3,12,12)
# bottomframe.grid(row = 100, column = 0, columnspan = 100, sticky = 'sew')
# bottomframe.columnconfigure(0, weight = 5)
# f=Flashcard(root, c1)
# f.render_front()
# root.mainloop()
