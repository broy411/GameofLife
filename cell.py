# cell.py
# Authors: Katie Adiletta and Brendan Roy
# Date created: January 8th, 2025

# Cell class for GameOfLife
# Each cell has two states: alive or dead
# Each cell has x,y coordinates that represent the row, column in the table

class Cell:
    flipStatus = False
    def __init__(self, status, row, col):
        self.alive = status
        self.x = col
        self.y = row
    def isAlive(self):
        return self.alive
    def setStatus(self, status):
        self.alive = status
    def getCoordinates(self):
        return self.x, self.y
    def flip(self):
        self.alive = not self.alive
