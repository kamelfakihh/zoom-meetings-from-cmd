import re
import os
import tkinter
from tkinter import END, filedialog, StringVar
import json

zoom_dir = None
meetings = []

# save meetings to a json
def save_meetings():    
    with open("meetings.json", "w") as f :
        json.dump(meetings, f)


# load meetings from json file
def load_meetings():
    global meetings
    try :
        f = open("meetings.json", "r")
        meetings = json.load(f)
    except :
        pass

    for meeting in meetings :
        listbox.insert(END, f"{meeting[0]}  ({meeting[1]})")

# add meeting to list
def add_meeting():

    msg.set('')

    # get link from entry
    meeting_link = link.get()
    meeting_name = name.get()

    if meeting_link :
    
        # add meeting to meetings list
        meetings.append((meeting_name, meeting_link))

        # add meeting to list box
        listbox.insert(END, f"{meeting_name}   ({meeting_link})")

        name.delete(0, END)
        link.delete(0, END)
    else :
        msg.set('you must provide a link')

# start selected meeting
def start_meeting(event = None):

    msg.set('')

    if not zoom_dir.endswith('Zoom.exe') :
        msg.set('please set Zoom.exe directory : file > change zoom directory')
        return
    
    index = listbox.curselection()
    meeting = meetings[index[0]]

    try :
        # find meeting id and hashed password from link
        link_regex = r'(\d+)\?pwd=(\w+)'
        credentials = re.findall(link_regex, meeting[1])
        # create windows command to start the Zoom app
        command = f'{zoom_dir} "--url=zoommtg://zoom.us/join?action=join&confno={credentials[0][0]}&pwd={credentials[0][1]}"'
        msg.set('started meeting')
        os.popen(command)
    except :
        msg.set('please enter a valid link')



# delete only one meeting
def delete_meeting():

    msg.set('')

    index = listbox.curselection()

    # remove meeting from meetings list
    meetings.pop(index[0])

    #remove meeting from list box
    listbox.delete(index)

# delete all meetings
def delete_all_meetings():
    global meetings

    msg.set('')

    # empty meetings list
    meetings.clear()

    # remove meetings from listbox
    listbox.delete(0, END)

# sets Zoom.exe directory
def set_zoom_dir():
    global zoom_dir

    msg.set('')

    filename = filedialog.askopenfilename(initialdir='/', title='select your zoom app', filetypes=[("Zoom App", "Zoom.exe"),("Executables", "*.exe")])
    if filename.endswith('Zoom.exe') :

        zoom_dir = filename
        msg.set('')

        with open('zoom_dir.txt', 'w') as f :
            f.write(zoom_dir) 



tk = tkinter.Tk()
tk.title('open zoom')
tk.geometry('500x500')
tk.resizable(False, False)

# menu bar 
menubar = tkinter.Menu(tk)

# file drop down
file = tkinter.Menu(menubar, tearoff=0)

file.add_command(label='change zoom directory', command=set_zoom_dir)
file.add_command(label='clear all meetings', command=delete_all_meetings)
file.add_command(label='quit', command=tk.quit)

# menu drop down commands
menubar.add_cascade(label='file', menu=file)
menubar.add_command(label='start meeting', command=start_meeting)
menubar.add_command(label='delete meeting', command=delete_meeting)

# add menubar to the main frame
tk.config(menu = menubar)

# Text component to display messages
msg = StringVar()
message = tkinter.Label(tk, textvariable=msg, fg='red')
message.pack()

# list box to view meetings
listbox = tkinter.Listbox(tk , width=500, height=22)
listbox.bind('<Double-1>', start_meeting)
listbox.pack()

# add meeting label
l = tkinter.Label(tk, text='add a new meeting : ', height=2)
l.pack()

# name of entered meeting
name = tkinter.Entry(tk, width=500)
name.insert(END, 'meeting name')
name.pack()

# link of entered meeting
link = tkinter.Entry(tk, width=500)
link.insert(END, 'meeting link')
link.pack()

# button to add meeting
add_meeting = tkinter.Button(tk, text='add meeting', command=add_meeting)
add_meeting.pack()


# set the zoom directory before start
try :
    dir = open('zoom_dir.txt', 'r') 
    zoom_dir = dir.readline()
except :
    pass

if not zoom_dir :
    msg.set('please set Zoom.exe directory : file > change zoom directory')
else :
    msg.set('double click a meeting to start')

load_meetings()
tk.mainloop()
save_meetings()