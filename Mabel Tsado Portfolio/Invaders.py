#################################################
# INVADERS
#################################################

def alternatingSum(L):
    s = 1
    c = 0
    if (L == []):
        return 0
    for i in L:
        c += i*s
        s = s*-1
    return c    
        

def median(L):
    n = len(L)
    a = sorted(L)
    if (L == []):
        return None
    if n % 2 == 1:
        return a[n//2]
    else:
        return sum(a[n//2-1:n//2+1])/2.0
        
        

#################################################
# Test Functions
#################################################

def testAlternatingSum():
    print('Testing alternatingSum()...', end='')
    assert(alternatingSum([ ]) == 0)
    assert(alternatingSum([1]) == 1)
    assert(alternatingSum([1, 5]) == 1-5)
    assert(alternatingSum([1, 5, 17]) == 1-5+17)
    assert(alternatingSum([1, 5, 17, 4]) == 1-5+17-4)
    print('Passed.')

def almostEqual(d1, d2):
    epsilon = 10**-10
    return (abs(d2 - d1) < epsilon)

def testMedian():
    print('Testing median()...', end='')
    assert(median([ ]) == None)
    assert(median([ 42 ]) == 42)
    assert(almostEqual(median([ 1 ]), 1))
    assert(almostEqual(median([ 1, 2]), 1.5))
    assert(almostEqual(median([ 2, 3, 2, 4, 2]), 2))
    assert(almostEqual(median([ 2, 3, 2, 4, 2, 3]), 2.5))
    # now make sure this is non-destructive
    a = [ 2, 3, 2, 4, 2, 3]
    b = a + [ ]
    assert(almostEqual(median(b), 2.5))
    if (a != b):
        raise Exception('Your median() function should be non-destructive!')
    print('Passed')

def testAll():
    testAlternatingSum()
    testMedian()

#################################################
# Animation
#################################################

from tkinter import *

####################################
# Customize any of these functions:
####################################

def init(data): pass                 # initialize the model (data.xyz)
def mousePressed(event, data): pass  # use event.x and event.y
def mouseDragged(event, data): pass  # use event.x and event.y
def mouseReleased(event, data): pass # use event.x and event.y
def mouseMoved(event, data): pass    # use event.x and event.y
def keyPressed(event, data): pass    # use event.key
def timerFired(data): pass           # respond to timer events
def drawAll(canvas, data): pass      # view the model in the canvas



class Shape(object):
    
    def __init__(shape, cx, cy, color):
        shape.cx = cx
        shape.cy = cy
        shape.r = 15
        shape.color = color
        

def init(data):
    data.missile = Shape(data.width//2, 485, 'black')
    data.base = Shape(data.width//2, 485, 'black')
    data.timerDelay = 25
    data.monstersDx = 3
    data.monstersDy = 40
    data.monsters = []
    data.r = 15
    data.gameOver = False
    data.colors = ['red', 'orange', 'yellow', 'lightGreen', 'cyan']
   
    data.win = False
    data.missileIsVisible = False
    data.xdirection = 1
    data.ydirection = 1
    for r in range(len(data.colors)):
        for c in range(8):
            cx = 165 + c * 67.14
            cy = 75 + r * 40
            color = data.colors [r]
            x = Shape(cx,cy,color)
            data.monsters.append(x)
            data.countmonsters = len(data.colors) * 8 


def moveMonsters(data):
    if (data.gameOver == False):
        hitedge = False
        
        for monsters in data.monsters:
                
            if(monsters.cx + monsters.r >= data.width): 
                hitedge = True
            elif(monsters.cx - monsters.r <= 0):
                hitedge = True
        if (hitedge == True):
            data.xdirection *= -1    
            
        for monsters in data.monsters:
            if (hitedge == True):
                monsters.cy += data.ydirection*data.monstersDy
            
            monsters.cx += data.xdirection*data.monstersDx
        
            #Game Over
        for monsters in data.monsters:
            if (monsters.cy >= 470):
                data.gameOver = True
                
            
    pass

def moveMissile(data):
    if (data.missileIsVisible == False):
        data.missile.cx = data.base.cx
        data.missile.cy = data.base.cy 
        
    if (data.missileIsVisible == True):
        data.missile.cy -= 10
        if (data.missile.cy <= 0):
            data.missileIsVisible = False
        
  

def checkForCollisions(data):
    for monsters in data.monsters:
        d = ((data.missile.cx - monsters.cx)**2 + (data.missile.cy - monsters.cy)**2)**0.5
        if(d <= 2*data.r and data.missileIsVisible == True):
            data.missileIsVisible = False
            data.monsters.remove(monsters)
            data.countmonsters -= 1
    if (data.countmonsters == 0):
        data.win = True
        data.gameOver = True
    elif (data.countmonsters >= 1):
        data.win = False
        
       
             
    
  

def keyPressed(event, data):
    
    if (event.key == 'r' and data.gameOver == True):
        init(data)
        
    if (data.missileIsVisible == False):
           
        if (event.key == 'Space'):
            data.missileIsVisible = True
    
    if (data.gameOver == False):
         
        if (event.key == 'Left'):
            data.base.cx -= 10
        elif (event.key == 'Right'):
            data.base.cx += 10
    else:
        data.missileIsVisible = False
       

def timerFired(data):
    if (data.gameOver == False):
        moveMonsters(data)
        
        if (data.missileIsVisible == True):
            moveMissile(data)
        elif(data.missileIsVisible == False):
            moveMissile(data)   
        
        checkForCollisions(data)

    

def drawAll(canvas, data):
    
#Game is not Over
    if (data.gameOver == False):
    
        #Title
        canvas.create_text(data.width//2,20, text = 'INVADERS: Use spacebar and left right arrows', font = 'Arial 35 bold')
        
        #Monsters
        
        for monster in data.monsters:   
            canvas.create_oval(monster.cx-monster.r,monster.cy-monster.r,monster.cx+monster.r,monster.cy+monster.r, fill = monster.color)
        
        #Missile
        if (data.missileIsVisible == True):
            canvas.create_oval(data.missile.cx - data.missile.r, data.missile.cy - data.missile.r, data.missile.cx + data.missile.r, data.missile.cy + data.missile.r, fill = 'black')
            
        #Base
        
        canvas.create_oval(data.base.cx - data.base.r, data.base.cy - data.base.r, data.base.cx + data.base.r, data.base.cy + data.base.r, fill = 'grey')
    
#Game Over
    
    #You Win
    elif (data.gameOver == True and data.win == True):
        
        #Title
        canvas.create_text(data.width//2,20, text = 'INVADERS: Use spacebar and left right arrows', font = 'Arial 35 bold')
        
        #Monsters
        for monster in data.monsters:   
            canvas.create_oval(monster.cx-monster.r,monster.cy-monster.r,monster.cx+monster.r,monster.cy+monster.r, fill = monster.color)
        
        #Missile
        if (data.missileIsVisible == True):
            canvas.create_oval(data.missile.cx - data.missile.r, data.missile.cy - data.missile.r, data.missile.cx + data.missile.r, data.missile.cy + data.missile.r, fill = 'black')
            
        #Base
        canvas.create_oval(data.base.cx - data.base.r, data.base.cy - data.base.r, data.base.cx + data.base.r, data.base.cy + data.base.r, fill = 'grey')  
        
        #You Win  
        canvas.create_text(data.width//2,data.height//2, text = 'YOU WIN!', font = 'Arial 35 bold')
        
        #Start Again
        canvas.create_text(data.width//2,485, text = 'Press r to start again', font = 'Arial 20 bold')
        
        
    #You Lose     
    elif (data.gameOver == True and data.win == False):
        
        #Title
        canvas.create_text(data.width//2,20, text = 'INVADERS: Use spacebar and left right arrows', font = 'Arial 35 bold')
        
        #Monsters
        for monster in data.monsters:   
            canvas.create_oval(monster.cx-monster.r,monster.cy-monster.r,monster.cx+monster.r,monster.cy+monster.r, fill = monster.color)
        
        #Missile
        if (data.missileIsVisible == True):
            canvas.create_oval(data.missile.cx - data.missile.r, data.missile.cy - data.missile.r, data.missile.cx + data.missile.r, data.missile.cy + data.missile.r, fill = 'black') 
            
        #Base
        canvas.create_oval(data.base.cx - data.base.r, data.base.cy - data.base.r, data.base.cx + data.base.r, data.base.cy + data.base.r, fill = 'grey')    
        
        #You Lose
        canvas.create_text(data.width//2,data.height//2, text = 'YOU LOSE!', font = 'Arial 35 bold')
        
        #Start Again
        canvas.create_text(data.width//2,485, text = 'Press r to start again', font = 'Arial 20 bold')
        
        

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
    run(800, 500)
