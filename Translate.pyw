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
window.title('Translate 1.0')
window.grid_rowconfigure(5, weight=1, minsize=100)
window.grid_columnconfigure(2, weight=1, minsize=90)
window.grid_columnconfigure(3, weight=1, minsize=100)
window.resizable(0,0)


# functions
def convert_file(inputfile):
    varget1 = dropvar1.get()
    varget2 = dropvar2.get()
    varget3 = dropvar3.get()

    if varget1 == 'Comma':
        stext = ','
    elif varget1 == 'Pipe':
        stext = '|'
    elif varget1 == 'Tab':
        stext = '\t'
    else:
        stext = '\t'

    if varget2 == 'Comma':
        rtext = ','
        ext = '.csv'
    elif varget2 == 'Pipe':
        rtext = '|'
        ext = '.psv'
    elif varget2 == 'Tab':
        rtext = '\t'
        ext = '.tsv'
    else:
        rtext = '\t'
        ext = '.txt'

    if varget3 == '*.txt':
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
            listbox1.insert(END,file)
    else:
        return None 


def drop_file():
    files = listbox1.get(0,tk.END)
    if files:
        filelist = window.tk.splitlist(files)
        filesmessage = ''
        filesize = 0
        sizetotal = 0
        runningtotal = 0 

        varget2 = dropvar2.get() 
        varget3 = dropvar3.get()

        for file in filelist:
            filesize = os.path.getsize(file)
            sizetotal = sizetotal + filesize

        for file in filelist:
            filesize = os.path.getsize(file)
            runningtotal = runningtotal + filesize
            percentage = runningtotal/sizetotal * 100
            pb1.grid(column=4,row=9,pady=10)
            pb1["value"] = percentage
            pb1.update()

            if varget2 == 'Comma':
                ext = '.csv'
            elif varget2 == 'Pipe':
                ext = '.psv'
            elif varget2 == 'Tab':
                ext = '.tsv'
            else:
                ext = '.txt'

            if varget3 == '*.txt':
                ext2 = '.txt'
            else:
                ext2 = ext

            try:
                convert_file(file)
                filesmessage = filesmessage + 'Success: ' + file.split(".")[0] + '-converted' + ext2 + '\n\n'
            except UnicodeDecodeError:
                filesmessage = filesmessage + 'Fail: ' + file + '\n\n'

        messagebox.showinfo('Translate Complete',  filesmessage)
        listbox1.delete(0,tk.END)
        pb1['value'] = 0
        pb1.grid_remove()

    else:
        return None

def remove_file():
    files = listbox1.curselection()
    for index in files[::-1]:  
        listbox1.delete(index)


# tkinter widgets
# format combobox dropdown font
window.option_add('*TCombobox*Listbox.font', ('Arial','10'))

# input dropdown and label
label1 = Label(text="Input format:",font=("Arial",10)).grid(column=0,columnspan=2,row=0,sticky='W',padx=10,pady=10)

dropvar1 = StringVar()
dropvar1.set('Tab')
dropval1 = ['Comma', 'Pipe', 'Tab']

drop1 = ttk.Combobox(window,textvariable=dropvar1,values=dropval1,state='readonly',font=('Arial','10')).grid(column=0,columnspan=2,row=1,padx=10)


# output dropdown and label
label2 = Label(text='Output format:',font=('Arial',10)).grid(column=3,columnspan=2,row=0,sticky='W',padx=10,pady=10)

dropvar2 = StringVar()
dropvar2.set('Pipe')

drop2 = ttk.Combobox(window,textvariable=dropvar2,values=dropval1,state='readonly',font=('Arial','10')).grid(column=3,columnspan=2,row=1,sticky='W',padx=10)

# arrow image
arrowimg = tk.PhotoImage(file=os.path.abspath('./arrow.png'))
labelarrow = tk.Label(window, image=arrowimg).grid(column=2,row=0,rowspan=2,sticky='S',padx=10)

#extra label to pad spacing
labelex = Label(text='',font=('Arial',10)).grid(column=0,row=3,pady=10)

# files label and add (open dialog window) and remove (remove files from list) buttons
label4 = Label(text='Files(s):',font=('Arial',10)).grid(column=0,columnspan=2,row=4,sticky='W',pady=10,padx=10)
addimg = tk.PhotoImage(file=os.path.abspath('./add.png'))
button1 = tk.Button(window, image=addimg, border=0, command=select_file, cursor='hand2').grid(column=2,row=4,sticky='W',padx=10)
removeimg = tk.PhotoImage(file=os.path.abspath('./remove.png'))
button3 = tk.Button(window, image=removeimg, border=0, command=remove_file, cursor='hand2').grid(column=2,row=4,sticky='E')


# listbox and scrollbar
listbox1 = Listbox(window, selectmode='extended', width=1, height=1, font=('Arial',9))
listbox1.grid(row=5, column=0, columnspan=5, padx=10, pady=5, sticky='NEWS')
scrollbar = Scrollbar(window, orient='vertical')
scrollbar.grid(column=4,row=5,sticky='N'+'S'+'E',padx=10,pady=5)
scrollbar.config( command = listbox1.yview )
listbox1.configure(yscrollcommand=scrollbar.set)

# file ext dropdown and label
label3 = Label(text='File ending:',font=('Arial',10)).grid(column=3, row=7,sticky='E',pady=10)

dropvar3 = StringVar()
dropvar3.set('*.txt')
dropval3 = ['Default', '*.txt']

drop3 = ttk.Combobox(window,textvariable=dropvar3,values=dropval3,state='readonly',width=7,font=('Arial','10')).grid(column=3,row=8,sticky='E')


# Translate button
# button style
buttonstyle = ttk.Style()
buttonstyle.configure('TButton', font=('Arial', 10))
button2 = ttk.Button(text="Translate file(s)", style='TButton', command=drop_file, cursor='hand2').grid(column=4,row=8,sticky='W',padx=10)


# progress bar
pb1 = ttk.Progressbar(window, orient='horizontal',mode='determinate')
pb1.grid(column=4,row=9,pady=10)
pb1.grid_remove()

label6 = Label(text='© 2018 Parry Pardun',font=('Arial',8)).grid(column=0,columnspan=2,row=9,sticky='W'+'S')

#extra label with same padding/size as progress bar to prevent window from changing with its reappearance
label7 = Label(text='',font=('Arial',10)).grid(column=2,row=9,pady=10)

# tkinterDnD functions 
def drop(event):
    if event.data:
        if event.widget == listbox1:
            # event.data is a list of filenames as one string;
            files = listbox1.tk.splitlist(event.data)
            fileslist = listbox1.get(0,tk.END)
            for f in files:
                if f not in fileslist:
                    if os.path.exists(f):
                        listbox1.insert('end', f)
    return event.action

# make the Listbox drop targets
listbox1.drop_target_register(DND_FILES, DND_TEXT)


for widget in (listbox1,):
    widget.dnd_bind('<<Drop>>', drop)


# define drag callbacks
def drag_init_listbox(event):
    # use a tuple as file list
    data = ()
    if listbox1.curselection():
        data = tuple([listbox.get(i) for i in listbox1.curselection()])
    # tuples can also be used to specify possible alternatives for
    # action type and DnD type:
    return ((ASK, COPY), (DND_FILES, DND_TEXT), data)



# finally make the widgets a drag source
listbox1.drag_source_register(1, DND_TEXT, DND_FILES)
listbox1.dnd_bind('<<DragInitCmd>>', drag_init_listbox)


window.update_idletasks()
window.deiconify()
window.mainloop()


