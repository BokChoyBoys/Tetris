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
    def __init__(self):
        return

def rowfilled(row):
    for x in range(len(row)):
        if board[row][x] == 0:
            return False
    return True

def move(event):
    if event.keysym == "Up":
        print("up")
    if event.keysym == "Down":
        print("down")
    if event.keysym == "Left":
        print("left")
    if event.keysym == "Right":
        print("right")

boardwidth = 10
boardheight = 20
wwidth = 480
wheight = 800
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

print(board)
win.mainloop()