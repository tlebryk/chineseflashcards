import tkinter as tk

# inheritance: inherit all the methods froma root tk.TK() window.
# some methods here: http://epydoc.sourceforge.net/stdlib/Tkinter.Tk-class.html
class testing(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        # stick to top, and expand to fill entire space
        # With full frame, this makes sense
        container.pack(side = "top", fill = "both", expand = "True")
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}

        for F in (StartPage,PageOne):

            frame = F(container,self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, controller):
        # find desired frame from dictionary
        # ie frame with key passed by controller
        frame = self.frames[controller]
        # bring frame to the front.
        frame.tkraise()

# adding new pages
# inherit all the tk.frame methods
# also tk.Frame__.init__() will auto be called.
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        #
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font = ("Verdana", 12))
        label.pack(pady=10, padx=10)
        button1 = tk.Button(self, text= "Start Studying",
            command = lambda: controller.show_frame(PageOne))
        button1.pack()

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One", font = ("Verdana", 12))
        label.pack(pady=10, padx=10)
        button1 = tk.Button(self, text= "Return home",
            command = lambda: controller.show_frame(StartPage))
        button1.pack()

app=testing()
app.mainloop()
