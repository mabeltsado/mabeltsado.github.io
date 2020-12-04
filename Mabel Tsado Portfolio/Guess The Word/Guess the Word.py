#################################################
# GUESS THE WORD
#################################################

def digitCount(n):
    if (n == 0): return 1
    n = abs(n)
    count = 0
    while (n > 0):
        count += 1
        n //= 10
    return count

def hasConsecutiveDigits(n):
    prevDigit = -1
    n = abs(n)
    while (n > 0):
        onesDigit = n%10
        n //= 10
        if (prevDigit == onesDigit):
            return True
        prevDigit = onesDigit
    return False

def isWordGuessed(word, guesses):
    for x in word: 
        if (not x in guesses):
            return False
    
    return True
                  
        
def makeDisplayWord(word, guesses):
    y = ''
    for x in word:
        if (x in guesses):
            y += x
        else:
            y += '-'
    return y
    
def getErrorMessage(guess, word, guesses):
    y = ''
    if (guess.isalpha() == False):
        y = guess + ' is not a letter!'
        return y
        
    else:
        if (guess not in word):
            y = guess + ' is not in the word!'
            return y
        elif (guess in guesses and guess in word):
            y = 'You already guessed ' + guess
            return y    
        elif (guess not in guesses and guess in word):
            return ''
        elif (guess in guesses and guess not in word):
            y = 'You already guessed ' + guess
            return y
        elif (guess in guesses):
            y = 'You already guessed ' + guess
            return y
        
            
    return y
    


#################################################
# Test Functions
#################################################

def testDigitCount():
    print('Test digitCount()...', end='')
    assert(digitCount(0) == 1)
    assert(digitCount(5) == 1)
    assert(digitCount(-5) == 1)
    assert(digitCount(42) == 2)
    assert(digitCount(-42) == 2)
    assert(digitCount(121) == 3)
    assert(digitCount(-121) == 3)
    assert(digitCount(-10002000) == 8)
    print('Passed')

def testHasConsecutiveDigits():
    print('Testing hasConsecutiveDigits()... ', end='')
    assert(hasConsecutiveDigits(0) == False)
    assert(hasConsecutiveDigits(123456789) == False)
    assert(hasConsecutiveDigits(1212) == False)
    assert(hasConsecutiveDigits(1212111212) == True)
    assert(hasConsecutiveDigits(33) == True)
    assert(hasConsecutiveDigits(330) == True)
    assert(hasConsecutiveDigits(3003) == True)
    assert(hasConsecutiveDigits(-1212111212) == True)
    print('Passed.')

def testIsWordGuessed():
    print('Testing isWordGuessed()...', end='')
    assert(isWordGuessed('egg', 'gw') == False)
    assert(isWordGuessed('egg', 'gwe') == True)
    assert(isWordGuessed('egg', '') == False)
    assert(isWordGuessed('egg', 'g') == False)
    assert(isWordGuessed('egg', 'eg') == True)
    assert(isWordGuessed('egg', 'abcdefg') == True)
    print('Passed')

def testMakeDisplayWord():
    print('Testing makeDisplayWord()...', end='')
    assert(makeDisplayWord('egg', 'gw') == '-gg')
    assert(makeDisplayWord('egg', 'gwe') == 'egg')
    assert(makeDisplayWord('egg', '') == '---')
    assert(makeDisplayWord('egg', 'g') == '-gg')
    assert(makeDisplayWord('egg', 'eg') == 'egg')
    assert(makeDisplayWord('egg', 'abcdefg') == 'egg')
    print('Passed')

def testGetErrorMessage():
    print('Testing getErrorMessage()...', end='')
    assert(getErrorMessage('e', 'egg', 'gw') == '')
    assert(getErrorMessage('g', 'egg', 'gw') == 'You already guessed g')
    assert(getErrorMessage('@', 'egg', 'gw') == '@ is not a letter!')
    assert(getErrorMessage('z', 'egg', 'gw') == 'z is not in the word!')
    print('Passed')

def testLongestDigitRun():
    print('Testing optional/bonus longestDigitRun()... ', end='')
    assert(longestDigitRun(117773732) == 7)
    assert(longestDigitRun(-677886) == 7)
    assert(longestDigitRun(5544) == 4)
    assert(longestDigitRun(1) == 1)
    assert(longestDigitRun(0) == 0)
    assert(longestDigitRun(22222) == 2)
    assert(longestDigitRun(111222111) == 1)
    print('Passed.')

def testAll():
    testDigitCount()
    testHasConsecutiveDigits()
    testIsWordGuessed()
    testMakeDisplayWord()
    testGetErrorMessage()
    try: testLongestDigitRun()
    except: print('bonus function did not pass')

#################################################
# Animation
#################################################

from tkinter import *
import random  

####################################
# Helper functions
####################################

# These functions are provided for you.

def readFile(path):
    # This makes a very modest attempt to deal with unicode if present
    with open(path, 'rt', encoding='ascii', errors='surrogateescape') as f:
        return f.read()

def getRandomWord():
    fileContents = readFile('hw3-words.txt')
    return random.choice(fileContents.splitlines()[1:])

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


def init(data):
    data.word = getRandomWord()
    data.guesses = ''
    data.missesLeft = 10
    data.message = 'Press any letter!'
    data.gameOver = False
    data.lose = True
    data.winwords = 'YOU GOT IT! YOU WON!!!'
    data.losewords = 'YOU LOSE!!'
    data.mDW = makeDisplayWord(data.word, data.guesses)

def keyPressed(event, data):
    guess = event.key
    data.guesses += guess
    if (data.gameOver == True):
        init(data)
    else:
        data.message = getErrorMessage(guess, data.word, data.guesses)
        #Guesses
        if (guess in data.word):
            data.mDW = makeDisplayWord(data.word, data.guesses)
            
        if (guess in data.word):
            data.missesLeft -= 0
        elif (guess in data.guesses and guess in data.word):
            data.missesLeft -= 1     
          
        elif (guess not in data.word):
            data.missesLeft -= 1
            
        elif (guess in data.guesses):
            data.missesLeft -= 1
            
        #Game over    
        if (data.missesLeft <= 0):
            data.gameOver = True
        if (data.mDW == data.word):
            data.gameOver = True
            data.lose = False    
        if (data.lose == True):
            data.losewords       
        elif (data.lose == False):   
            data.winwords
         
        
    
def drawAll(canvas, data):
    
    canvas.create_text(data.width/2, 20,text='Guess the Word!', font='Arial 26 bold')
    canvas.create_text(data.width/2, 45,text='Misses Left:' + str(data.missesLeft), font='Arial 20 bold')
    
#Game not Over
    if (data.gameOver == False):
        canvas.create_text(data.width/2, data.height/3,text='Guesses:' + data.guesses, font='Arial 20 bold')
        for i in range (len(data.mDW)):
            canvas.create_text((i*2+1) * data.width/(len(data.word)*2), data.height/2, text = data.mDW[i], font='Arial 20 bold')
        canvas.create_text(data.width/2, 70,text=data.message, font='Arial 20 bold')
#Game Over
    #You lose
    elif (data.gameOver == True and data.lose == True):
        canvas.create_text(data.width/2, 70, text= data.losewords, font='Arial 20 bold')
        canvas.create_text(data.width/2, data.height/3,text = 'GAME OVER', font='Arial 26 bold')
        canvas.create_text(data.width/2, data.height/3 + 25,text = 'Press any key to continue', font='Arial 20 bold')
        for i in range (len(data.word)):
            if (data.mDW[i] == '-'):
                canvas.create_text((i*2+1) * data.width/(len(data.word)*2), data.height/2, text = data.word[i], font='Arial 20 bold', fill='red')
            else:
                canvas.create_text((i*2+1) * data.width/(len(data.word)*2), data.height/2, text = data.word[i], font='Arial 20 bold', fill='black')
    #You win            
    elif (data.gameOver == True and data.lose == False):
        canvas.create_text(data.width/2, 70, text= data.winwords, font='Arial 20 bold')
        canvas.create_text(data.width/2, data.height/3,text = 'GAME OVER', font='Arial 26 bold')
        canvas.create_text(data.width/2, data.height/3 + 25,text = 'Press any key to continue', font='Arial 20 bold')
        for i in range (len(data.word)):
            canvas.create_text(data.width/2 - 123 + (i*50), data.height/2, text = data.word[i], font='Arial 20 bold')
        
        

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
    run(500, 500)
