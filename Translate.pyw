# Python 3.6.4
# Requires TKinter extension TKinterDnD (tkDnD2.8) and TKinterDnD Python wrapper (TKinterDnD2)
    # tkDnD2.8 available at: https://sourceforge.net/projects/tkdnd/
        # copy to \Tcl directory
    # TKinterDnD2 Python wrapper available at: https://sourceforge.net/projects/tkinterdnd/
        # copy to \Lib\site-packages directory

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from math import trunc
import os
import platform
import sys
from TkinterDnD2 import *
try:
    from Tkinter import *
    from ScrolledText import ScrolledText
except ImportError:
    from tkinter import *
    from tkinter.scrolledtext import ScrolledText


window = TkinterDnD.Tk()
window.iconbitmap(os.path.abspath('./copy.ico'))
window.title('Translate 2.0')
window.grid_rowconfigure(5, weight=1, minsize=100)
window.grid_columnconfigure(2, weight=1, minsize=90)
window.grid_columnconfigure(3, weight=1, minsize=100)
window.resizable(0,0)


#functions
def convert_file(inputfile):
    getinput = inputcombovar.get()
    getoutput = outputcombovar.get()
    getformat = formatcombovar.get()

    if getinput == 'Comma':
        stext = ','
    elif getinput == 'Pipe':
        stext = '|'
    elif getinput == 'Tab':
        stext = '\t'
    else:
        stext = '\t'

    if getoutput == 'Comma':
        rtext = ','
        ext = '.csv'
    elif getoutput == 'Pipe':
        rtext = '|'
        ext = '.psv'
    elif getoutput == 'Tab':
        rtext = '\t'
        ext = '.tsv'
    else:
        rtext = '\t'
        ext = '.txt'

    if getformat == '*.txt':
        ext2 = '.txt'
    else:
        ext2 = ext

    #priming read to determine whether input file is an acceptable format
    input = open(inputfile, encoding='utf-8') 
    ii = 1
    for line in input:
        ii = ii + 1
        if ii >= 10:
            break

    #read file and write output
    input = open(inputfile, encoding='utf-8') 
    outputfile = inputfile.split(".")[0] + '-converted' + ext2
    output = open(outputfile, 'w',encoding='utf-8')
    for line in input:
        try:
            output.write(line.replace(stext, rtext))
        except:
            output.close(  )
            os.remove(output)
    output.close(  )
    input.close(  )


def select_file():
    root = tk.Tk()
    root.withdraw()
    files = filedialog.askopenfilenames()
    if files:
        filelist = root.tk.splitlist(files)
        for file in filelist:
            filelistbox.insert(END,file)
    else:
        return None 


def drop_file():
    files = filelistbox.get(0,tk.END)
    if files:
        filelist = window.tk.splitlist(files)
        filesmessage = ''
        filesize = 0
        sizetotal = 0
        runningtotal = 0 

        getoutput = outputcombovar.get() 
        getformat = formatcombovar.get()

        for file in filelist:
            filesize = os.path.getsize(file)
            sizetotal = sizetotal + filesize

        for file in filelist:
            filesize = os.path.getsize(file)
            runningtotal = runningtotal + filesize
            percentage = runningtotal/sizetotal * 100
            pb.grid(column=4,row=9,pady=10)
            pb["value"] = percentage
            pb.update()

            if getoutput == 'Comma':
                ext = '.csv'
            elif getoutput == 'Pipe':
                ext = '.psv'
            elif getoutput == 'Tab':
                ext = '.tsv'
            else:
                ext = '.txt'

            if getformat == '*.txt':
                ext2 = '.txt'
            else:
                ext2 = ext

            try:
                convert_file(file)
                filesmessage = filesmessage + 'Success: ' + file.split(".")[0] + '-converted' + ext2 + '\n\n'
            except UnicodeDecodeError:
                filesmessage = filesmessage + 'Fail: ' + file + '\n\n'

        messagebox.showinfo('Translate Complete',  filesmessage)
        filelistbox.delete(0,tk.END)
        pb['value'] = 0
        pb.grid_remove()

    else:
        return None


def remove_file():
    files = filelistbox.curselection()
    for index in files[::-1]:  
        filelistbox.delete(index)


#GUI widgets
#format combobox dropdown font
window.option_add('*TCombobox*Listbox.font', ('Arial','10'))

#input dropdown and label
Label(text="Input format:",font=("Arial",10)).grid(column=0,columnspan=2,row=0,sticky='W',padx=10,pady=10)
inputcombovar = StringVar()
inputcombovar.set('Tab')
combovals = ['Comma', 'Pipe', 'Tab']
ttk.Combobox(window,textvariable=inputcombovar,values=combovals,state='readonly',font=('Arial','10')).grid(column=0,columnspan=2,row=1,padx=10)

#output dropdown and label
Label(text='Output format:',font=('Arial',10)).grid(column=3,columnspan=2,row=0,sticky='W',padx=10,pady=10)
outputcombovar = StringVar()
outputcombovar.set('Pipe')
ttk.Combobox(window,textvariable=outputcombovar,values=combovals,state='readonly',font=('Arial','10')).grid(column=3,columnspan=2,row=1,sticky='W',padx=10)

#arrow image
arrowimg = tk.PhotoImage(file=os.path.abspath('./arrow.png'))
tk.Label(window, image=arrowimg).grid(column=2,row=0,rowspan=2,sticky='S',padx=10)

#extra label to pad spacing
Label(text='',font=('Arial',10)).grid(column=0,row=3,pady=10)

#files label and add (open dialog window) and remove (remove files from list) buttons
Label(text='File(s):',font=('Arial',10)).grid(column=0,columnspan=2,row=4,sticky='W',pady=10,padx=10)
addimg = tk.PhotoImage(file=os.path.abspath('./add.png'))
tk.Button(window, image=addimg, border=0, command=select_file, cursor='hand2').grid(column=2,row=4,sticky='W',padx=10)
removeimg = tk.PhotoImage(file=os.path.abspath('./remove.png'))
tk.Button(window, image=removeimg, border=0, command=remove_file, cursor='hand2').grid(column=2,row=4,sticky='E')

#listbox and scrollbar
filelistbox = Listbox(window, selectmode='extended', width=1, height=1, font=('Arial',9))
filelistbox.grid(row=5, column=0, columnspan=5, padx=10, pady=5, sticky='NEWS')
scrollbar = Scrollbar(window, orient='vertical')
scrollbar.grid(column=4,row=5,sticky='N'+'S'+'E',padx=10,pady=5)
scrollbar.config( command = filelistbox.yview )
filelistbox.configure(yscrollcommand=scrollbar.set)

#file extension dropdown and label
Label(text='File ending:',font=('Arial',10)).grid(column=3, row=7,sticky='E',pady=10)
formatcombovar = StringVar()
formatcombovar.set('*.txt')
formatcomboval = ['Default', '*.txt']
ttk.Combobox(window,textvariable=formatcombovar,values=formatcomboval,state='readonly',width=7,font=('Arial','10')).grid(column=3,row=8,sticky='E')

#translate button
buttonstyle = ttk.Style()
buttonstyle.configure('TButton', font=('Arial', 10))
ttk.Button(text="Translate file(s)", style='TButton', command=drop_file, cursor='hand2').grid(column=4,row=8,sticky='W',padx=10)

#progress bar
pb = ttk.Progressbar(window, orient='horizontal',mode='determinate')
pb.grid(column=4,row=9,pady=10)
pb.grid_remove()

#extra label with same padding/size as progress bar to prevent window from changing with its reappearance
Label(text='',font=('Arial',10)).grid(column=2,row=9,pady=10)
Label(text='© 2019 Parry Pardun',font=('Arial',8)).grid(column=0,columnspan=2,row=9,sticky='W'+'S')

#tkinterDnD functions 
def drop(event):
    if event.data:
        if event.widget == filelistbox:
            #event.data is a list of filenames as one string;
            files = filelistbox.tk.splitlist(event.data)
            fileslist = filelistbox.get(0,tk.END)
            for f in files:
                if f not in fileslist:
                    if os.path.exists(f):
                        filelistbox.insert('end', f)
    return event.action

#make the listbox drop targets
filelistbox.drop_target_register(DND_FILES, DND_TEXT)

for widget in (filelistbox,):
    widget.dnd_bind('<<Drop>>', drop)

#define drag callbacks
def drag_init_listbox(event):
    #use a tuple as file list
    data = ()
    if filelistbox.curselection():
        data = tuple([listbox.get(i) for i in filelistbox.curselection()])
    #tuples can also be used to specify possible alternatives for
    #action type and DnD type:
    return ((ASK, COPY), (DND_FILES, DND_TEXT), data)

#finally make the widgets a drag source
filelistbox.drag_source_register(1, DND_TEXT, DND_FILES)
filelistbox.dnd_bind('<<DragInitCmd>>', drag_init_listbox)


window.update_idletasks()

window.deiconify()

window.mainloop()