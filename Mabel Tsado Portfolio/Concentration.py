#################################################
#Concentration
#################################################

import random

def make2dList(rows, cols, defaultValue=None):
    a=[]
    for row in range(rows): a.append([defaultValue]*cols)
    return a

def addRowAndColSums(L):
    sum = 0
    M = make2dList(len(L), len(L[0]))
    cols = len(M[0])
    rows = len(M)
    for row in range(rows):
        for col in range(cols):
            M[row][col] = L[row][col]
    for row in range(rows):
        for col in range(cols):
            sum += M[row][col]
        M[row].append(sum)
        sum = 0
    newList = []
    cols = len(M[0])
    for col in range(cols):
        for row in range(rows):
            sum += M[row][col]
        newList.append(sum)
        sum = 0
    M.append(newList)

    return M
    

def findWinningDice(dice1, dice2, rolls):
    
    sucess = 0
    trials = 10**4
    for trial  in range(trials):
        if (trialSucceeds(dice1, dice2, rolls)):
            sucess += 1
        prob = (sucess/trials)
    if (prob >= 0.5):
        return dice1
    else:
        return dice2    

def trialSucceeds(dice1, dice2, rolls):
    player1 = 0
    player2 = 0
    for i in range(rolls):
        player1 += random.choice(dice1)
        player2 += random.choice(dice2)
    if (player1 > player2):
        return True
    if (player1 < player2):    
        return False

#################################################
# Test Functions
#################################################

def testAddRowAndColSums():
    print('Testing addRowAndColSums()...', end='')
    L = [ [ 1, 2, 3],
          [ 4, 5, 6] ]
    M = [ [ 1, 2, 3, 6 ],
          [ 4, 5, 6, 15 ],
          [ 5, 7, 9, 21 ] ]
    assert(addRowAndColSums(L) == M)
    L = [ [ 1, 3 ] ]
    M = [ [ 1, 3, 4],
          [ 1, 3, 4] ]
    assert(addRowAndColSums(L) == M)
    print('Passed!')

def testFindWinningDice():
    print('Testing findWinningDice()...', end='')
    # A, B, C from https://plus.maths.org/content/non-transitiv-dice
    A = [3, 3, 6, 3, 3, 3]
    B = [5, 5, 5, 2, 2, 2]
    C = [4, 4, 1, 4, 4, 4]

    assert(findWinningDice(A, B, 1) == A)
    assert(findWinningDice(A, B, 2) == B)

    assert(findWinningDice(B, C, 1) == B)
    assert(findWinningDice(B, C, 2) == C)

    assert(findWinningDice(C, A, 1) == C)
    assert(findWinningDice(C, A, 2) == A)
    print('Passed!')

def testAll():
    testAddRowAndColSums()
    testFindWinningDice()
    pass
#################################################
#Concentration
#################################################

from tkinter import *
import random

def init(data):
    margin = 20
    topMargin = 150
    data.boardGame = BoardGame(4, 8, margin, topMargin,
                               data.width-margin, data.height-margin)
    data.guesses = 0
    data.foundCount = 0
    data.selections = []
    data.boardGame.rows = 4
    data.boardGame.cols = 8
    #values
    data.values = list(range(16))*2
    random.shuffle(data.values)
    for row in range(data.boardGame.rows):
        for col in range(data.boardGame.cols):
            cell = data.boardGame.board[row][col]
            cell.value = data.values.pop()
            cell.isFound = False
            cell.color = 'white'
    data.gameOver = False
    data.showNumbers = True
    data.displayValues = False
    data.sort = False
    data.matches = []
  
def cellsMatch(cell1, cell2):
    if (cell1.value == cell2.value and (cell1.row != cell2.row or cell1.col != cell2.col)):
        return True
    else:
        return False
    
def mousePressed(event, data):
    cell = getCell(data.boardGame, event.x, event.y)
    if (data.gameOver == False):
        if (len(data.selections) == 2):
            data.selections = []
        if (cell != None and cell.isFound == False and cell not in data.selections):
            selectCell(cell, data)
    

def selectCell(cell, data):
    if (data.gameOver == False):
        data.selections.append(cell)
        if (len(data.selections) == 2):
            if (cellsMatch(data.selections[0], data.selections[1]) == True):
                data.selections[0].isFound = True
                data.selections[1].isFound = True
                data.foundCount += 1
                data.matches.append(data.selections[0])
                data.matches.append(data.selections[1])
            data.guesses += 1
            if (data.foundCount == 16):
                data.gameOver = True    
            
def restartAndSortValues(data):
    init(data)
    data.sort = True
    ordered = list(range(16))*2
    for row in range(data.boardGame.rows):
        for col in range(data.boardGame.cols):
            cell = data.boardGame.board[row][col]
            cell.value = ordered.pop(0)
    

def keyPressed(event, data):
    if (event.key == 'n'):
        data.showNumbers = not data.showNumbers
        
    elif (event.key == 'v'):
        data.displayValues = not data.displayValues
        
    elif (event.key == 's'):
        restartAndSortValues(data)
    
    elif (event.key == 'r'):
        init(data)    
    elif (event.key == 'a'):
        autoplay(data)

def autoplay(data):
    if (data.gameOver == True):
        init(data)
    else:
        if (len(data.selections) == 2):
            data.selections = []
        if (len(data.selections) == 0):
            while True:
                randomCell = data.boardGame.board[random.randrange(data.boardGame.rows)][random.randrange(data.boardGame.cols)]
                if (randomCell != None and randomCell.isFound == False):
                    selectCell(randomCell, data)
                    return
        elif (len(data.selections) == 1):
            for row in range(data.boardGame.rows):
                for col in range(data.boardGame.cols):
                    cell = data.boardGame.board[row][col]
                    randomCell = data.selections[0]
                    if (cellsMatch(cell, randomCell) == True):
                        selectCell(cell, data)
            
    

def drawCellValue(canvas, data, cell, bounds):
    cx = (bounds.x0+bounds.x1)/2
    cy = (bounds.y0+bounds.y1)/2
    if (data.showNumbers == True):
        canvas.create_text(cx,cy, text = str(cell.value))
    else: 
        bit0 = cell.value % 2
        bit1 = cell.value//2 % 2
        bit2 = cell.value//4 % 2
        bit3 = cell.value//8 % 2
        colors = ['red', 'orange', 'green', 'blue']
        colorIndex = 2*bit3 + bit2
        fillColor = colors[colorIndex]
        if (bit1 == 1):
            outlineColor = 'black'
        else:
            outlineColor = fillColor
        x0 = cx - data.boardGame.cellWidth*0.4
        x1 = cx + data.boardGame.cellWidth*0.4
        y0 = cy - data.boardGame.cellHeight*0.4
        y1 = cy + data.boardGame.cellHeight*0.4
        if (bit0 == 1):
            canvas.create_oval(x0,y0,x1,y1, fill = fillColor, outline = outlineColor, width = 5)
        else:
            canvas.create_rectangle(x0,y0,x1,y1, fill = fillColor, outline = outlineColor, width = 5)

def drawAll(canvas, data):
    
    #Title
    canvas.create_text(data.width/2, 20, text='Concentration!', font='Arial 35 bold')
    
    # Draw the board
    for row in range(data.boardGame.rows):
        for col in range(data.boardGame.cols):
            bounds= getCellBounds(data.boardGame, row, col)
            cell = data.boardGame.board[row][col]
            cx = (bounds.x0+bounds.x1)/2
            cy = (bounds.y0+bounds.y1)/2
            
            canvas.create_rectangle(bounds.x0, bounds.y0, bounds.x1, bounds.y1, fill='white', outline='black')
            
            if (cell in data.matches):
                canvas.create_rectangle(bounds.x0, bounds.y0, bounds.x1, bounds.y1, fill='light green', outline='black')   
                drawCellValue(canvas, data, cell, bounds)
                
            elif (cell in data.selections) : 
                if (len(data.selections) == 1):
                    canvas.create_rectangle(bounds.x0, bounds.y0, bounds.x1, bounds.y1, fill='yellow', outline='black')
                    drawCellValue(canvas, data, cell, bounds)
                else:
                    canvas.create_rectangle(bounds.x0, bounds.y0, bounds.x1, bounds.y1, fill='pink', outline='black')
                    drawCellValue(canvas, data, cell, bounds)
            
            if (data.displayValues == True):
                drawCellValue(canvas, data, cell, bounds)
             
    #Instructions
    
    canvas.create_text(data.width/2, 80, text='Press a to autoplay, v to view values, n to toggle numbers, r to restart, s to sort', font='Arial 20')
    if (data.gameOver == False):
        canvas.create_text(data.width/2, 50, text='Click to find matches', font='Arial 20')
    else:
        canvas.create_text(data.width/2, 50, text='You Did It! Huzzah!! (Press r to restart)', font='Arial 20')
        canvas.create_text(data.width/2, data.height/2, text='Game Over!!!', font='Arial 70 bold')
        canvas.create_text(data.width/2, data.height/2 + 50, text='Press r to restart', font='Arial 20 bold')
        
    #Guesses
    canvas.create_text(data.width/2, 110, text='Guesses: ' + str(data.guesses), font='Arial 20')
    
            
    

####################################
# BoardGame class and functions
####################################

class Cell(object):
    def __init__(cell, row, col):
        cell.row = row
        cell.col = col

class Bounds(object):
    def __init__(bounds, x0, y0, x1, y1):
        bounds.x0 = x0
        bounds.y0 = y0
        bounds.x1 = x1
        bounds.y1 = y1

class BoardGame(object):
    def __init__(boardGame, rows, cols, x0, y0, x1, y1):
        boardGame.rows = rows
        boardGame.cols = cols
        boardGame.x0 = x0
        boardGame.y0 = y0
        boardGame.x1 = x1
        boardGame.y1 = y1
        boardGame.width = x1 - x0
        boardGame.height = y1 - y0
        boardGame.cellWidth = boardGame.width / boardGame.cols
        boardGame.cellHeight = boardGame.height / boardGame.rows
        # load the board, a 2d list of cells
        boardGame.board = make2dList(boardGame.rows, boardGame.cols)
        for row in range(boardGame.rows):
            for col in range(boardGame.cols):
                boardGame.board[row][col] = Cell(row, col)

def getCellBounds(boardGame, row, col):
    # aka "modelToView"
    x0 = boardGame.x0 + boardGame.cellWidth * col
    y0 = boardGame.y0 + boardGame.cellHeight * row
    x1 = x0 + boardGame.cellWidth
    y1 = y0 + boardGame.cellHeight
    return Bounds(x0, y0, x1, y1)

def getCell(boardGame, x, y):
    # aka "viewToModel"
    if ((x < boardGame.x0) or (x >= boardGame.x1) or
        (y < boardGame.y0) or (y >= boardGame.y1)):
        return None
    row = int((y - boardGame.y0) / boardGame.cellHeight)
    col = int((x - boardGame.x0) / boardGame.cellWidth)
    return boardGame.board[row][col]

def make2dList(rows, cols, defaultValue=None):
    a = [ ]
    for row in range(rows): a.append([defaultValue]*cols)
    return a

####################################
# Animation Framework:
####################################

class Struct(object): pass

def run(width=300, height=300):
    def drawAllWrapper():
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, width, height, fill='white', width=0)
        drawAll(canvas, data)
        canvas.update()

    def callFn(fn, event=None):
        if (fn == 'mousePressed'): data._mouseIsPressed = True
        elif (fn == 'mouseReleased'): data._mouseIsPressed = False
        if ('mouse' in fn): data._lastMousePosn = (event.x, event.y)
        if (fn in globals()):
            if (fn.startswith('key')):
                c = event.key = event.char
                if ((c in [None, '']) or (len(c) > 1) or (ord(c) > 255)):
                    event.key = event.keysym
                elif (c == '\t'): event.key = 'Tab'
                elif (c in ['\n', '\r']): event.key = 'Enter'
                elif (c == '\b'): event.key = 'Backspace'
                elif (c == chr(127)): event.key = 'Delete'
                elif (c == chr(27)): event.key = 'Escape'
                elif (c == ' '): event.key = 'Space'
                if (event.key.startswith('Shift')): return
            args = [data] if (event == None) else [event, data]
            globals()[fn](*args)
            drawAllWrapper()

    def timerFiredWrapper():
        callFn('timerFired')
        data._afterId1 = root.after(data.timerDelay, timerFiredWrapper)

    def mouseMotionWrapper():
        if (((data._mouseIsPressed == False) and (data._mouseMovedDefined == True)) or
            ((data._mouseIsPressed == True ) and (data._mouseDragDefined == True))):
            event = Struct()
            event.x = root.winfo_pointerx() - root.winfo_rootx()
            event.y = root.winfo_pointery() - root.winfo_rooty()
            if ((data._lastMousePosn !=  (event.x, event.y)) and
                (event.x >= 0) and (event.x <= data.width) and
                (event.y >= 0) and (event.y <= data.height)):
                fn = 'mouseDragged' if (data._mouseIsPressed == True) else 'mouseMoved'
                callFn(fn, event)
        data._afterId2 = root.after(data.mouseMovedDelay, mouseMotionWrapper)

    # Set up data and call init
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    data.mouseMovedDelay = 50 # ditto
    data._mouseIsPressed = False
    data._lastMousePosn = (-1, -1)
    data._mouseMovedDefined = 'mouseMoved' in globals()
    data._mouseDragDefined = 'mouseDragged' in globals()
    data._afterId1 = data._afterId2 = None
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event: callFn('mousePressed', event))
    # root.bind("<B1-Motion>", lambda event: callFn('mouseDragged', event))
    root.bind("<B1-ButtonRelease>", lambda event: callFn('mouseReleased', event))
    root.bind("<Key>", lambda event: callFn('keyPressed', event))
    # initialize, start the timer, and launch the app
    callFn('init')
    if ('timerFired' in globals()): timerFiredWrapper()
    if (data._mouseMovedDefined or data._mouseDragDefined): mouseMotionWrapper()
    root.mainloop()  # blocks until window is closed
    if (data._afterId1): root.after_cancel(data._afterId1)
    if (data._afterId2): root.after_cancel(data._afterId2)
    print("bye!")

if __name__ == '__main__':
    testAll()
    run(840, 525)
