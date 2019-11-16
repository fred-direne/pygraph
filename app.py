import tkinter as tk
import tkinter.filedialog as fd
from tkinter import messagebox

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.text=tk.Text(self,height=10,width=50)
        self.text.pack()
        menu=tk.Menu(self)
        file_menu=tk.Menu(menu,tearoff=0)
        file_menu.add_command(label="New file")
        file_menu.add_command(label="Open",command=self.choose_file)
        file_menu.add_separator()
        file_menu.add_command(label="Save",command=self.save_file)
        file_menu.add_command(label="Save as...",command=self.save_as_file)
        menu.add_cascade(label="File",menu=file_menu)
        algorithm_menu=tk.Menu(menu,tearoff=0)
        algorithm_menu.add_command(label="Eullerian Path")
        menu.add_cascade(label="Algorithm",menu=algorithm_menu)
        menu.add_command(label="About")
        menu.add_command(label="Quit",command=self.quit)
        self.config(menu=menu)

    def choose_file(self):
        filetypes=(("Plain text files","*.txt"),
                    ("All files", "*"))
        filename=fd.askopenfilename(title="Open file",
                initialdir="/",
                filetypes=filetypes)
        if filename:
            print(filename)

    def save_file(self):
        contents=self.text.get(1.0,tk.END)
        new_file=fd.asksaveasfile(title="Save file",
                    defaultextension=".txt",
                    filetypes=(("Text files","*.txt"),))
        if new_file:
            new_file.write(contents)
            new_file.close()

    def save_as_file(self):
        contents=self.text.get(1.0,tk.END)
        new_file=fd.asksaveasfilename(title="Save file as",
                    defaultextension=".txt",
                    filetypes=(("Text files","*.txt"),))
        if new_file:
            new_file.write(contents)
            new_file.close()

    def quit(self):
        if messagebox.askyesno('Quit','Do you really want to quit?'):
            self.destroy() 

app=App()
app.mainloop()