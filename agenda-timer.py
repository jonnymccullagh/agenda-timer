#!/usr/bin/python

from tkinter import *
from tkinter import ttk
from tkinter import font
import datetime
import json
import os

# ############################################################################
# Configuration Options

timeremaining_warning=240 # When there is only x seconds left change the text to orange to warn the speaker
timeremaining_critical=180 # When there is only x seconds left change the text to red to warn the speaker
fullscreen=False

color_bg="#282c34"
color_mute="#abb2bf"
color_green="#8dc270"
color_highlights="#ffffff"

# You should not need to change anything below
# ############################################################################
def quit(*args):
    root.destroy()

def update_agenda():
    # Get the time remaining until the event
    now = datetime.datetime.now()
    realTime.set(now.strftime('%H:%M'))

    json_file = open('agenda.json')
    json_str = json_file.read()
    data = json.loads(json_str)
    # Count the number of agenda items in the Json file
    numOfSessions=len(data)

    # We need to loop through all the sessions and stop at the current session to get the details of that agenda item
    for i in range(numOfSessions):
        if datetime.datetime.now() < datetime.datetime.strptime(data[i]['endtime'], '%Y%m%d%H%M%S' ):
            currSession = i
            sessionTitle.set(data[i]['title'])
            currentSpeaker.set(data[i]['speaker'])
            break

    endtime = datetime.datetime.strptime(data[currSession]['endtime'], '%Y%m%d%H%M%S')
    remainder = datetime.datetime.strptime(data[currSession]['endtime'], '%Y%m%d%H%M%S') - now
    # remove the microseconds part
    remainder = remainder - datetime.timedelta(microseconds=remainder.microseconds)

    # Set the countdown colour based on the remaining amount of time
    if (datetime.datetime.now()  > (endtime - datetime.timedelta(seconds=timeremaining_warning) ) ):
        lblCountdownTime.configure(foreground='orange')
    elif  (datetime.datetime.now()  > (endtime - datetime.timedelta(seconds=timeremaining_critical) ) ):
        lblCountdownTime.configure(foreground='red')
    else:
        lblCountdownTime.configure(foreground=color_green)
    # Set the text on the Tk Label for Countdown
    remainingTime.set(str(remainder))
    # Trigger the countdown after 1000ms
    root.after(1000, update_agenda)

# Use Tkinter to create the app window
root = Tk()
imgicon = PhotoImage(file=os.path.join(os.path.dirname(os.path.realpath(__file__)),'icon.gif'))
root.tk.call('wm', 'iconphoto', root._w, imgicon)
if (fullscreen):
    root.attributes("-fullscreen", True)
else:
    root.geometry("1024x800")
root.title("Agenda Countdown")
root.configure(background=color_bg)
root.bind("<Escape>", quit)
root.bind("x", quit)
style = ttk.Style()
style.theme_use('classic') # to fix bug on Mac OSX
style.configure("Red.TLabel", fg='red')


# Set the end date and time for the countdown
fntNormal = font.Font(family='Helvetica', size=60, weight='bold')
fntForCountdown = font.Font(family='Helvetica', size=80, weight='bold')
fntForTitle = font.Font(family='Helvetica', size=40, weight='bold')
fntSmall = font.Font(family='Helvetica', size=20, weight='bold')

# Create some Tkinter variables
remainingTime = StringVar()
sessionTitle = StringVar()
realTime = StringVar()
currentSpeaker = StringVar()
numOfSessions = IntVar()
currSession = IntVar()
i = IntVar()
txtTimeRemaining = StringVar()


# Add Tkinter Labels to hold the text elements
lblRealTime = ttk.Label(root, textvariable=realTime, font=fntNormal, foreground=color_mute, background=color_bg)
lblRealTime.place(relx=0.9, rely=0.1, anchor=CENTER)

lblTimeRemaining = ttk.Label(root, textvariable=txtTimeRemaining, font=fntSmall, foreground=color_mute, background=color_bg)
lblTimeRemaining.place(relx=0.5, rely=0.45, anchor=CENTER)
txtTimeRemaining.set('Time Remaining: ')

lblTitle =  ttk.Label(root, textvariable=sessionTitle, font=fntForTitle, foreground=color_highlights, background=color_bg)
lblTitle.place(relx=0.5, rely=0.2, anchor=CENTER)

lblSpeaker =  ttk.Label(root, textvariable=currentSpeaker, font=fntForTitle, foreground=color_highlights, background=color_bg)
lblSpeaker.place(relx=0.5, rely=0.3, anchor=CENTER)

lblCountdownTime = ttk.Label(root, textvariable=remainingTime, font=fntForCountdown, foreground=color_green, background=color_bg)
lblCountdownTime.place(relx=0.5, rely=0.6, anchor=CENTER)

# Run the update_agenda
root.after(1000, update_agenda)
root.mainloop()
