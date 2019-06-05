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

#version: 1.2
#attempted rotation
#work on placement of numbers for inputs after rotations

def newshape(event,holding):
    global shapes,dy,dx,shapetype,board,nextshape,nextshapes,shapeboard,held,holdshapes,gameplaying,degree
    if not holding:
        held = False
        for x in range(4):
            canvas.delete(shapes[x])
            shapeboard[shapepoints[shapetype][x] // 4 + dy][shapepoints[shapetype][x] % 4 + dx + 3] = canvas.create_image(
                (shapepoints[shapetype][x] % 4 + dx + 3) * size,
                (shapepoints[shapetype][x] // 4 + dy) * size, anchor=NW,
                image=shapesimg[shapetype])
        for x in range(4):
            board[shapepoints[shapetype][x] // 4 + dy][shapepoints[shapetype][x] % 4 + dx + 3] = 0 - shapetype - 1
            print(x)
        for x in range(boardheight):
            if rowfilled(x):
                for r in range(boardheight):
                    for c in range(boardwidth):
                        canvas.delete(shapeboard[r][c])
                shapeboard = np.delete(shapeboard,x,0)
                newrow2 = np.ndarray((1,boardwidth),dtype=PhotoImage)
                shapeboard = np.concatenate((newrow2,shapeboard),axis=0)
                print(shapeboard)
                board = np.delete(board,x,0)
                newrow = np.zeros((1,boardwidth))
                board = np.concatenate((newrow, board), axis=0)
                print(board)
                for r in range(boardheight):
                    for c in range(boardwidth):
                        if shapeboard[r][c] != None:
                            shapeboard[r][c] = canvas.create_image(c * size,r * size,anchor=NW,image=shapesimg[int(-1-board[r][c])])
        shapetype = nextshape
        nextshape = random.randint(0, 6)
    dy = 0
    dx = 0
    degree = 0
    for x in range(4):
        if not board[shapepoints[shapetype][x] // 4][shapepoints[shapetype][x] % 4 + 3] >= 0:
            gameplaying = False
    if not gameplaying:
        return

    for s in nextshapes:
        canvas.delete(s)
    for s in holdshapes:
        canvas.delete(s)
    #if holding:
        #nextshape = random.randint(0,6)
    nextshapes = []
    holdshapes = []
    for x in range(4):
        if nextshape == 0 or nextshape == 3:
            nextshapes.append(canvas.create_image((shapepoints[nextshape][x] % 4 + 10.5) * size,
                                                  (shapepoints[nextshape][x] // 4 + 10) * size, anchor=NW,
                                                  image=shapesimg[nextshape]))
        else:
            nextshapes.append(
            canvas.create_image((shapepoints[nextshape][x] % 4 + 11) * size,
                                (shapepoints[nextshape][x] // 4 + 10) * size,
                                anchor=NW, image=shapesimg[nextshape]))
    for x in range(4):
        if holdshape == 0 or holdshape == 3:
            holdshapes.append(canvas.create_image((shapepoints[holdshape][x] % 4 + 10.5) * size,
                                                      (shapepoints[holdshape][x] // 4 + 2) * size, anchor=NW,
                                                      image=shapesimg[holdshape]))
        elif holdshape != None:
            holdshapes.append(
                canvas.create_image((shapepoints[holdshape][x] % 4 + 11) * size,
                                    (shapepoints[holdshape][x] // 4 + 2) * size,
                                    anchor=NW, image=shapesimg[holdshape]))
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
    if not gameplaying:
        return
    if event.keysym == "Up":
        rotate(True)
    elif event.keysym == "Down":
        #down another if
        if valid(1):
            downinput(pressed = True)
        else:
            newshape(event,False)
    elif event.keysym == "Left":
        if valid(2):
            leftinput()
    elif event.keysym == "Right":
        if valid(3):
            rightinput()

def downinput(pressed):
    global dy
    if not gameplaying:
        return
    if not valid(1):
        newshape(None,False)
        dy -= 1
    dy +=1
    for s in shapes:
        canvas.delete(s)

    for x in range(4):
        if shapepoints[shapetype][x] // 4 + dy-1 != -1:
            board[shapepoints[shapetype][x] // 4 + dy-1][shapepoints[shapetype][x] % 4 + dx + 3] = 0

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
        shapes[x] = canvas.create_image((shapepoints[shapetype][x] % 4 + dx + 3) * size,
                                            (shapepoints[shapetype][x] // 4 + dy) * size, anchor=NW,
                                            image=shapesimg[shapetype])
    print(board)

def rotate(right):
    def rotatevalid(points,offset):
        for x in range(4):
            #for y in range(2):
            px = points[0]
            py = points[1]
            if not offset:
                px /= size
                py /= size
            print(px)
            if shapepoints[shapetype][x] // 4 + py / size > boardheight - 1:
                print("1")
                return False
            if shapepoints[shapetype][x] % 4 + px + 2 < -1 or shapepoints[shapetype][x] % 4 + px + 1 > 7:
                print("2")
                return False
            #if board[shapepoints[shapetype][x] // 4 + py][
                #shapepoints[shapetype][x] % 4 + 3 + dx] < 0:
                #print("3")
                #return False
           # if board[shapepoints[shapetype][x] // 4 + dy][
               # shapepoints[shapetype][x] % 4 + 3 + px] < 0:
               # print(px)
                #return False
        return True
    def offset():
        global rotationdx,canrotate,fx
        lastdx = rotationdx
        if rotation == 1:
            rotationdx += 1
        else:
            rotationdx -= 1
        rotationdx = rotationdx % 4
        offsetdata = []
        if shapetype == 3:
            offsetdata = offsetI
        else:
            offsetdata = offsetnormal
        for x in range(5):
            bx = offsetdata[x][lastdx]
            cx = offsetdata[x][rotationdx]
            fx = np.subtract(bx,cx)
            #fx = np.expand_dims(fx, axis=0)
            print(fx)
            if rotatevalid(fx, True):
                canrotate = True
                break
        return canrotate
    global degree
    rotation = 1
    if shapetype == 0:
        return
    if right:
        for x in range(shapepoints[shapetype][3] // 4 + dy-1,shapepoints[shapetype][3] // 4 + dy + 3):
            for y in range(shapepoints[shapetype][3] % 4 + dx,shapepoints[shapetype][3] % 4 + dx + 5):
                if board[x][y] == shapetype + 1:
                    board[x][y] = 0
            #board[shapepoints[shapetype][x] % 4 + dx + 3][shapepoints[shapetype][x] // 4 + dy] = 10
        print(board)
        for x in range(4):
            newx = (shapepoints[shapetype][x] % 4 + dx + 3) * size
            newy = (shapepoints[shapetype][x] // 4 + dy) * size
            #pos = [newx - ((shapepoints[shapetype][pivotpoints[shapetype - 1][degree] - 1] % 4 + dx + 3) * size) , newy - (shapepoints[shapetype][pivotpoints[shapetype - 1][degree] - 1] // 4 + dy) * size]

            #a = np.array([[newx],[newy]])
            #p = np.array([[(shapepoints[shapetype][pivotpoints[shapetype - 1][degree] - 1] % 4 + dx + 3) * size],[(shapepoints[shapetype][pivotpoints[shapetype - 1][degree] - 1] // 4 + dy) * size]])
            #print(p)
            #a = a - p
            #if degree == 0:
            #b = np.array([[0,1 * rotation],[-1 * rotation ,0]])
            #c = np.dot(pos,b)
            #px = c[0]
            #py = c[1]
            #newpos = [px,py]
           # newpos[0] += (shapepoints[shapetype][0] % 4 + dx + 3) * size
           # newpos[1] += (shapepoints[shapetype][0] // 4 + dy) * size

           # offset()
            #if rotatevalid(newpos,False):
              #  if canrotate:
              #      print("Heee")
              #      canvas.delete(shapes[x])
              #      shapes[x] = canvas.create_image(newpos[0] + fx[0], newpos[1] + fx[1], anchor=NW,
                  #                                  image=shapesimg[shapetype])
                #else:
                    #canvas.delete(shapes[x])
                    #shapes[x] = canvas.create_image(newpos[0],newpos[1], anchor=NW,
                                                    #image=shapesimg[shapetype])
            a = np.array([[newx], [newy]])
            p = np.array([[(shapepoints[shapetype][pivotpoints[shapetype - 1][degree] - 1] % 4 + dx + 3) * size],
                          [(shapepoints[shapetype][pivotpoints[shapetype - 1][degree] - 1] // 4 + dy) * size]])
            print(p)
            a = a - p
            if degree == 0:
                b = np.array([[0, -1], [1, 0]])
            elif degree == 1:
                b = np.array([[-1, 0], [0, -1]])
            elif degree == 2:
                b = np.array([[0, 1], [-1, 0]])
            elif degree == 3:
                b = np.array([[1, 0], [0, 1]])
            c = np.dot(b, a) + p
            if shapetype == 3:
                if degree == 0:
                    c[1][0] += 40
                elif degree == 1:
                    c[0][0] += 40
                    c[1][0] += 40
                elif degree == 2:
                    c[0][0] -= 40
            print(c[1][0])
            board[int(c[1][0] / 40)][int(c[0][0] / 40)] = shapetype + 1
            canvas.delete(shapes[x])
            shapes[x] = canvas.create_image(c[0][0], c[1][0], anchor=NW,
                                            image=shapesimg[shapetype])
    print(board)
    degree = (degree + 1) % 4

def valid(dir): #up,down,left,right
    px = 0
    py = 0
    if dir == 1:
        py = dy + 1
        px = dx
    elif dir == 2:
        px = dx - 1
    elif dir == 3:
        px = dx + 1

    a = 0
    for x in range(4):
        if shapepoints[shapetype][x] // 4 + py > boardheight - 1:
            print("1")
            return False
        if shapepoints[shapetype][x] % 4 + px + 2 < -1 or shapepoints[shapetype][x] % 4 + px + 1 > 7:
            print("2")
            return False
        if (dir == 0 or dir == 1) and board[shapepoints[shapetype][x] // 4 + py][shapepoints[shapetype][x] % 4 + 3 + dx] < 0:
            print("3")
            return False
        if (dir == 2 or dir == 3) and board[shapepoints[shapetype][x] // 4 + dy][shapepoints[shapetype][x] % 4 + 3 + px] < 0:
            print(px)
            return False
    return True

def hold(event):
    global holdshape,shapetype,held,nextshape
    if holdshape == None:
        holdshape = shapetype
        shapetype = nextshape
        nextshape = random.randint(0, 6)
        held = True
        for s in shapes:
            canvas.delete(s)
        newshape(None, True)
    elif not held:
        temp = holdshape
        holdshape = shapetype
        shapetype = temp
        held = True
        for s in shapes:
            canvas.delete(s)
        newshape(None,True)


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
nextshape = random.randint(0,6)
delay = 1000
degree = 0
holdshape = None
held = False
rotationdx = 0
canrotate = False
fx = np.array([0,0])

board = np.zeros((boardheight,boardwidth))
shapeboard = np.ndarray((boardheight,boardwidth),dtype=PhotoImage)

win = Tk()
win.title('Tetris')
win.resizable(0,0)
canvas = Canvas(win, width=wwidth, height = wheight,bg = "gray",borderwidth=0,highlightthickness=0)
win.bind('<Key>', move)
win.bind("c", hold)
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

pivotpoints = [[4,0,4,0], #S
               [3,3,3,3],#T
               [3,2,3,3],#I
               [3,3,3,3],#Z
               [3,3,3,3],#L
               [3,3,3,3]#J
]
offsetnormal = [[(0,0),(0,0),(0,0),(0,0)],
                [(0,0),(1,0),(0,0),(-1,0)],
                 [(0,0),(1,-1),(0,0),(-1,-1)],
                 [(0,0),(0,2),(0,0),(0,2)],
                 [(0,0),(1,2),(0,0),(-1,2)]]

offsetI =  [[(0,0),(-1,0),(-1,1),(0,1)],
            [(-1,0),(0,0),(1,1),(0,1)],
            [(2,0),(0,0),(-2,1),(0,1)],
            [(-1,0),(0,1),(1,0),(0,-1)],
            [(2,0),(0,-2),(-2,0),(0,2)]]
print(offsetnormal[0][0][0])
nextshapes = []
holdshapes = []
for x in range(4):
    if nextshape == 0 or nextshape == 3:
        nextshapes.append(canvas.create_image((shapepoints[nextshape][x] % 4 + 10.5) * size,(shapepoints[nextshape][x] // 4 + 10)* size,anchor=NW,image= shapesimg[nextshape]))
    else:
        nextshapes.append(
            canvas.create_image((shapepoints[nextshape][x] % 4 + 11) * size, (shapepoints[nextshape][x] // 4 + 10) * size,
                                anchor=NW, image=shapesimg[nextshape]))
#start()
#win.after(delay,downinput,False)
print(board)
win.mainloop()