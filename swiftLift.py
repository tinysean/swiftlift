#!/usr/bin/python3
import tkinter as tk
from fractions import Fraction as frac

from RPi import GPIO
from time import sleep

clk = 17
dt = 18
clkState = 0
dtState = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def click_check(channel):
    clkState = GPIO.input(clk)
    print("click check")
#    print(clkState)
    if (clkState==0):
      print("Clockwise")
      fractionText.set( frac( fractionText.get() ) + frac( globals()["liftDelta"]) )
    elif (clkState==1):
      print("Counter clockwise")
      fractionText.set( frac( fractionText.get() ) - frac( globals()["liftDelta"]) )
    display=format_mixed( frac(fractionText.get()) )

    wholeNum.set(display[0])
    numer.set(display[1])
    denom.set(display[2])

def format_mixed(f):
    """Format the fraction f as a (possibly) mixed fraction.    """
#    if abs(f) <= 1 or f.denominator == 1:
    if abs(f) < 1:
        ''' No mixed fraction needed '''
        if ( (f.numerator == 0) and (f.denominator == 1) ):
            ''' We are at zero man '''
            sep.set('')
            return 0, '', ''

        sep.set('------')
        ''' Welp, what if it's neg but > -1 '''
        if (f.numerator < 0):
            return "-", abs(f.numerator), abs(f.denominator)
        else:
            return '', abs(f.numerator), abs(f.denominator)
    else:
        ''' Figure out mixed fraction. '''
        if ( int((f-int(f)).denominator) == 1 ):
            ''' Whole number only, no fraction.'''
            sep.set('')
            return int(f), '', ''
        else:
            sep.set('------')
            return int(f), abs( (f-int(f)).numerator ), abs( (f-int(f)).denominator )

def show_lan(my_bText,numButton):
    print(my_bText, numButton)

    if (numButton == 0):
        ''' Insert code to reset zero '''
        print("Reset Zero")
        fractionText.set("0")
        wholeNum.set('0')
        denom.set('')
        numer.set('')
        sep.set('')

    if (numButton == 1):
        ''' Insert code for Macro Adjustments '''
        print("Macro")
        globals()["liftDelta"]="1/32"

    if (numButton == 2) or (numButton == 5):
        if (numButton == 2):
            ''' Add liftDelta to current hidden label value '''
            print("Up")
            fractionText.set( frac( fractionText.get() ) + frac( globals()["liftDelta"]) )
        else:
            ''' Subtract liftDelta from current hidden label value '''
            print("Down")
            fractionText.set( frac( fractionText.get() ) - frac( globals()["liftDelta"]) )

        ''' Okay, got the three values, set the display labels '''
        display=format_mixed( frac(fractionText.get()) )

        wholeNum.set(display[0])
        numer.set(display[1])
        denom.set(display[2])

    if (numButton == 3):
        ''' Insert code for auto zero '''
        print("Auto Zero")
        exit(0)

    if (numButton == 4):
        ''' Insert code for micro adjustments '''
        print("Micro")
        globals()["liftDelta"]="1/64"

    if (numButton == 6):
        ''' Insert code for imperial vs metric '''
        print("units toggle from:", globals()["units"])
        if (globals()["units"] == "imp"):
            globals()["units"]="metric"
            ''' Insert code to convert current display to metric '''
        else:
            globals()["units"]="imp"
            ''' Insert code to convert current display to fractions '''

#def buttonPress(event):
#    event.widget.configure(fg = "black")

# Buttons:  Up, Down, Zero Out, Auto Zero, mm/in, Macro Adj, Micro Adj
def create_buttons(container):
    button_frame = tk.Frame(container, bg="Black", borderwidth = 1, border=1, relief=tk.GROOVE )

    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)
    button_frame.columnconfigure(2, weight=1)
    button_frame.rowconfigure(0, weight=1)
    button_frame.rowconfigure(1, weight=1)
    button_frame.rowconfigure(2, weight=1)

    button_list = ("Reset\nZero", "Macro\nAdj", "Up",
                "Auto\nZero", "Micro\nAdj", "Down",
                "in/mm", "", "",
                )

    var = tk.StringVar(None, "Macro\nAdj")
    bCol=0
    bRow=0
    numButton=0

    ''' btnNumber.bind('<ButtonRelease-1>', destroy) '''
    for bText in button_list:
        if (bText == ""):
            button = tk.Button(button_frame, text=bText, bg="Black", fg="White", command=lambda numButton=numButton, 
				lan=bText:show_lan(lan, numButton), state="disabled" )
        elif ( (bText == "Macro\nAdj") or (bText == "Micro\nAdj") ):
            button = tk.Radiobutton(button_frame, text=bText, indicatoron = 0, bg="Black", fg="White",
                    activeforeground="Black", activebackground="White", selectcolor="slate gray",
                    command=lambda numButton=numButton, lan=bText:show_lan(lan, numButton),
                    variable=var, value=bText, font=("ubuntu, bold", 20 ) )
            if ( bText == "Macro\nAdj"):
                button.select()
        else:
            button = tk.Button(button_frame, text=bText, bg="Black", fg="White", command=lambda numButton=numButton, 
				lan=bText:show_lan(lan, numButton), font=("ubuntu, bold", 20) )
#        button.bind('<ButtonRelease-1>', buttonPress)
        button.grid(row=(bRow), column=bCol, sticky="news", padx=5, pady=5)
        bCol+=1
        numButton+=1
        if (bCol >= 3):
            bRow+=1
            bCol=0

    return button_frame

def create_fraction_label(container):
    fraction_frame = tk.Frame(container, bg="Black", borderwidth = 5, border=1, relief=tk.GROOVE )

    hidden_label = tk.Label(fraction_frame, textvariable=fractionText, bg="Black", fg="turquoise1", font=("Ariel", 1) )
    wholeNumber_label = tk.Label(fraction_frame, textvariable=wholeNum, font=("Technology", 40), width=2, bg="Black", fg="turquoise1", justify="left")
    numerNumber_label = tk.Label(fraction_frame, textvariable=numer, font=("Technology", 40), width=2, bg="Black", fg="turquoise1", justify="center")
    denomNumber_label = tk.Label(fraction_frame, textvariable=denom, font=("Technology", 40), width=2, bg="Black", fg="turquoise1", justify="center")
    seperator_label = tk.Label(fraction_frame, textvariable=sep, font=("Technology", 30), bg="Black", fg="turquoise1")

    hidden_label.place(x=500, y=0, width=1, height=1)
    wholeNumber_label.place(x=40, y=130)
    numerNumber_label.place(x=150, y=50)
    seperator_label.place(x=140, y=130)
    denomNumber_label.place(x=150, y=205)

    return fraction_frame

def create_status_label(container):
    status_frame = tk.Frame(container, bg="slate gray", borderwidth = 5, border = 1, relief=tk.SUNKEN )

    label = tk.Label(status_frame, textvariable=statusText, bg="slate gray", fg="black", borderwidth=5, anchor=tk.W, 
			justify="left", font=("ubuntu, bold", 24) )

    label.columnconfigure(0, weight=1)
    label.rowconfigure(0, weight=1)
    label.grid(sticky="W")

    return status_frame

def create_main_window(root):
    print(liftDelta)

    statusText=tk.StringVar()
#    root.resizable(0, 0)

    button_frame=create_buttons(root)
    button_frame.place(x=0, y=0, height=400, width=500)

    fraction_frame=create_fraction_label(root)
    fraction_frame.place(x=500, y=0, height=400, width=300)

    status_label=create_status_label(root)
    status_label.place(x=0, y=400, height=80, width=800)

if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.title('Swift Lift v0.1')
    root.geometry("800x480")

    statusText=tk.StringVar()
    statusText.set("This is some text")
    fractionText=tk.StringVar()
    fractionText.set('0')
    wholeNum=tk.StringVar()
    wholeNum.set('0')
    denom=tk.StringVar()
    denom.set('')
    numer=tk.StringVar()
    numer.set('')
    sep=tk.StringVar()
    sep.set('')

    global liftDelta
    liftDelta="1/32"

    global units
    units="imp"

    GPIO.add_event_detect(dt, GPIO.FALLING, callback=click_check, bouncetime=50)
#    GPIO.add_event_detect(clk, GPIO.FALLING, callback=click_check, bouncetime=200)

    create_main_window(root)
    root.mainloop()

