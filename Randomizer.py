import tkinter as tk
from tkinter import ttk     # for notebook widget
import random

class Randomizer:

    def __init__(self, root):
        # set-up main window
        self.root = root
        self.root.title("Randomizer")
        self.root.iconbitmap(r'favicon.ico')
        self.root.resizable(0, 0)
        self.rootWidth = 600
        self.rootHeight = 300
        self.xCoordWindow = (self.root.winfo_screenwidth() / 2) - (self.rootWidth / 2)
        self.yCoordWindow = (self.root.winfo_screenheight() / 2) - (self.rootHeight / 2)
        self.root.geometry('%dx%d+%d+%d' % (self.rootWidth, self.rootHeight, self.xCoordWindow, self.yCoordWindow))

        # set-up the 2 main frames
        self.f1 = tk.Frame(root, width=(self.rootWidth / 2), bg='#2E2E2E')      # frame to hold notebook/entries/list on left side
        self.f1.pack(side=tk.LEFT, fill=tk.Y)
        self.f1.pack_propagate(0)
        self.f2 = tk.Frame(root, width=(self.rootWidth / 2), bg='#2E2E2E')      # frame to hold welcome/results on right side
        self.f2.pack(side=tk.RIGHT, fill=tk.Y)
        self.f2.pack_propagate(0)

        # ------ LEFT SIDE ------
        self.nb = ttk.Notebook(self.f1)
        self.nb.pack(expand=tk.TRUE, fill=tk.Y)
        self.tab1 = tk.Frame(self.nb, bg='#2E2E2E', borderwidth=0)
        self.tab2 = tk.Frame(self.nb, bg='#2E2E2E')
        self.nb.add(self.tab1, text='Items'.center(44))
        self.nb.add(self.tab2, text='List'.center(44))

        # ::::::: Tab1 :::::::
        self.labelframe_left = tk.LabelFrame(self.tab1, bg='#2E2E2E', borderwidth=1)
        self.labelframe_left.pack(fill=tk.BOTH, expand=tk.TRUE)

        self.clearItemsButton = tk.Button(self.tab1, text='Clear All'.center(20), pady=3, font='verdana 9 bold', borderwidth=3, bg='#CCF3FF', fg='black')
        self.clearItemsButton.pack(side=tk.LEFT, pady=1, padx=(20, 0))
        self.clearItemsButton.config(command=self.clearEntries)
        
        self.submitItemsButton = tk.Button(self.tab1, text='Submit'.center(20), pady=3, font='verdana 9 bold', borderwidth=3, bg='#CCF3FF', fg='black')
        self.submitItemsButton.pack(side=tk.BOTTOM, pady=1)
        self.submitItemsButton.bind('<ButtonRelease-1>', self.submitEntries)
        
        self.itemEntries = []
        for i in range(10):
            tk.Label(self.labelframe_left, text='Item #' + str(i+1), font='verdana 9', bg='#2E2E2E', fg='#E6DD5B').grid(row=i, column=0, padx=(25, 10), pady=(3, 0))
            self.itemEntries.append(tk.Entry(self.labelframe_left, width=25, justify=tk.CENTER, bg='#F5F5F5', fg='#242424'))
            self.itemEntries[i].grid(row=i, column=1, pady=(3, 0))
        
        for i in range(10):
            self.itemEntries[i].bind('<Return>', self.submitEntries)

        # ::::::: Tab2 :::::::
        self.submitListButton = tk.Button(self.tab2, text='Submit'.center(20), pady=3, font='verdana 9 bold', borderwidth=3, bg='#CCF3FF')
        self.submitListButton.pack(side=tk.BOTTOM, pady=1)
        self.submitListButton.config(command=self.submitList)

        self.scrolly = tk.Scrollbar(self.tab2)
        self.scrolly.pack(side=tk.RIGHT, fill=tk.Y)
        self.textbox = tk.Text(self.tab2, yscrollcommand=self.scrolly.set, wrap=tk.WORD, bg='#F5F5F5', fg='#242424')
        self.textbox.pack()
        self.scrolly.config(command=self.textbox.yview)

        # ------- RIGHT SIDE -------
        self.labelframe_right = tk.LabelFrame(self.f2, bg='#2E2E2E', fg='white', borderwidth=3)
        self.labelframe_right.pack(fill=tk.BOTH, expand=tk.TRUE)

        self.helpFrame = tk.Frame(self.labelframe_right, borderwidth=3, bg='#2E2E2E')
        self.helpFrame.pack()
        tk.Label(self.helpFrame, text='\nWelcome to the Randomizer!\n\n', font='verdana 13 bold', bg='#2E2E2E', fg='#FF5C87').pack()
        tk.Label(self.helpFrame, text='Enter items to get up to 6 back in random order.\n\nUse the List tab to enter more than 10 items if needed, seperated by commas.', font='verdana 10', wrap=290, justify=tk.LEFT, bg='#2E2E2E', fg='#FF5C87').pack()
        
        self.resultFrame = tk.Frame(self.labelframe_right, borderwidth=4, bg='#2E2E2E')
        self.topResultFrame = tk.LabelFrame(self.resultFrame, bg='#3D3D3D', borderwidth=4, padx=5)

        self.resultLabel = []
        self.resultLabel.append(tk.Label(self.topResultFrame, pady=10, font='system 20 bold', wrap=260, bg='#3D3D3D', fg='white'))
        self.resultLabel.append(tk.Label(self.resultFrame, pady=5, font='system 11', wrap=250, bg='#2E2E2E', fg='#FFB3B3'))
        self.resultLabel.append(tk.Label(self.resultFrame, pady=5, font='system 10', wrap=250, bg='#2E2E2E', fg='#FF9E9E'))
        self.resultLabel.append(tk.Label(self.resultFrame, pady=5, font='system 9', wrap=250, bg='#2E2E2E', fg='#FF8A8A'))
        self.resultLabel.append(tk.Label(self.resultFrame, pady=5, font='system 8', wrap=250, bg='#2E2E2E', fg='#FF7575'))
        self.resultLabel.append(tk.Label(self.resultFrame, pady=5, font='system 7', wrap=250, bg='#2E2E2E', fg='#FF6161'))

        self.flag = True                # flag to ensure helpFrame destroy & result grids only happen once

    # clears all 10 entry fields, and brings focus back to first entry field
    def clearEntries(self):
        for i in range(10):
            self.itemEntries[i].delete('0', 'end')
        self.itemEntries[0].focus()
    
    # takes in all 10 entries from 'Items' tab, cleans them up, then calls printResults
    def submitEntries(self, event):

        self.items = [''] * 10
        for i in range(10):                                     # get each entry and strip of any whitespaces on ends
            self.items[i] = self.itemEntries[i].get()
            self.items[i] = self.items[i].strip()

        self.items = [x for x in self.items if x != '']         # ignore any list items that contain nothing (incase user put comma twice)
        random.shuffle(self.items)                              # shuffle the cleaned up item list
        for i in range(6):                                      # append 6 blank spaces incase user enters less than 6 items, so blanks can be printed instead
            self.items.append('')

        self.printResults()

    # takes in string from 'List' tab, splits/cleans it up, then calls printResults
    def submitList(self):

        self.items = self.textbox.get('1.0', 'end-1c')          # take in long string from textbox
        self.items = self.items.split(',')                      # split string into list by commas

        for i in range(len(self.items)):                        # remove whitespaces from ends and remove all new-lines, if any
            self.items[i] = self.items[i].strip()
            self.items[i] = self.items[i].replace('\n', '')

        self.items = [x for x in self.items if x != '']         # ignore any list items that contain nothing (incase user put comma twice)
        random.shuffle(self.items)                              # shuffle the cleaned up item list
        for i in range(6):                                      # append 6 blank spaces incase user enters less than 6 items, so blanks can be printed instead
            self.items.append('')

        self.printResults()
    
    # prints the results of either 'Items' or 'List' tab
    def printResults(self):

        if self.flag and self.items[0] != '':                   # set-up for displaying results; flag ensures it only happens once
            self.helpFrame.destroy()                            # destroy frame with welcome/help messages to display results instead

            self.labelframe_right['text'] = '   Result   '
            self.resultFrame.pack()

            self.resultLabel[0].grid(row=0, column=0)
            self.resultLabel[1].grid(row=1, column=0)
            self.resultLabel[2].grid(row=2, column=0)
            self.resultLabel[3].grid(row=3, column=0)
            self.resultLabel[4].grid(row=4, column=0)
            self.resultLabel[5].grid(row=5, column=0)
            self.flag = False

        if self.items[0] == '':                                 # don't show top result labelframe if no items
            self.topResultFrame.grid_forget()
        else:
            self.topResultFrame.grid(pady=(5, 15), row=0, column=0)

        # printing the results
        for i in range (6):
            self.resultLabel[i]['text'] = self.items[i]


def main():
    master = tk.Tk()
    my_gui = Randomizer(master)
    master.mainloop()

if __name__ == '__main__':
    main()