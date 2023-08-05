#!/usr/bin/env python3

from tkinter import *
from tkinter.messagebox import *
import requests
import os

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title('OpenCollabo')
        self.pack()

        self.title = Label(self, text="OpenCollabo", font='Helvetica', height=3)
        self.title.pack()

        self.text_field = Entry(self, width=80)
        self.text_field.bind('<Return>', self.send)
        self.text_field.pack()

    def send(self, e):
        text = e.widget.get()

        with open(os.path.expanduser('~/.opencollaborc'), 'r') as f:
            url = f.read().strip()

        headers = {'Content-Type': 'application/json'}
        payload = {'text': text}

        r = requests.post(url, headers=headers, json=payload)

        # Clear
        e.widget.delete(0, last=len(text))

def run():
    root = Tk()
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    run()