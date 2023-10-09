#!/usr/bin/python3

from tkinter import *
from tkinter.ttk import *

window = Tk()
window.geometry("800x600")
window.title("Swift Lift")

app = Frame(window)
app.pack()

buttonFrame = Frame(window)

greet = Label(app, text="Welcome!", font=("Technology", 70) )

label = Label(
    foreground="black",
    background="white",
)
greet.pack(side=TOP)

button = Button(
    buttonFrame,
    text="Click me #1!",
    width=25,
#    height=5,
#    bg="blue",
#    fg="yellow",
)
button.pack(side=BOTTOM)

button2 = Button(
    buttonFrame,
    text="Click me!",
    width=25,
#    height=5,
#    bg="blue",
#    fg="yellow",
)
button2.pack(side=BOTTOM)

app.pack(padx=1,pady=1)
buttonFrame.pack(padx=10,pady=50)

window.mainloop()
