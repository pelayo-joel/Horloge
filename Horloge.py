from time import *
from tkinter import *
from tkinter import messagebox

'''Code for the clock, supports time set, alarm, AM mode and pause'''

#Creates the main window
mainWindow = Tk()
mainWindow.geometry("400x200")
mainWindow.title("Clock")

#Variables for the actual clock
timeClock = [23, 59, 55]
hourMinSec = {"Hour":23, "MinSec":59}
clock = f"{timeClock[0]}:{timeClock[1]}:{timeClock[2]}"

#Variables used for the Time and alarm setter
timeSet = []
alarmEntry = []
alarmSet = [0, 0, 0]
alarmEnabled = False

#Variables for pause and AM mode
paused = False
AmPmMode = False
mode = "H"

#Creates two frames, one for the clock and the other for the different settings (the one for the settings is layed out as a grid)
clockFrame = Frame(mainWindow, height=200)
clockFrame.pack(expand=True, fill="both")
buttonsFrame = Frame(mainWindow)
buttonsFrame.pack(expand=True, fill="both")
for i in range(2):
    buttonsFrame.rowconfigure(i, weight=1)
    buttonsFrame.columnconfigure(i, weight=1)

#Label for the clock
clockLabel = Label(clockFrame, text=clock, font=("Arial", 30, "bold"), anchor=CENTER)
clockLabel.pack(expand=True, fill="both")

#Utility function to cleanup the Clock and SetAlarm function
def HoursMinSec(alarmMode):
    global timeClock, alarmSet, hourMinSec
    time = [0, 0, 0]
    if alarmMode == True:
        time = alarmSet
    else:
        time = timeClock

    if time[2] > hourMinSec["MinSec"]:
        time[2] -= 60
        if alarmMode == False:
            time[1] += 1
    if time[1] > hourMinSec["MinSec"]:
        time[1] -= 60
        if alarmMode == False:
            time[0] += 1
    if time[0] > hourMinSec["Hour"]:
        time[0] -= 24

    if alarmMode == True:
        alarmSet = time
    else:
        timeClock = time

#The function that recursively updates the clock
def Clock():
    global mode, timeClock, clock
    clock = f"{timeClock[0]}{mode}:{timeClock[1]}m:{timeClock[2]}s"
    timeClock[2] += 1

    HoursMinSec(False)
    Alarm()
    if AmPmMode and timeClock[0] > 12:
        timeClock[0] = 1
        if mode == "AM":
            mode = "PM"
        else:
            mode = "AM"

    clockLabel.config(text=clock)
    mainWindow.update()
    sleep(1)
    mainWindow.after(1000, Clock())

#Function that sets up the inputed time on the clock
def SetTime():
    global timeSet, timeClock, mode, AmPmMode
    for i in range(3):
        try:
            if timeSet[i].get().isalnum():
                timeClock[i] = int(timeSet[i].get())
                if AmPmMode == True:
                    AmPmMode = False
                    mode = "H"
        except:
            messagebox.showerror("Error", "Invalid input")
            break

#Sets up the alarm
def SetAlarm():
    global alarmEntry, alarmSet, alarmEnabled, AmPmMode, mode
    if alarmEnabled == False:
        for i in range(3):
            try:
                if alarmEntry[i].get().isalnum():
                    alarmSet[i] = int(alarmEntry[i].get())
                    HoursMinSec(True)
            except:
                messagebox.showerror("Error", "Invalid input")
                return None
        if AmPmMode == True:
            AmPmMode = False
            mode = "H"
        alarmEnabled = True
        messagebox.showinfo("Alarm", f"Alarm has been set to {alarmSet[0]}H:{alarmSet[1]}m:{alarmSet[2]}s")
    else:
        alarmEnabled = False
        messagebox.showinfo("Alarm", "Alarm disabled")

#The actual alarm, this where i could modify what to perform when the clock reaches the alarm
def Alarm():
    global timeClock, alarmSet, alarmEnabled
    if timeClock == alarmSet and alarmEnabled:
        messagebox.showinfo("Alarm", "Now i'm motivated (alarm now disabled)")
        alarmEnabled = False

#Changes the displayed clock in AmPm mode
def AmPmSet():
    global AmPmMode, mode, timeClock
    if AmPmMode == False:
        AmPmMode = True
        mode = "AM"
        if timeClock[0] > 12:
            timeClock[0] -= 12
            mode = "PM"
        elif timeClock[0] == 0:
            timeClock[0] = 12
    else:
        AmPmMode = False
        if mode == "PM":
            timeClock[0] += 12
        elif mode == "AM" and timeClock[0] == 12:
            timeClock[0] = 0
        mode = "H"

#Handles the pause features
def Pause():
    global paused, timeClock
    if paused == False:
        paused = True
    else:
        paused = False

    pausedAt = timeClock
    clock = f"{pausedAt[0]}{mode}:{pausedAt[1]}m:{pausedAt[2]}s"

    while paused:
        clockLabel.config(text=clock)
        mainWindow.update()

#Sets up the frames for the time and alarm setter, they're both frames because they hold multiple widgets
def TimeEntryFrame():
    global timeSet, alarmSet
    setFrame = Frame(buttonsFrame)
    setFrame.grid(row=0, column=0, sticky=NSEW)
    alarmFrame = Frame(buttonsFrame)
    alarmFrame.grid(row=0, column=1, sticky=NSEW)

    setDict = {setFrame:"Set Time", alarmFrame:"Set Alarm"}

    for frame, label in setDict.items():
        for i in range(3):
            setEntry = Entry(frame, width=5)
            setEntry.pack(side=LEFT, padx=4)
            if frame is setFrame:
                timeSet.append(setEntry)
            elif frame is alarmFrame:
                alarmEntry.append(setEntry)
        if frame is setFrame:
            setButton = Button(frame, text=label, font=("Arial", 10), command=SetTime)
        elif frame is alarmFrame:
            setButton = Button(frame, text=label, font=("Arial", 10), command=SetAlarm)
        setButton.pack(expand=True)

#Utility, creates the different features in buttonsFrame
def Features():
    TimeEntryFrame()
    modeButton = Button(buttonsFrame, text="AM/PM", font=("Arial", 10), command=AmPmSet).grid(row=1, column=0, sticky=NSEW)
    pauseButton = Button(buttonsFrame, text="Pause", font=("Arial", 10), command=Pause).grid(row=1, column=1, sticky=NSEW)
    


def main():
    try:
        Features()
        Clock()
        mainWindow.mainloop()
    except:
        print("Program Closed")





if __name__ == "__main__":
    main()