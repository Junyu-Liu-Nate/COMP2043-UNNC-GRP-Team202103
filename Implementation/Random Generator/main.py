import tkinter as tk
import tkinter.messagebox
import random
from generateInput import generateInput

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
            tkinter.messagebox.showinfo(
                title='Success!', message="Input successfully generated!")
            return

    tkinter.messagebox.showwarning(
        title='Warning', message='Seed should be a number range from 11111 to 65535')


button_generate = tk.Button(
    window, text='Generate random input', font='Verdana', command=checkValid)
button_generate.place(x=150, y=300)

window.mainloop()
