import tkinter as tk
from a2_support import*



class View(AbstractGrid):
    
    def __init__(self, master):
        super().__init__(master, (2, 2), (500, 500))
        self.pack()
        self.render()
    
    def render(self):
        self.color_cell((1, 1), 'red')


root = tk.Tk()
root.geometry('500x500')
app = View(root)

root.mainloop()