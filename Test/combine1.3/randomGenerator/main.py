import tkinter as tk
import tkinter.messagebox
import random
from tkinter import *
from generateInput import generateInput


def rgGUI():
    window = tk.Tk()
    window.title('Random Input Generator')
    window.geometry('500x500')

    label_seed = tk.Label(
        window, text='Seed (range from 11111 to 65535):', font='Verdana')
    label_seed.place(x=100, y=50)

    entry_seed = tk.Entry(window, show=None, font='Verdana', width=10)
    entry_seed.place(x=200, y=80)

    def generateRandomSeed():
        entry_seed.delete(0, tk.END)
        entry_seed.insert(0, random.randint(11111, 65535))

    button_seed = tk.Button(window, text='Generate random seed',
                            font='Verdana', command=generateRandomSeed)
    button_seed.place(x=152, y=110)

    def checkValid():
        seed = entry_seed.get()
        if len(seed) == 0:
            tkinter.messagebox.showwarning(
                title='Warning', message='Please input seed first!')
            return

        if seed.isdigit():
            seed = int(seed)
            if seed <= 65535 and seed >= 11111:
                generateInput(seed)
                Q = tkinter.messagebox.askyesno(
                    title='Success!', message="Input successfully generated!\nDo you want to check the result?")
                window.destroy()
                with open("resource/sample_input.txt", "r") as patternSeclect:
                    if (patternSeclect.read(1) == '#'):
                        patternNum = 1
                    else:
                        patternNum = 2
                if Q:
                    windowShow = tk.Tk()
                    windowShow.title('Random Input Result')
                    windowShow.geometry('1230x800')
                    with open("resource/sample_input.txt", "r") as f:
                        data = f.read()

                    scroll_v = Scrollbar(windowShow)
                    scroll_v.pack(side=RIGHT, fill="y")

                    # Add a Horizontal Scrollbar
                    scroll_h = Scrollbar(windowShow, orient=HORIZONTAL)
                    scroll_h.pack(side=BOTTOM, fill="x")
                    # Add a Text widget
                    text = Text(windowShow, height=500, width=350, yscrollcommand=scroll_v.set,
                                xscrollcommand=scroll_h.set, wrap=NONE, font=('Helvetica 15'))
                    text.pack(fill=BOTH, expand=0)
                    text.insert(END, data)
                    text.configure(state='disabled')

                    # Attact the scrollbar with the text widget
                    scroll_h.config(command=text.xview)
                    scroll_v.config(command=text.yview)
                return

        tkinter.messagebox.showwarning(
            title='Warning', message='Seed should be a number range from 11111 to 65535')

    button_generate = tk.Button(
        window, text='Generate random input', font='Verdana', command=checkValid)
    button_generate.place(x=150, y=300)

    window.mainloop()
