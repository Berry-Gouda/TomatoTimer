import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from playsound import playsound
import time

#Window Grid Size
GRID_WIDTH = 30
GRID_HIEGHT = 20

#Time Constants
ACTIVE_TIME = 25
MIN_REST = 5
LONG_REST_AFTER = 4
LONG_REST = 20

#Color Constants
ACTIVE_COLOR = "pink4"
REST_COLOR = 'aquamarine'
LR_COLOR = 'lawn green'
COMP_COLOR = 'SlateBlue3'

#Global Refrences
window = tk.Tk()
timer_label_ref = tk.Label()
button_ref = tk.Button()
cancel_ref = tk.Button()
entry_to_delete = tk.Entry()
label_to_delete = tk.Label()
current_round = 0
paused_time = 0.0
total_time = 0
total_active_time = 0
label_list = []

#Pause fonctionality
def pause_countdown(remainingTime, timeToAdd, bIsActive):

    global paused_time
    global total_active_time
    global total_time

    if bIsActive:
        total_active_time += timeToAdd

    total_time += timeToAdd

    paused_time = remainingTime

    button_ref.config(text="Resume Timer")
    button_ref.bind("<Button-1>", start_countdown)

    window.mainloop()

#Resets the Window when 
def finished(event=None):

    global window
    global button_ref
    global total_active_time
    global total_time
    
    for child in window.winfo_children():
        if child == button_ref:
            continue
        child.destroy()


    button_ref.config(text="Start Over")
    button_ref.grid(row=18, column=12, columnspan=5)    
    button_ref.bind("<Button-1>", build_home_page)
    
    tTimeLabel = tk.Label(window, text="Total Time: " + str(total_time/60), bg="black", fg="Red", font=('Helvetica bold', 36))
    tTimeLabel.grid(row=4, column=4, columnspan=10, rowspan=3, sticky='nsew', pady=15)
    tTimeLabel = tk.Label(window, text="Active Time: " + str(total_active_time/60), bg="black", fg="Red", font=('Helvetica bold', 36))
    tTimeLabel.grid(row=8, column=4, columnspan=10, rowspan=3, sticky='nsew', pady=15)

    window.mainloop()


def start_countdown(event=None):

    global current_round
    global timer_label_ref
    global button_ref
    global paused_time
    global total_time
    global total_active_time

    bIsActive = False

    type = label_list[current_round].cget("text")
    
    if type == 'A':
        goalTime = ACTIVE_TIME * 60
        bIsActive = True
    elif type == 'R':
        goalTime = MIN_REST * 60
    else:
        goalTime = LONG_REST * 60

    if paused_time == 0:
        remainingTime = goalTime
    else:
        remainingTime = paused_time
        goalTime = remainingTime
        paused_time = 0
    
    targetTime = time.time() + remainingTime
    
    button_ref.config(text='Pause Timer')
    button_ref.bind("<Button-1>", lambda event : pause_countdown(remainingTime, (goalTime - remainingTime), bIsActive))
    cancel_ref.bind("<Button-1>", finished)
    
    while remainingTime > 0:
        
        currentTime = time.time()
        remainingTime = max(0, int(targetTime - currentTime))

        minutes = remainingTime // 60
        seconds = remainingTime % 60

        displayText = str(minutes) + " : " + str(seconds)
        timer_label_ref.config(text=displayText)

        window.update()



    #plays sounds and updates total times
    if type == 'A':
        playsound("finishactive.mp3")
        total_active_time += goalTime
    elif type == 'R':
        playsound("finishrest.wav")
    else:
        playsound("finishlr.wav")
    
    total_time += goalTime

    label_list[current_round].config(text="", bg=COMP_COLOR)
    current_round += 1

    if current_round >= len(label_list):
        finished(tk.Event)

    button_ref.config(text="Start Timer")
    button_ref.bind("<Button-1>", start_countdown)



    window.mainloop()

    

def build_active_page(loops:int):

    global window
    global button_ref
    global cancel_ref

    totalTimers = int(loops)*2

    startRow = 6
    startColumn = 8
    rowModifier = 0
    columModifier = 0
    activeCounter = 0

    for i in range(totalTimers + 1):
        
        currentColumn = startColumn + columModifier
        currentRow = startRow + rowModifier
        if i == 0:
            continue
        #Builds Long Rest
        if activeCounter == LONG_REST_AFTER:
            activeCounter = 0
            currentRow = startRow + rowModifier
            lrLabel = tk.Label(window, bg=LR_COLOR, fg='black', text='LR')
            lrLabel.grid(row=(currentRow), column=currentColumn, sticky='nsew')
            rowModifier += 2
            columModifier = 0
            label_list.append(lrLabel)
        #Builds Rest
        elif i % 2 == 0:
            trLabel = tk.Label(window, bg=REST_COLOR, fg='black', text = 'R')
            trLabel.grid(row=(currentRow), column=(currentColumn), sticky='nsew')
            columModifier += 2
            label_list.append(trLabel)
        #Builds Active
        else:
            activeCounter += 1
            taLabel = tk.Label(window, bg=ACTIVE_COLOR, fg='black', text='A')
            taLabel.grid(row=(currentRow), column=(currentColumn), sticky='nsew')
            columModifier += 2
            label_list.append(taLabel)
    
    cancelBut = tk.Button(window, background='goldenrod', text='Finish')
    cancel_ref = cancelBut
    button_ref.grid(row=18, column=8, columnspan=5)
    cancelBut.grid(row=18, column=16, columnspan=5)



def start_timer(event):

    global entry_to_delete
    global label_to_delete

    entryRef = entry_to_delete.get()

    if entryRef == '':
        build_home_page()

    entry_to_delete.destroy()
    label_to_delete.destroy()
    build_active_page(entryRef)
    start_countdown()

    

#Builds the page Start to.
def build_home_page(event=None):
    global window
    global timer_label_ref
    global button_ref
    global label_to_delete
    global entry_to_delete

    #Clears any leftover Children when reseting to homepage.
    for child in window.winfo_children():
        child.destroy()

    #Creates the grid used for alignment
    for i in range(GRID_WIDTH):
        window.grid_columnconfigure(i, weight=1, minsize=20, pad=5)
        for j in range(GRID_HIEGHT):
            window.grid_rowconfigure(j, weight=1, minsize=20, pad=5)
            

    count_timer = tk.Label(window, text="00:00",font=('Helvetica bold', 36), bg='black', fg='red')
    count_timer.grid(row=0, rowspan=2, column=11, columnspan=8, pady=15, sticky='nsew')
    timer_label_ref = count_timer

    loop_label = tk.Label(window, text="Number Of Loops", bg='salmon', fg='black')
    loop_label.grid(row=8, column=13, columnspan=3)
    label_to_delete = loop_label

    loop_Entry = tk.Entry(window, bd=2)
    loop_Entry.grid(row = 9, column=12, columnspan=5)
    entry_to_delete = loop_Entry

    start_button = tk.Button(window, background='goldenrod', text='Start Timer')
    start_button.grid(row=18, column=12, columnspan=5)
    button_ref = start_button
    button_ref.bind("<Button-1>", start_timer)

    window.mainloop()

def main():

    global window

    img = PhotoImage(file='icon.png')
    window.tk.call('wm', 'iconphoto', window._w, img)
    window.wm_title("Tomato Timer")
    window.wm_iconname("Tomato Timer")
    window.wm_class = ("Tomato Timer")
    window.title("Tomato Timer")
    window.geometry("900x600")
    window.configure(background="salmon")
    window.maxsize(900, 600)

    build_home_page()





if __name__ == "__main__":
    main()








