# main.py
# Authors: Katie Adiletta and Brendan Roy
# Date created: January 7th, 2025.

# This implements the functionality of Conway's Game of Life. After starting
# the program, the user can choose to use the default starting position or a
# unique one. This implementation also incorporates a mutation feature, that
# 
# Rules of the game:

# Any live cell with fewer than two live neighbours dies (underpopulation)
# Any live cell with two or three live neighbours lives on
# Any live cell with more than three live neighbours dies (overpopulation)
# Any dead cell with exactly three live neighbours becomes alive (reproduction)
# Note: a neighbor of a cell is defined as any cell that borders it, including
#       diagonally. i.e. [row - 1][col - 1] is a neighbor of [row][col]
    

from cell import Cell

from tkinter import *
from PIL import Image, ImageDraw, ImageFont, ImageTk
import time
import random



# mutate
# if we have a mutation, then flip a random neighbor of a random alive cell
def mutate(gameBoard):
    global isAliveCt
    chance = random.randint(1, 100)
    MUTATION_RATE = 2 # set mutation rate to 2%
    if (chance == MUTATION_RATE):
        cellNumToChange = random.randint(1, isAliveCt)
        numSeen = 0
        for i in range(1, 20, 1):
            for j in range(1, 30, 1):
                if (numSeen == cellNumToChange):
                    flipNeighbor(gameBoard, i - 1, j - 1)
                if (gameBoard[i][j].isAlive()):
                    numSeen += 1

# checkNeighbors
# Takes in a cell and the gameBoard; returns how many alive neighbors it has
def checkNeighbors(cell, gameBoard):
    row, col = cell.getCoordinates()
    numAlive = 0
    if (gameBoard[row - 1][col - 1].isAlive()):
        numAlive += 1
    if (gameBoard[row][col - 1].isAlive()):
        numAlive += 1
    if (gameBoard[row + 1][col - 1].isAlive()):
        numAlive += 1
    if (gameBoard[row + 1][col].isAlive()):
        numAlive += 1
    if (gameBoard[row + 1][col + 1].isAlive()):
        numAlive += 1
    if (gameBoard[row][col + 1].isAlive()):
        numAlive += 1
    if (gameBoard[row - 1][col + 1].isAlive()):
        numAlive += 1
    if (gameBoard[row - 1][col].isAlive()):
        numAlive += 1
    return numAlive

# toFlip
# Takes in a cell and its number of alive neighbors. Executes each of the rules
# of the game: Turns cell to alive / dead depending on neighbors' statuses
def toFlip(numAlive, cell):
    if (cell.isAlive()):
        if (numAlive < 2):
            cell.flipStatus = True
        if (numAlive == 2) or (numAlive == 3):
            cell.flipStatus = False
        if (numAlive > 3):
            cell.flipStatus = True
    if (not cell.isAlive()):
        if (numAlive == 3):
            cell.flipStatus = True
        else:
            cell.flipStatus = False
count = 0
goToPlay = True
# click 
# Defines the play / pause button behavior; changes icon
def click():
    global count
    global goToPlay
    count += 1
    goToPlay = not goToPlay
    if (goToPlay):
        button.config(image=play) 
    else: 
        button.config(image=pause) 
    
    
# setBoard
# After each "generation" we call setBoard to flip all cells according to rules
def setBoard(gameBoard):
    for i in range(1, 20, 1):
        for j in range(1, 30, 1):
            if (gameBoard[i][j].flipStatus):
                gameBoard[i][j].flip()
    
# flipNeighbor
# We flip a random neighbor of a cell 
def flipNeighbor(gameBoard, i, j):
    randNeighbor = random.randint(1, 8)
    if (randNeighbor == 1):
        gameBoard[i - 1][j].flip()
    if (randNeighbor == 2):
        gameBoard[i - 1][j - 1].flip()
    if (randNeighbor == 3):
        gameBoard[i - 1][j + 1].flip()
    if (randNeighbor == 4):
        gameBoard[i][j - 1].flip()
    if (randNeighbor == 5):
        gameBoard[i][j + 1].flip()
    if (randNeighbor == 6):
        gameBoard[i + 1][j].flip()
    if (randNeighbor == 7):
        gameBoard[i + 1][j - 1].flip()
    if (randNeighbor == 8):
        gameBoard[i + 1][j + 1].flip()
        

# printBoard
# Updates the Image with the correct alive / dead cells. Takes in the gameBoard
def printBoard(gameBoard):
    global ct
    width, height = 1080, 720
    life_canvas = Image.new("RGB", (width, height), "white")

    draw = ImageDraw.Draw(life_canvas)

    for i in range(0,720,36):
        draw.line([(0,i),(1080,i)], fill ="black", width = 3) 
    for i in range(0,1080,36):
        draw.line([(i,0),(i,720)], fill ="black", width = 3) 


    global isAliveCt
    isAliveCt = 0
    for i in range(1, 20, 1):
        for j in range(1, 30, 1):
            if (gameBoard[i][j].isAlive()):
                isAliveCt += 1
                draw.rectangle(((j*36)+2, (i*36)+2, (j*36)+34, (i*36)+34), 
                               outline=None, fill="blue")
            else: 
                draw.rectangle(((j*36)+2, (i*36)+2, (j*36)+34, (i*36)+34), 
                                outline=None, fill="white")


    font = ImageFont.truetype("Helvetica", size=20)
    textOne = "Generation: " + str(ct)
    textTwo = "Population: " + str(isAliveCt)
    draw.rectangle([(3,3),(180,60)], fill='white', outline="Black")
    draw.text([5,5],textOne,font=font,fill="black")
    draw.text([5,30],textTwo, font=font, fill="black")

    return life_canvas
    
    

# updateImage
# Changes the label's image to the inputted new image
def updateImage(label, newImage):
    tk_image = ImageTk.PhotoImage(newImage) 
    label.config(image=tk_image)  
    label.image = tk_image  

hasClosed = False
# onClose
# When the window is closed, destroy it and signal to the rest of the program
# that it is over by setting hasClosed to true
def onClose():
    global ct
    ct = 50
    global hasClosed 
    hasClosed = True
    global count
    count = 1
    window.destroy()

# selectSquare
# takes in the "click" of the user and flips the cell that was clicked
def selectSquare(event):
    global hasStarted
    if (not hasStarted):
        x,y = event.x, event.y
        global gameBoard
        global image_label

        gameBoard[int(y/36)][int(x/36)].flip()
        new_image = printBoard(gameBoard)
        updateImage(image_label, new_image)
# startDefaultSim
# Once we begin the actual simulation, we do not need the default / custom setup
# buttons, so we delete them
def startDefaultSim():
    global hasStarted
    hasStarted = True
    buttonDefault.destroy()
    buttonCustom.destroy()

# customSetup
# We flip the cells that represent the default setup so that they are blakn
def customSetup():
    global image_label
    global hasStarted
    hasStarted = False
    gameBoard[10][15].flip()
    gameBoard[11][15].flip()
    gameBoard[12][15].flip()
    gameBoard[11][14].flip()
    gameBoard[12][16].flip()
    currImage = printBoard(gameBoard)
    updateImage(image_label, currImage)

    buttonCustom.destroy()
    buttonDefault.destroy()


# Create a new blank image with white background (RGB mode, 1000x800)
rows, cols = (21, 31)
gameBoard = [[Cell(False, j, i) for j in range(cols)] for i in range(rows)]

# Create the Tkinter window
window = Tk()
window.title("Game of Life")

isAliveCt = 0
ct = 0
# Initial image setup
gameBoard[10][15].flip()
gameBoard[11][15].flip()
gameBoard[12][15].flip()
gameBoard[11][14].flip()
gameBoard[12][16].flip()
currImage = printBoard(gameBoard)
tk_initial_image = ImageTk.PhotoImage(currImage)

#Create a label to display the image
image_label = Label(window, image=tk_initial_image)
image_label.pack()

image_label.bind("<Button-1>", selectSquare)

# initialize pause + play buttons
pause = PhotoImage(file='pause.png')
play = PhotoImage(file='play.png')
button = Button(window,
                command=click,
                image=play,
                state=ACTIVE,
                )

buttonCustom = Button(window,
                      command=customSetup,
                      text = "Choose unique setup",
                      font = "Helvetica, 30",
                      state=ACTIVE)

buttonDefault = Button(window,
                       command=startDefaultSim,
                       state=ACTIVE,
                       text="Use default setup",
                       font = "Helvetica, 30")

buttonDefault.place(x=150, y = 500)
buttonCustom.place(x = 550, y = 500)
button.place(x=30, y=80)
window.protocol("WM_DELETE_WINDOW", onClose)
hasStarted = True

MUTATION_RATE = 2
while (not hasClosed): # run while window is open
    while (not count % 2 == 0): # run until the the pause button is pressed
        hasStarted = True
        mutate(gameBoard)
        currBoard = printBoard(gameBoard)
        if (isAliveCt == 0):
            time.sleep(2)
            window.destroy()
            hasClosed = True
            break
        updateImage(image_label, currBoard)
        window.update()  # Update the window immediately

        for i in range(1, 20, 1):
            for j in range(1, 30, 1):
                numAlive = checkNeighbors(gameBoard[i][j], gameBoard)
                toFlip(numAlive, gameBoard[i][j])
        setBoard(gameBoard)
        tk_image = ImageTk.PhotoImage(currBoard)
        image_label.config(image=tk_image)
        image_label.image = tk_image  # Keep reference to avoid garbage collection
        
        ct +=1
        time.sleep(0.2)
    if (not hasClosed):
        window.update()

window.mainloop()