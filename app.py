import tkinter as tk
from tkinter import ttk

def calculate(*args):
    print("not implemented")
    # try:
    #     # value = float(feet.get())
    #     meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
    # except ValueError:
    #     pass
class Flash:

    def __init__(self, root):


        s = ttk.Style()
        grey = '#D3D3D3'

        s.configure("Frame1.TFrame", background = grey)
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0)

        #apologies for odd tk vs ttk choices (experimenting with both)
        bottomframe = ttk.Frame(root, style="Frame1.TFrame")
        bottomframe['padding']= (3,3,12,12)
        bottomframe.grid(row = 100, column = 0, columnspan = 100, sticky = 'sew')
        bottomframe.columnconfigure(0, weight = 5)
        root.columnconfigure(0, weight =1)
        root.rowconfigure(0,weight=1)
        root.title("Flashcard app")

        Quiz = ttk.Label(mainframe, text = "对吗?")
        Quiz.grid(column=0, row=0)
        # , anchor=tk.CENTER)

        # Quiz.place(relx=0.5,rely=0.5, anchor=tk.CENTER)
        # Quiz.grid(column=1, row = 1)

        # front = tk.Text(master=root, height = 10, width = 20)

        flip = ttk.Button(bottomframe, text = "flip card")
        # flip.pack(side=tk.BOTTOM,)
        # flip.geometry("10x20")
        flip.grid(column=0, row=1)

root = tk.Tk()
Flash(root)
root.mainloop()
