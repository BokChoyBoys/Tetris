from __future__ import absolute_import, division, print_function
from tkinter import *
import numpy as np
import time
import math
from PIL import Image, ImageTk
#import pyautogui
import random
from PIL import Image, ImageTk
import json

#version: 1.4
#fix I spawn
#work on drawing score and ai

def newshape(event,holding):
    global shapes,dy,dx,shapetype,board,nextshape,nextshapes,shapeboard,held,holdshapes,gameplaying,degree,score,totalrowsfilled,level,delay,fx
    if not holding:
        held = False
        for x in range(4):
            canvas.delete(shapes[x])
            shapeboard[shapepoints[degree][shapetype][x] // 4 + dy + fx[1]][shapepoints[degree][shapetype][x] % 4 + dx + 3 + fx[0]] = canvas.create_image(
                (shapepoints[degree][shapetype][x] % 4 + dx + 3 + fx[0]) * size,
                (shapepoints[degree][shapetype][x] // 4 + dy + fx[1]) * size, anchor=NW,
                image=shapesimg[shapetype])
        for x in range(4):
            board[shapepoints[degree][shapetype][x] // 4 + dy + fx[1]][shapepoints[degree][shapetype][x] % 4 + dx + 3 + fx[0]] = 0 - shapetype - 1
           # print(x)
        rowsfillednum = 0
        for x in range(boardheight):
            if rowfilled(x):
                rowsfillednum += 1
                totalrowsfilled += 1
                if totalrowsfilled % 10 == 0 and not totalrowsfilled == 0:
                    level += 1
                    updatelevel()
                    delay = delay * 0.9
                    print("Increasing difficulty")
                for r in range(boardheight):
                    for c in range(boardwidth):
                        canvas.delete(shapeboard[r][c])
                shapeboard = np.delete(shapeboard,x,0)
                newrow2 = np.ndarray((1,boardwidth),dtype=PhotoImage)
                shapeboard = np.concatenate((newrow2,shapeboard),axis=0)
                #print(shapeboard)
                board = np.delete(board,x,0)
                newrow = np.zeros((1,boardwidth))
                board = np.concatenate((newrow, board), axis=0)
               # print(board)
                for r in range(boardheight):
                    for c in range(boardwidth):
                        if shapeboard[r][c] != None:
                            shapeboard[r][c] = canvas.create_image(c * size,r * size,anchor=NW,image=shapesimg[int(-1-board[r][c])])
        if rowsfillednum == 1:
            score += 100
        elif rowsfillednum == 2:
            score += 300
        elif rowsfillednum == 3:
            score += 500
        elif rowsfillednum == 4:
            score += 800
        #print(score)
        shapetype = 1
        nextshape = random.randint(0, 6)
    dy = 0
    dx = 0
    degree = 0
    fx = np.array([0, 0])
    for x in range(4):
        if not board[shapepoints[degree][shapetype][x] // 4][shapepoints[degree][shapetype][x] % 4 + 3] >= 0:
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
            nextshapes.append(canvas.create_image((shapepoints[degree][nextshape][x] % 4 + 10.5) * size,
                                                  (shapepoints[degree][nextshape][x] // 4 + 10) * size, anchor=NW,
                                                  image=shapesimg[nextshape]))
        else:
            nextshapes.append(
            canvas.create_image((shapepoints[degree][nextshape][x] % 4 + 11) * size,
                                (shapepoints[degree][nextshape][x] // 4 + 10) * size,
                                anchor=NW, image=shapesimg[nextshape]))
    for x in range(4):
        if holdshape == 0 or holdshape == 3:
            holdshapes.append(canvas.create_image((shapepoints[degree][holdshape][x] % 4 + 10.5) * size,
                                                      (shapepoints[degree][holdshape][x] // 4 + 3) * size, anchor=NW,
                                                      image=shapesimg[holdshape]))
        elif holdshape != None:
            holdshapes.append(
                canvas.create_image((shapepoints[degree][holdshape][x] % 4 + 11) * size,
                                    (shapepoints[degree][holdshape][x] // 4 + 3) * size,
                                    anchor=NW, image=shapesimg[holdshape]))

    shapes = []
    for x in range(4):
        shapes.append(
            canvas.create_image((shapepoints[degree][shapetype][x] % 4 + 3) * size, shapepoints[degree][shapetype][x] // 4 * size,
                                anchor=NW, image=shapesimg[shapetype]))
        board[shapepoints[degree][shapetype][x] // 4][shapepoints[degree][shapetype][x] % 4 + 3] = shapetype + 1
    updatescore()

def rowfilled(row):
    for x in range(boardwidth):
        if board[row][x] == 0:
            return False
    return True

def updatelevel():
    global levelimage
    canvas.delete(levelimage)
    levelimage = canvas.create_text(500,650,fill="darkblue",font="Times 20 italic bold",
                        text=str(level))

def updatescore():
    global scoreimage
    canvas.delete(scoreimage)
    scoreimage = canvas.create_text(500,750,fill="darkblue",font="Times 20 italic bold",
                        text=str(score))
def move(event):
    global i,dy,dx,degree,fx
   # print(board)
    if not gameplaying:
        return
    if event.keysym == "Up":
        if rotatevalid():
            print("here")
            rotate(True)
        #elif offset():
           # print("here2")
            #rotate(True)
            #fx = np.array([0, 0])
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
    global dy,score,fx
    score += 1
    updatescore()
    #fx = np.array([0, 0])
    if not gameplaying:
        return
    if not valid(1):
        #time.sleep(3)
        newshape(None,False)
        dy -= 1
    dy +=1
    for s in shapes:
        canvas.delete(s)

    for x in range(4):
        if shapepoints[degree][shapetype][x] // 4 + dy-1 + fx[1] != -1:
            board[shapepoints[degree][shapetype][x] // 4 + dy-1 + fx[1]][shapepoints[degree][shapetype][x] % 4 + dx + 3 + fx[0]] = 0

    for x in range(4):
        board[shapepoints[degree][shapetype][x] // 4 + dy + fx[1]][shapepoints[degree][shapetype][x] % 4 + dx + 3 + fx[0]] = shapetype + 1

    for x in range(4):
        shapes[x] = canvas.create_image((shapepoints[degree][shapetype][x] % 4 + dx + 3 + fx[0]) * size, (shapepoints[degree][shapetype][x] // 4 + dy + fx[1]) * size, anchor=NW,
                             image=shapesimg[shapetype])
    if not pressed:
        win.after(int(delay),downinput,False)
    print(board)

def leftinput():
    global dx
    for s in shapes:
        canvas.delete(s)
    dx -= 1

    for x in range(4):
        board[shapepoints[degree][shapetype][x] // 4 + dy + fx[1]][shapepoints[degree][shapetype][x] % 4 + dx + 1+ 3 + fx[0]] = 0

    for x in range(4):
        board[shapepoints[degree][shapetype][x] // 4 + dy + fx[1]][shapepoints[degree][shapetype][x] % 4 + dx + 3 + fx[0]] = shapetype + 1

    for x in range(4):
        shapes[x] = canvas.create_image((shapepoints[degree][shapetype][x] % 4 + dx + 3 + fx[0]) * size,
                                            (shapepoints[degree][shapetype][x] // 4 + dy + fx[1]) * size, anchor=NW,
                                            image=shapesimg[shapetype])
    print(board)

def rightinput():
    global dx
    for s in shapes:
        canvas.delete(s)
    dx += 1

    for x in range(4):
        board[shapepoints[degree][shapetype][x] // 4 + dy + fx[1]][shapepoints[degree][shapetype][x] % 4 + dx - 1 + 3 + fx[0]] = 0

    for x in range(4):
        board[shapepoints[degree][shapetype][x] // 4 + dy + fx[1]][shapepoints[degree][shapetype][x] % 4 + dx + 3 + fx[0]] = shapetype + 1

    for x in range(4):
        shapes[x] = canvas.create_image((shapepoints[degree][shapetype][x] % 4 + dx + 3 + fx[0]) * size,
                                            (shapepoints[degree][shapetype][x] // 4 + dy + fx[1]) * size, anchor=NW,
                                            image=shapesimg[shapetype])
    print(board)

def rotatevalid():#points,offset):
    if shapetype == 0:
        return
    for x in range(4):
        newx = (shapepoints[degree][shapetype][x] % 4 + dx + 3 + fx[0] + fxx[0]) * size
        newy = (shapepoints[degree][shapetype][x] // 4 + dy + fx[1] + fxx[1]) * size
        #print(fx[0])
        a = np.array([[newx], [newy]])
        p = np.array([[(shapepoints[degree][shapetype][pivotpoints[shapetype - 1][degree] - 1] % 4 + dx + 3 + fx[0] + fxx[0]) * size],
                      [(shapepoints[degree][shapetype][pivotpoints[shapetype - 1][degree] - 1] // 4 + dy + fx[1] + fxx[1]) * size]])
        # print(p)
        a = a - p
        b = np.array([[0, -1], [1, 0]])
        c = np.dot(b, a) + p
        if shapetype == 3:
            if degree == 0:
                c[1][0] += 40
            elif degree == 1:
                c[0][0] -= 40
            elif degree == 2:
                c[0][0] -= 40
            elif degree == 3:
                c[1][0] -= 40
        if c[0][0] > 399 or c[0][0] < -1:
            print("11")
            return False
        if c[1][0] > 799 or c[1][0] < -1:
            print("22")
            return False
        if board[int(c[1][0] / 40)][int(c[0][0] / 40)] < 0:
            print("33")
            return False
    return True
    #for x in range(4):
        #px = points[0]
        #py = points[1]
        #if not offset:
          #  px /= size
          #  py /= size
      #  if shapepoints[degree][shapetype][x] // 4 + py / size > boardheight - 1:
         #   print("1")
         #   return False
    #    if shapepoints[degree][shapetype][x] % 4 + px + 2 < -1 or shapepoints[degree][shapetype][x] % 4 + px + 1 > 7:
          #  print("2")
          #  return False
   # return True



def offset():
    global rotationdx,canrotate,fx,dx,fxx
    lastdx = rotationdx
    rotationdx += 1
    rotationdx %= 4
    offsetdata = []
    fxx = fx
    if shapetype == 3:
        offsetdata = offsetI
    else:
        offsetdata = offsetnormal
    for x in range(5):
        bx = np.array([offsetdata[x][lastdx][0],offsetdata[x][lastdx][1]])
        #print(bx)
        cx = np.array([offsetdata[x][rotationdx][0],offsetdata[x][rotationdx][1]])
        fx = np.subtract(bx,cx)
       # print(fx)
        if rotatevalid():
            canrotate = True
            break
    print(fx)
    return canrotate

def rotate(right):
    global degree,fx,dx
    rotation = 1
    if shapetype == 0:
        return
    if right:
        for x in range(boardheight):
            for y in range(boardwidth):
                if board[x][y] > 0:
                    board[x][y] = 0
        #for x in range(4):
            #board[shapepoints[degree][shapetype][x] // 4 + dy + fx[1]][shapepoints[degree][shapetype][x] % 4 + dx + 3 + fx[0]] = 0
           # print(board)
            #board[shapepoints[shapetype][x] % 4 + dx + 3][shapepoints[shapetype][x] // 4 + dy] = 10
        #print(board)
        for x in range(4):
            newx = (shapepoints[degree][shapetype][x] % 4 + dx + 3 + fx[0]) * size
            newy = (shapepoints[degree][shapetype][x] // 4 + dy + fx[1]) * size

            a = np.array([[newx], [newy]])
            p = np.array([[(shapepoints[degree][shapetype][pivotpoints[shapetype - 1][degree] - 1] % 4 + dx + 3 + fx[0]) * size],
                          [(shapepoints[degree][shapetype][pivotpoints[shapetype - 1][degree] - 1] // 4 + dy + fx[1]) * size]])
           # print(p)
            a = a - p
            b = np.array([[0, -1], [1, 0]])
            c = np.dot(b, a) + p
            if shapetype == 3:
                if degree == 0:
                    c[1][0] += 40
                elif degree == 1:
                    c[0][0] -= 40
                elif degree == 2:
                    c[0][0] -= 40
                elif degree == 3:
                    c[1][0] -= 40
          #  print(c[1][0])
            board[int((c[1][0])/ 40)][int((c[0][0])/ 40)] = shapetype + 1
           # print(board)
            #if offset():
            canvas.delete(shapes[x])
            shapes[x] = canvas.create_image(c[0][0], c[1][0], anchor=NW,
                                            image=shapesimg[shapetype])
    print(board)
    #fx = np.array([0, 0])
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
        if shapepoints[degree][shapetype][x] // 4 + py + fx[1] > boardheight - 1:
            print("1")
            return False
        if shapepoints[degree][shapetype][x] % 4 + px + 2 + fx[0]< -1 or shapepoints[degree][shapetype][x] % 4 + px + 1 + fx[0] > 7:
            print(board)
            print("2")
            return False
        if (dir == 0 or dir == 1) and board[shapepoints[degree][shapetype][x] // 4 + py + fx[1]][shapepoints[degree][shapetype][x] % 4 + 3 + dx + fx[0]] < 0:
            print("3")
            return False
        if (dir == 2 or dir == 3) and board[shapepoints[degree][shapetype][x] // 4 + dy + fx[1]][shapepoints[degree][shapetype][x] % 4 + 3 + px + fx[0]] < 0:
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

def x(event):
    global fx
    fx = np.array([0, 0])
wwidth = 600
wheight = 800
win = Tk()
win.title('Tetris')
win.resizable(0,0)
canvas = Canvas(win, width=wwidth, height = wheight,bg = "gray",borderwidth=0,highlightthickness=0)
win.bind('<Key>', move)
win.bind("c", hold)
win.bind('<space>', x)
canvas.pack()

boardwidth = 10
boardheight = 20
size = wheight/boardheight
gameplaying = True
dx = 0
dy = 0
toplayerblock = False
shapetype = random.randint(0,6)
nextshape = random.randint(0,6)
delay = 750
degree = 0
holdshape = None
held = False
rotationdx = 0
canrotate = False
fx = np.array([0,0])
fxx = fx
print(fx)
offsetrotate = 0
score = 0
totalrowsfilled = 0
level = 1
levelimage = canvas.create_text(500,650,fill="darkblue",font="Times 20 italic bold",
                        text=str(level))
scoreimage = canvas.create_text(500,750,fill="darkblue",font="Times 20 italic bold",
                        text=str(score))

board = np.zeros((boardheight,boardwidth))
shapeboard = np.ndarray((boardheight,boardwidth),dtype=PhotoImage)

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
shapepoints = [[[1,2,5,6], #O
               [1,2,4,5], #S
               [1,4,5,6],#T
               [4,5,6,7],#I
               [0,1,5,6],#Z
               [2,4,5,6],#L
               [0,4,5,6]],#J
               [[1,2,5,6], #O
                [1,5,6,10],#S
                [1,5,6,9], #T
                [2,6,10,14], #I
                [2,5,6,9],#Z
                [1,5,9,10],#L
                [1,2,5,9]],#J
               [[1,2,5,6],#O
                [5,6,8,9],#S
                [4,5,6,9],#T
                [8,9,10,11],#I
                [4,5,9,10],#Z
                [4,5,6,8],#L
                [4,5,6,10]],#J
                [[1,2,5,6],
                 [0,4,5,9],
                 [1,4,5,9],
                 [1,5,9,13],
                 [1,4,5,8],
                 [0,1,5,9],
                 [1,5,8,9]]
]
shapes = []
for x in range(4):
    shapes.append(canvas.create_image((shapepoints[0][shapetype][x] % 4 + 3) * size,shapepoints[0][shapetype][x] // 4* size,anchor=NW,image= shapesimg[shapetype]))
    board[shapepoints[0][shapetype][x] // 4][shapepoints[0][shapetype][x] % 4 + 3] = shapetype + 1

pivotpoints = [[4,2,1,3], #S
               [3,2,2,3],#T
               [3,3,3,3],#I
               [3,2,2,3],#Z
               [3,2,2,3],#L
               [3,3,2,2]#J
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
#print(offsetnormal[0][0][0])
nextshapes = []
holdshapes = []
for x in range(4):
    if nextshape == 0 or nextshape == 3:
        nextshapes.append(canvas.create_image((shapepoints[0][nextshape][x] % 4 + 10.5) * size,(shapepoints[0][nextshape][x] // 4 + 10)* size,anchor=NW,image= shapesimg[nextshape]))
    else:
        nextshapes.append(
            canvas.create_image((shapepoints[0][nextshape][x] % 4 + 11) * size, (shapepoints[0][nextshape][x] // 4 + 10) * size,
                                anchor=NW, image=shapesimg[nextshape]))
#start()
canvas.create_text(500,600,fill="darkblue",font="Times 20 italic bold",
                        text="Level")
canvas.create_text(500,700,fill="darkblue",font="Times 20 italic bold",
                        text="Score")
imagenext = ImageTk.PhotoImage(Image.open("next.jpg"))
canvas.create_image(500,320,image=imagenext)
imagehold = ImageTk.PhotoImage(Image.open("hold.jpg"))
canvas.create_image(500,50,image=imagehold)
#win.after(int(delay),downinput,False)
#print(board)

popsize = 10
generation = 0
mutrate = 0.05
data = {}


with open('data.json', 'w') as outfile:
    json.dump(data, outfile,indent= 2)
    #outfile.write('\n')

def createchildren():
    global data
    data['population'] = []
    for x in range(popsize):
        data['population'].append({
            'id': random.random(),
            'rowsfilled': random.random(),
            'totalheightcols': random.random(),
            'totalrowsfilled': random.random(),
            'numholes': random.random(),
            'rigidness': random.random()
        })

def evaluate():
    return
win.mainloop()