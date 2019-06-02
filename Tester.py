from __future__ import absolute_import, division, print_function
from tkinter import *
import numpy as np
import time
import math
from PIL import Image, ImageTk
#import pyautogui
import random
from PIL import Image, ImageTk
#import matplotlib
#matplotlib.use("TkAgg")
#from matplotlib import pyplot as plt

class Shape:
    def __init__(self,shape):
        return

def newshape(event):
    if rowfilled(19):
        print("nice")
    global shapes,dy,dx,shapetype,board
    for x in range(4):
        board[shapepoints[shapetype][x] // 4 + dy][shapepoints[shapetype][x] % 4 + dx + 3] = -1
    dy = 0
    dx = 0
    shapetype = random.randint(0,6)
    shapes = []
    for x in range(4):
        shapes.append(
            canvas.create_image((shapepoints[shapetype][x] % 4 + 3) * size, shapepoints[shapetype][x] // 4 * size,
                                anchor=NW, image=shapesimg[shapetype]))
        board[shapepoints[shapetype][x] // 4][shapepoints[shapetype][x] % 4 + 3] = shapetype + 1
def rowfilled(row):
    for x in range(boardwidth):
        if board[row][x] == 0:
            return False
    return True

def move(event):
    global i,dy,dx,degree
    if event.keysym == "Up":
        return
    elif event.keysym == "Down":
        #down another if
        if valid(1):
            downinput(pressed = True)
        else:
            newshape(event)
    elif event.keysym == "Left":
        if valid(2):
            leftinput()
    elif event.keysym == "Right":
        if valid(3):
            rightinput()

def downinput(pressed):
    global dy
    if not valid(1):
        newshape(None)
        dy -= 1
    for s in shapes:
        canvas.delete(s)
    dy += 1

    for x in range(4):
        board[shapepoints[shapetype][x] // 4 + dy - 1][shapepoints[shapetype][x] % 4 + dx + 3] = 0

    for x in range(4):
        board[shapepoints[shapetype][x] // 4 + dy][shapepoints[shapetype][x] % 4 + dx + 3] = shapetype + 1

    for x in range(4):
         shapes[x] = canvas.create_image((shapepoints[shapetype][x] % 4 + dx + 3) * size, (shapepoints[shapetype][x] // 4 + dy) * size, anchor=NW,
                             image=shapesimg[shapetype])
    if not pressed:
        win.after(delay,downinput,False)
    print(board)

def leftinput():
    global dx
    for s in shapes:
        canvas.delete(s)
    dx -= 1

    for x in range(4):
        board[shapepoints[shapetype][x] // 4 + dy][shapepoints[shapetype][x] % 4 + dx + 1+ 3] = 0

    for x in range(4):
        board[shapepoints[shapetype][x] // 4 + dy][shapepoints[shapetype][x] % 4 + dx + 3] = shapetype + 1

    for x in range(4):
        shapes[x] = canvas.create_image((shapepoints[shapetype][x] % 4 + dx + 3) * size,
                                            (shapepoints[shapetype][x] // 4 + dy) * size, anchor=NW,
                                            image=shapesimg[shapetype])
    print(board)

def rightinput():
    global dx
    for s in shapes:
        canvas.delete(s)
    dx += 1

    for x in range(4):
        board[shapepoints[shapetype][x] // 4 + dy][shapepoints[shapetype][x] % 4 + dx - 1 + 3] = 0

    for x in range(4):
        board[shapepoints[shapetype][x] // 4 + dy][shapepoints[shapetype][x] % 4 + dx + 3] = shapetype + 1

    for x in range(4):
        shapes[3 - x] = canvas.create_image((shapepoints[shapetype][3 - x] % 4 + dx + 3) * size,
                                            (shapepoints[shapetype][3 - x] // 4 + dy) * size, anchor=NW,
                                            image=shapesimg[shapetype])
    print(board)

def rotate(right):
    if right:

        return

def valid(dir): #up,down,left,right
    px = 0
    py = 0
    if dir == 0:
        px = dx + 1
        return
    if dir == 1:
        py = dy + 1
        px = dx
    if dir == 2:
        px = dx - 1
    if dir == 3:
        px = dx + 1

    a = 0
    for x in range(4):
        if shapepoints[shapetype][x] // 4 + py > boardheight - 1:
            print("1")
            return False
        if shapepoints[shapetype][x] % 4 + px + 2 < -1 or shapepoints[shapetype][x] % 4 + px + 1 > 7:
            print("2")
            return False
        if (dir == 0 or dir == 1) and board[shapepoints[shapetype][x] // 4 + py][shapepoints[shapetype][x] % 4 + 3 + dx] == -1:
            print("3")
            return False
        if (dir == 2 or dir == 3) and board[shapepoints[shapetype][x] // 4 + dy][shapepoints[shapetype][x] % 4 + 3 + px] == -1:
            print(px)
            return False
    return True

boardwidth = 10
boardheight = 20
wwidth = 600
wheight = 800
size = wheight/boardheight
gameplaying = True
dx = 0
dy = 0
toplayerblock = False
shapetype = random.randint(0,6)
delay = 1000

board = np.zeros((boardheight,boardwidth))

win = Tk()
win.title('Tetris')
win.resizable(0,0)
canvas = Canvas(win, width=wwidth, height = wheight,bg = "white",borderwidth=0,highlightthickness=0)
win.bind('<Key>', move)
win.bind('<space>', newshape)
canvas.pack()

for y in range(boardheight):
    canvas.create_line(0,y*(wheight/boardheight), (wheight/boardheight) * (boardwidth),y*(wheight/boardheight))
for x in range(boardwidth):
    canvas.create_line((x+1) * (wheight/boardheight),0,(x+1)*(wheight/boardheight),wheight)

tiles = Image.open("tiles.jpg")
tiles = tiles.resize((280,40), Image.ANTIALIAS)
shapesimg = [
    ImageTk.PhotoImage(tiles.crop((0,0,size,size))), #O [0]
    ImageTk.PhotoImage(tiles.crop((size,0,size * 2,size))), #S [1]
    ImageTk.PhotoImage(tiles.crop((size * 2,0,size * 3,size))), #T [2]
    ImageTk.PhotoImage(tiles.crop((size * 3,0,size * 4,size))), #I [3]
    ImageTk.PhotoImage(tiles.crop((size * 4, 0, size * 5, size))), #Z [4]
    ImageTk.PhotoImage(tiles.crop((size * 5,0,size * 6,size))), #L [5]
    ImageTk.PhotoImage(tiles.crop((size * 6,0,size * 7,size))), #J [6]
    ]
shapepoints = [[1,2,5,6], #same indices as above
               [1,2,4,5],
               [1,4,5,6],
               [0,1,2,3],
               [0,1,5,6],
               [2,4,5,6],
               [0,4,5,6],
]
shapes = []
for x in range(4):
    shapes.append(canvas.create_image((shapepoints[shapetype][x] % 4 + 3) * size,shapepoints[shapetype][x] // 4* size,anchor=NW,image= shapesimg[shapetype]))
    board[shapepoints[shapetype][x] // 4][shapepoints[shapetype][x] % 4 + 3] = shapetype + 1
#start()
#win.after(delay,downinput,False)
print(board)
win.mainloop()