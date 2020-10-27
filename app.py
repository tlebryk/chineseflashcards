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

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky= (tk.N, tk.W, tk.E, tk.S))
        root.columnconfigure(0, weight =1)
        root.rowconfigure(0,weight=1)
        root.title("Flashcard app")

        Quiz = ttk.Label(mainframe, text = "Filler")

        Quiz.grid(column=1, row = 1)

        # front = tk.Text(master=root, height = 10, width = 20)

        flip = ttk.Button(mainframe, text = "flip card")
        # flip.geometry("10x20")
        flip.grid(column=1, row=2)

root = tk.Tk()
Flash(root)
root.mainloop()
