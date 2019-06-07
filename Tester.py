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

#version: 1.5
#fix hold bug
#work on ai

def newshape(holding):
    global shapes,dy,dx,shapetype,board,nextshape,nextshapes,shapeboard,held,holdshapes,gameplaying,degree,score,totalrowsfilled,level,delay,fx,fxx
    if not holding:
        held = False
        for x in range(4):
            canvas.delete(shapes[x])
            shapeboard[shapepoints[degree][shapetype][x] // 4 + dy +fxx[1]+ fx[1]][shapepoints[degree][shapetype][x] % 4 + dx + 3 +fxx[0] + fx[0]] = canvas.create_image(
                (shapepoints[degree][shapetype][x] % 4 + dx + 3 +fxx[0]+ fx[0]) * size,
                (shapepoints[degree][shapetype][x] // 4 + dy +fxx[1]+ fx[1]) * size, anchor=NW,
                image=shapesimg[shapetype])
        for x in range(4):
            board[shapepoints[degree][shapetype][x] // 4 + dy +fxx[1] + fx[1]][shapepoints[degree][shapetype][x] % 4 + dx + 3 +fxx[0]+ fx[0]] = 0 - shapetype - 1
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
        shapetype = nextshape
        nextshape = random.randint(0, 6)
    dy = 0
    dx = 0
    degree = 0
    fx = np.array([0, 0])
    fxx = fx
    for x in range(boardwidth):
        if board[1][x] < 0:
            gameplaying = False
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
    global i,dy,dx,degree,fx,rotation
   # print(board)
    if not gameplaying:
        return
    if event.keysym == "Up":
        rotation = 1
        rotate()
    elif event.keysym == "z":
        rotation = -1
        rotate()
    elif event.keysym == "Down":
        downinput(pressed = True)
    elif event.keysym == "Left":
        leftinput()
    elif event.keysym == "Right":
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
        newshape(False)
        dy -= 1
    dy +=1
    for s in shapes:
        canvas.delete(s)

    for x in range(boardheight):
        for y in range(boardwidth):
            if board[x][y] > 0:
                board[x][y] = 0
    for x in range(4):
        board[shapepoints[degree][shapetype][x] // 4 + dy + fxx[1]+ fx[1]][shapepoints[degree][shapetype][x] % 4 + dx + 3 +fxx[0]+ fx[0]] = shapetype + 1

    for x in range(4):
        shapes[x] = canvas.create_image((shapepoints[degree][shapetype][x] % 4 + dx + 3 +fxx[0]+ fx[0]) * size, (shapepoints[degree][shapetype][x] // 4 + dy+fxx[1] + fx[1]) * size, anchor=NW,
                             image=shapesimg[shapetype])
    if not pressed:
        win.after(int(delay),downinput,False)
   # print(board)

def leftinput():
    global dx
    if not valid(2):
        return
    for s in shapes:
        canvas.delete(s)
    dx -= 1

    for x in range(boardheight):
        for y in range(boardwidth):
            if board[x][y] > 0:
                board[x][y] = 0
    for x in range(4):
        board[shapepoints[degree][shapetype][x] // 4 + dy +fxx[1]+ fx[1]][shapepoints[degree][shapetype][x] % 4 + dx + 3 +fxx[0]+ fx[0]] = shapetype + 1

    for x in range(4):
        shapes[x] = canvas.create_image((shapepoints[degree][shapetype][x] % 4 + dx + 3 +fxx[0]+ fx[0]) * size,
                                            (shapepoints[degree][shapetype][x] // 4 + dy +fxx[1]+ fx[1]) * size, anchor=NW,
                                            image=shapesimg[shapetype])
   # print(board)

def rightinput():
    global dx
    if not valid(3):
        return
    for s in shapes:
        canvas.delete(s)
    dx += 1

    for x in range(boardheight):
        for y in range(boardwidth):
            if board[x][y] > 0:
                board[x][y] = 0

    for x in range(4):
        board[shapepoints[degree][shapetype][x] // 4 + dy +fxx[1]+ fx[1]][shapepoints[degree][shapetype][x] % 4 + dx + 3 + fxx[0] +fx[0]] = shapetype + 1

    for x in range(4):
        shapes[x] = canvas.create_image((shapepoints[degree][shapetype][x] % 4 + dx + 3 +fxx[0]+ fx[0]) * size,
                                            (shapepoints[degree][shapetype][x] // 4 + dy + fxx[1] + fx[1]) * size, anchor=NW,
                                            image=shapesimg[shapetype])
   # print(board)

def rotatevalid():#points,offset):
    if shapetype == 0:
        return
    for x in range(4):
        newx = (shapepoints[degree][shapetype][x] % 4 + dx + 3 + fx[0] + fxx[0]) * size
        newy = (shapepoints[degree][shapetype][x] // 4 + dy + fx[1] + fxx[1]) * size
        a = np.array([[newx], [newy]])
        p = np.array([[(shapepoints[degree][shapetype][pivotpoints[shapetype - 1][degree] - 1] % 4 + dx + 3 + fx[0] + fxx[0]) * size],
                      [(shapepoints[degree][shapetype][pivotpoints[shapetype - 1][degree] - 1] // 4 + dy + fx[1] + fxx[1]) * size]])
        # print(p)
        a = a - p
        b = np.array([[0, -1 * rotation], [1 * rotation, 0]])
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
            return False
        if c[1][0] > 799:
            return False
        if board[int(c[1][0] / 40)][int(c[0][0] / 40)] < 0:
            return False
    return True

def offset():
    global rotationdx,canrotate,fx,dx,fxx
    if shapetype == 0:
        return
    canrotate = False
    lastdx = degree
    rotationdx = (degree + 1 * rotation) % 4
   # print("attempting offset")
    #fx = np.array([0, 0])
  #  print(degree)
   # print(fx)
    fxx += fx
    if shapetype == 3:
        offsetdata = offsetI
    else:
        offsetdata = offsetnormal
    for x in range(5):
        bx = np.array([offsetdata[x][lastdx][0],offsetdata[x][lastdx][1]])
        #print(bx)
        cx = np.array([offsetdata[x][rotationdx][0],offsetdata[x][rotationdx][1]])
        fx = np.subtract(bx,cx)
      #  print(fx)
        if rotatevalid():
            canrotate = True
           # print("nice")
            break
    #print(board)
    return canrotate

def rotate():
    global degree,fx,dx
    if shapetype == 0:
        return
    if rotatevalid():
        poop = 0
    elif offset():
        poop = 0
    else:
        return
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
        newx = (shapepoints[degree][shapetype][x] % 4 + dx + 3 +fxx[0] + fx[0]) * size
        newy = (shapepoints[degree][shapetype][x] // 4 + dy + fxx[1] +fx[1]) * size

        a = np.array([[newx], [newy]])
        p = np.array([[(shapepoints[degree][shapetype][pivotpoints[shapetype - 1][degree] - 1] % 4 + dx + 3 +fxx[0]+ fx[0]) * size],
                      [(shapepoints[degree][shapetype][pivotpoints[shapetype - 1][degree] - 1] // 4 + dy +fxx[1] + fx[1]) * size]])
       # print(p)
        a = a - p
        b = np.array([[0, -1 * rotation], [1 * rotation, 0]])
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
   # print(board)
    #fx = np.array([0, 0])
    degree = (degree + 1 * rotation) % 4

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
        if shapepoints[degree][shapetype][x] // 4 + dy +fxx[1]+ fx[1] > boardheight-1:
            return False
        if shapepoints[degree][shapetype][x] // 4 + py + fxx[1] + fx[1] > boardheight - 1:
            return False
        if shapepoints[degree][shapetype][x] % 4 + px + 2 + fx[0] + fxx[0]< -1 or shapepoints[degree][shapetype][x] % 4 + px + 1 + fxx[0] + fx[0] > 7:
            return False
        if (dir == 0 or dir == 1) and board[shapepoints[degree][shapetype][x] // 4 + py +fxx[1] +fx[1]][shapepoints[degree][shapetype][x] % 4 + 3 + dx +fxx[0]+ fx[0]] < 0:
            return False
        if (dir == 2 or dir == 3) and board[shapepoints[degree][shapetype][x] // 4 + dy +fxx[1]+ fx[1]][shapepoints[degree][shapetype][x] % 4 + 3 + px +fxx[0]+ fx[0]] < 0:
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
        newshape(True)
    elif not held:
        temp = holdshape
        holdshape = shapetype
        shapetype = temp
        held = True
        for s in shapes:
            canvas.delete(s)
        newshape(True)

def x(event):
    global board
    moveblocks()

def placeblocks(event):
    if board[event.y//40][event.x//40] == 0:
        shapeboard[event.y//40][event.x//40] = canvas.create_image(event.x // 40* size,event.y//40* size, anchor=NW,image=shapesimg[0])
        board[event.y//40][event.x//40] = -10
        #print(board)
    elif board[event.y//40][event.x//40] == -10:
        canvas.delete(shapeboard[event.y//40][event.x//40])
        board[event.y // 40][event.x // 40] = 0
        #print(board)

wwidth = 600
wheight = 800
win = Tk()
win.title('Tetris')
win.resizable(0,0)
canvas = Canvas(win, width=wwidth, height = wheight,bg = "gray",borderwidth=0,highlightthickness=0)
win.bind('<Key>', move)
win.bind("c", hold)
win.bind('<space>', x)
canvas.bind('<Button-1>', placeblocks)
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
rotation = 1
canrotate = False
fx = np.array([0,0])
fxx = fx
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
                 [(0,0),(1,1),(0,0),(-1,1)],
                 [(0,0),(0,-2),(0,0),(0,-2)],
                 [(0,0),(1,-2),(0,0),(-1,-2)]]

offsetI =  [[(0,0),(-1,0),(-1,-1),(0,-1)],
            [(-1,0),(0,0),(1,-1),(0,-1)],
            [(2,0),(0,0),(-2,-1),(0,-1)],
            [(-1,0),(0,-1),(1,0),(0,1)],
            [(2,0),(0,2),(-2,0),(0,-2)]]
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
generation = 1
mutrate = 0.05
data = {}
startboard = np.zeros((boardheight,boardwidth))
generationindex = 0
maxmoves = 500
fitness = 0


def createchildren():
    global data
    data['population'] = []
    for x in range(popsize):
        data['population'].append({
            'id': random.random(),
            'generation': generation,
            'rowsfilled': random.random(),
            'totalheightcols': random.random() - 0.5,
            'numholes': random.random() * 0.5,
            'rigidness': random.random() - 0.5,
            'fitness': 0
        })
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, indent=1)
    evaluate()

def getrowsfilled():
    return totalrowsfilled + 1

def gettotalheightcols():
    totalheight = 0
    for x in range(boardwidth):
        for y in range(boardheight):
            if board[y][x] < 0:
                totalheight += 1
    return totalheight
def getnumholes():
    numholes = 0
    for y in range(boardwidth):
        hashole = False
        for x in range(boardheight):
            if board[x][y] < 0:
                hashole = True
            elif board[x][y] == 0 and hashole:
                numholes += 1
    return numholes

def getrigidness():

    def getcolheight(col):
        height = 0
        for x in range(boardheight):
            if board[x][col] < 0:
                height += 1
        return height

    rigidness = 0
    for x in range(boardwidth-1):
        rigidness += abs(getcolheight(x) - getcolheight(x + 1))
    return rigidness
def getallmoves():
    global board,shapes,dy,dx,fx,fxx,degree,score,fitness,shapeboard
    moverating = 0
    bestmove = -69696969
    testboard = board.copy()
    testshapes = shapes.copy()
    savedscore = score
    fitness = score
    moveset = []
   # print(moveset.shape)
    for rotations in range(4):
        for x in range(-5,5):
            board = testboard.copy()
            for k in range(rotations):
                rotate()
              #  print(board)
            if x < 0:
                for i in range(abs(x)):
                    leftinput()
                   # print(board)
            elif x > 0:
                for j in range(x):
                    rightinput()
                  #  print(board)
            while valid(1):
                downinput(True)
                #print(board)
            moverating += getrowsfilled() * rowsfilled
            moverating += gettotalheightcols() * totalheightcols
            moverating += getnumholes() * numholes
            moverating += getrigidness() * rigidness
            if moverating > bestmove:
                bestmove = moverating
                moveset = [rotations,x]
               # print(bestmove)
                moverating = 0
            #print(bestmove)
        #print(board)
    board = testboard.copy()
    dy = 0
    dx = 0
    fxx = np.array([0,0])
    fx = np.array([0,0])
    degree = 0
    shapeboard = np.ndarray((boardheight, boardwidth), dtype=PhotoImage)
    score = savedscore
   # shapes = testshapes
    #newshape(False)
    #print(moveset)
    return moveset
def moveblocks():
    moves = getallmoves()
    for r in range(int(moves[0])):
        rotate()
    for x in range(abs(int(moves[1]))):
        #print(moves[1])
        if moves[1] < 0:
            leftinput()
        elif moves[1] > 0:
            rightinput()
    while valid(1):
        downinput(True)
    newshape(False)
def restartgame():
    global board,dy,dx,fxx,fx,degree,gameplaying,score,shapeboard
    board = startboard.copy()
    dy = 0
    dx = 0
    fxx = np.array([0, 0])
    fx = np.array([0, 0])
    degree = 0
    score = 0
    gameplaying = True
    shapeboard = np.ndarray((boardheight, boardwidth), dtype=PhotoImage)

def mate():
    global data
    fit = 0
    with open("data.json", "r") as p:
        for s in p:
            if int(s['fitness']) > fit:
                fit = int(s['fitness'])
                print(fit)
def evaluate():
    global rowsfilled,totalheightcols,numholes,rigidness,data,fitness,generationindex
   # print(shapeboard)
    if generationindex == popsize:
        print("Generation done")
        mate()
        return
    print("Poplation" + str(generationindex))

    fitness = 0
    rowsfilled = float(data['population'][generationindex]['rowsfilled'])
    totalheightcols = float(data['population'][generationindex]['totalheightcols'])
    numholes = float(data['population'][generationindex]['numholes'])
    rigidness = float(data['population'][generationindex]['rigidness'])
    while gameplaying:
        moveblocks()
    restartgame()
    with open("data.json", "r") as p: #
        tempdata = json.load(p)
    print(tempdata)

    tempdata['population'][generationindex]['fitness'] = fitness
    with open("data.json", "w") as p:
        json.dump(tempdata, p,indent=1)
    data = tempdata
    print(tempdata['population'][generationindex]['fitness'])
    generationindex += 1
    evaluate()
rowsfilled = 0
totalheightcols = 0
numholes = 0
rigidness = 0

createchildren()
win.mainloop()