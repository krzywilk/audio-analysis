import tkinter as tk


class MasterView:
    """src https://stackoverflow.com/questions/16115378/tkinter-example-code-for-multiple-windows-why-wont-buttons-load-correctly"""

    def __init__(self, master, views):
        self.master = master
        self.master.title("Analysis options window")
        self.master.geometry("400x400")
        self.frame = tk.Frame(self.master)
        for view in views:
            self.new_button(*view)
        self.frame.pack()

    def new_button(self, text, title, _class):
        tk.Button(self.frame, text=text, width=25, command=lambda: self.new_window(_class, title)).pack()

    def new_window(self, title,_class):
        new_window = tk.Toplevel(self.master)
        _class(new_window, title)
