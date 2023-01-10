from tkinter import *
from threading import Event
import time
import sys
import asyncio

sys.stdout.flush()

from numpy import size
root = Tk()
root.title('Traffic Control System')

canvas = Canvas(root, width=700, height=700, bg='blue')
canvas.grid(row=0, column=0, pady=20, padx=20)

canvas.create_line(10, 600, 690, 600, width=2)
canvas.create_line(10, 100, 690, 100, width=15)
canvas.create_line(100, 10, 100, 650, width=15)
canvas.create_line(600, 10, 600, 650, width=15)

entry1 = Entry(root, width=5)
entry2 = Entry(root, width=5)
entry3 = Entry(root, width=5)
entry4 = Entry(root, width=5)
entry5 = Entry(root, width=5)
entry6 = Entry(root, width=5)

canvas.create_window(50, 100, window=entry1)# 300B
canvas.create_window(650, 100, window=entry2)# 400
canvas.create_window(605, 70, window=entry3)# 100
canvas.create_window(50, 600, window=entry4)# 300A
canvas.create_window(105, 625, window=entry5)# 500A
canvas.create_window(650, 600, window=entry6)# 600

canvas.create_text(50, 120, text='<---', fill='red', font=('Helvetica 20 bold'))
canvas.create_text(50, 580, text='--->', fill='green', font=('Helvetica 20 bold'))
canvas.create_text(650, 120, text='<---', fill='green', font=('Helvetica 20 bold'))
canvas.create_text(650, 620, text='--->', fill='red', font=('Helvetica 20 bold'))
canvas.create_text(300, 120, text='<---', fill='yellow', font=('Helvetica 20 bold'))
canvas.create_text(300, 140, text='x4', fill='black', font=('Helvetica 20 bold'))#x4
canvas.create_text(300, 160, text='', fill='white', font=('Helvetica 20 bold'))#x4

canvas.create_text(300, 620, text='--->', fill='yellow', font=('Helvetica 20 bold'))
canvas.create_text(300, 640, text='x1', fill='black', font=('Helvetica 20 bold'))
canvas.create_text(120, 70, text='↑', fill='black', font=('Helvetica 20 bold'))#x3
canvas.create_text(145, 70, text='x3', fill='black', font=('Helvetica 20 bold'))
canvas.create_text(570, 70, text='↓', fill='green', font=('Helvetica 20 bold'))# 100
canvas.create_text(620, 300, text='↓', fill='black', font=('Helvetica 20 bold'))# x5
canvas.create_text(640, 300, text='x5', fill='black', font=('Helvetica 20 bold'))# 100
canvas.create_text(135, 625, text='↑', fill='green', font=('Helvetica 20 bold'))# 500
canvas.create_text(125, 300, text='↑', fill='black', font=('Helvetica 20 bold'))
canvas.create_text(145, 300, text='x2', fill='black', font=('Helvetica 20 bold'))

#traffic lights
canvas.create_text(100, 85, text='.', fill='red', font=('Helvetica 70 bold'))#junction 1
canvas.create_text(602, 85, text='.', fill='red', font=('Helvetica 70 bold'))#junction 2
canvas.create_text(602, 585, text='.', fill='red', font=('Helvetica 70 bold'))#junction 3
canvas.create_text(100, 585, text='.', fill='red', font=('Helvetica 70 bold'))#junction 4


x1=x2=x3=x4=x5=''
j_a=j_b=j_c=j_d=''


def arrange_matrix(matrix_x):
    v = ''
    for row in matrix_x:
        for value in row:
            v+=str(value)
            v+='  '
        v+='\n'
    return v

def changeTrafficLight1(color):
    canvas.create_text(100, 85, text='.', fill=color, font=('Helvetica 70 bold'))#junction 1
    canvas.create_text(602, 85, text='.', fill=color, font=('Helvetica 70 bold'))#junction 2
    canvas.create_text(602, 585, text='.', fill=color, font=('Helvetica 70 bold'))#junction 3
    canvas.create_text(100, 585, text='.', fill=color, font=('Helvetica 70 bold'))#junction 4


def show_x5():
    a=int(entry4.get())+int(entry5.get())
    b=int(entry1.get())
    c=int(entry2.get())+int(entry3.get())
    d=int(entry6.get())

    tMatrix = [
        [1, 1, 0, 0, 0, a],
        [0, 1, -1, 1, 0, b],
        [0, 0, 0, 1, 1, c],
        [1, 0, 0, 0, 1, d]
    ]
    count = 0
    for x in tMatrix[3]:
        tMatrix[3][count] = tMatrix[3][count]-tMatrix[0][count]
        count+=1
    
    Label(actionsFrame, text=arrange_matrix(tMatrix), fg='red').grid(row=4, column=0, padx=10, pady=10)

    count=0
    for x in tMatrix[0]:
        tMatrix[0][count] = tMatrix[0][count]+tMatrix[3][count]
        count+=1

    Label(actionsFrame, text=arrange_matrix(tMatrix), fg='red').grid(row=4, column=1, padx=10, pady=10)

    count=0
    for x in tMatrix[3]:
        tMatrix[3][count] = tMatrix[3][count]+tMatrix[1][count]
        count+=1
    
    Label(actionsFrame, text=arrange_matrix(tMatrix), fg='red').grid(row=5, column=0, padx=10, pady=10)

    count=0
    for x in tMatrix[1]:
        tMatrix[1][count]=tMatrix[1][count]-tMatrix[3][count]
        count+=1
    
    Label(actionsFrame, text=arrange_matrix(tMatrix), fg='red').grid(row=5, column=1, padx=10, pady=10)
    count=0
    for x in tMatrix[2]:
        tMatrix[2][count]=tMatrix[2][count]-tMatrix[3][count]
        count+=1
    
    Label(actionsFrame, text=arrange_matrix(tMatrix), fg='red').grid(row=6, column=0, padx=10, pady=10)
    count=0
    for x in tMatrix[3]:
        tMatrix[3][count] = tMatrix[3][count]+tMatrix[2][count]
        count+=1
    Event().wait(2)
    Label(actionsFrame, text=arrange_matrix(tMatrix), fg='red').grid(row=6, column=1, padx=10, pady=10)

    minValue = min(tMatrix[0][5], tMatrix[3][5])
    x5Label.config(text=f'x5<={minValue}')

    global j_a, j_b, j_c, j_d

    j_a=tMatrix[0][5]
    j_b=tMatrix[1][5]
    j_c=tMatrix[2][5]
    j_d=tMatrix[3][5]

    print(f'{j_a} Ian')

actionsFrame = LabelFrame(root)
actionsFrame.grid(row=0, column=1)

x5Label = Label(actionsFrame, text='', font=('Helvetica 20 bold'))
x5Label.grid(row=0, column=0)

button = Button(actionsFrame, text='Show x5', command=show_x5)
button.grid(row=1, column=0)

x5Entry = Entry(actionsFrame)
x5Entry.grid(row=2, column=1)

Label(actionsFrame, text='Enter Value of x5').grid(row=2, column=0)

def show_other_values():
    Event().wait(2)
    x1=j_a-int(x5Entry.get())
    x2=j_b+int(x5Entry.get())
    x3=j_c
    x4=j_d-int(x5Entry.get())
   
    x1Value.config(text=f'x1:{x1}')
    x2Value.config(text=f'x2:{x2}')
    x3Value.config(text=f'x3:{x3}')
    x4Value.config(text=f'x4:{x4}')

    #time
    street1T=(x3+x4)*1.5
    street2T=(int(x5Entry.get())+x4)*1.5
    street3T=x1*1.5
    street4T=(x3+x4)*1.5

    street1.config(text=f'Street1: {street1T} sec')
    street2.config(text=f'Street2: {street2T} sec')
    street3.config(text=f'Street3: {street3T} sec')
    street4.config(text=f'Street4: {street4T} sec')

showOtherValues = Button(actionsFrame, text='Show Unknown Values', command=show_other_values)
showOtherValues.grid(row=3, column=0)

x1Value = Label(actionsFrame, text='', fg='green')
x1Value.grid(row=7, column=0)

x2Value = Label(actionsFrame, text='', fg='green')
x2Value.grid(row=8, column=0)

x3Value = Label(actionsFrame, text='', fg='green')
x3Value.grid(row=9, column=0)

x4Value = Label(actionsFrame, text='', fg='green')
x4Value.grid(row=10, column=0)

street1 = Label(actionsFrame, text='', fg='red', font=('Helvetica 15 bold'))
street1.grid(row=7, column=1)

street2 = Label(actionsFrame, text='', fg='red', font=('Helvetica 15 bold'))
street2.grid(row=8, column=1)

street3 = Label(actionsFrame, text='', fg='red', font=('Helvetica 15 bold'))
street3.grid(row=9, column=1)

street4 = Label(actionsFrame, text='', fg='red', font=('Helvetica 15 bold'))
street4.grid(row=10, column=1)

def openStreet2():
    canvas.create_text(602, 85, text='.', fill='green', font=('Helvetica 70 bold'))#junction 2
    canvas.create_text(100, 585, text='.', fill='red', font=('Helvetica 70 bold'))#junction 4
    canvas.create_text(100, 85, text='.', fill='green', font=('Helvetica 70 bold'))#junction 1
    canvas.create_text(602, 585, text='.', fill='green', font=('Helvetica 70 bold'))#junction 3

def openStreet4():
     canvas.create_text(100, 585, text='.', fill='green', font=('Helvetica 70 bold'))#junction 4
     canvas.create_text(602, 85, text='.', fill='red', font=('Helvetica 70 bold'))#junction 2
     canvas.create_text(100, 85, text='.', fill='green', font=('Helvetica 70 bold'))#junction 1
     canvas.create_text(602, 585, text='.', fill='green', font=('Helvetica 70 bold'))#junction 3

open2=Button(actionsFrame, text='Open Street 2', command=openStreet2)
open2.grid(column=0, row=11)

open4=Button(actionsFrame, text='Open Street 4', command=openStreet4)
open4.grid(column=1, row=11)

root.mainloop()