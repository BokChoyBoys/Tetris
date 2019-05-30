from __future__ import absolute_import, division, print_function
from tkinter import *
import numpy as np
#import pyautogui
import random
from PIL import Image, ImageTk
#import matplotlib
#matplotlib.use("TkAgg")
#from matplotlib import pyplot as plt

class Shape:
    def __init__(self,shape):
        return

def rowfilled(row):
    for x in range(len(row)):
        if board[row][x] == 0:
            return False
    return True

def move(event):
    global i,down,shift,degree
    #shapecoords = np.array((3 + shift) * size, size * (down)),((7 + shift) * size, (down + 1) * size)
    canvas.delete(i)
    if event.keysym == "Up":
        #shapecoords = shapecoords * ((0,-1),(-1,0))
        degree += 1
    elif event.keysym == "Down":
        #down another if
        if down < boardheight - 2:
            downinput()
            down += 1
    elif event.keysym == "Left":
        if shift > -3:
            leftinput()
            shift -= 1
    elif event.keysym == "Right":
        if shift < 3:
            rightinput()
            shift += 1
    i = canvas.create_rectangle(((3 + shift) * size, size * (down)),((7 + shift) * size, (down + 1) * size),fill="#01f0f1")
    #i = canvas.create_rectangle(((4 + shift) * size, size *down),((6 + shift) * size, (down + 2) * size),fill="#f0f001")
    print(board)
def downinput():
    for x in range(4):
        board[down + 1][shift+ x+3] = board[down][shift + x+3]
        board[down][shift + x+3] = 0

def leftinput():
    for x in range(4):
        board[down][shift + 2 + x] = board[down][shift + 3 + x]
        board[down][shift + 3 + x] = 0

def rightinput():
    for x in range(4):
        board[down][7 + shift - x] = board[down][6 + shift - x]
        board[down][6 + shift - x] = 0

boardwidth = 10
boardheight = 20
wwidth = 600
wheight = 800
size = wheight/boardheight
gamestarted = True
degree = 0
rotationtuple = ()
shift = 0
down = 0
toplayerblock = False
board = np.zeros((boardheight,boardwidth))
win = Tk()
win.title('Tetris')
win.resizable(0,0)
canvas = Canvas(win, width=wwidth, height = wheight,bg = "white",borderwidth=0,highlightthickness=0)
win.bind('<Key>', move)
#canvas.bind('<Button-3>',flag)
#win.bind('<space>', restart)
canvas.pack()

for y in range(boardheight):
    canvas.create_line(0,y*(wheight/boardheight), (wheight/boardheight) * (boardwidth),y*(wheight/boardheight))
for x in range(boardwidth):
    canvas.create_line((x+1) * (wheight/boardheight),0,(x+1)*(wheight/boardheight),wheight)
#if not toplayerblock: #change 0 to above
i = canvas.create_rectangle((3 * wheight/boardheight,0,7 * wheight/boardheight, wheight/boardheight),fill = "black")
#i = canvas.create_rectangle(((4 + shift) * size, size *down),((6 + shift) * size, (down + 2) * size),fill = "black")
for x in range(4):
    board[0][x+3] = 1
print(board)
#green 00f000 S
#blue 0101f0 L
#orange efa000 J
#red f00100 Z
#pink a000f1 T
win.mainloop()