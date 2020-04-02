#!/usr/bin/env python3

from pyglet.gl import *
import pyglet as P

import math
import time

from quadTree import *

class PCell:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.pressure = 108000
        self.temperature = 20

def drawLine(sX,sY,eX,eY):
    glBegin(GL_LINES)
    glVertex2f(sX,sY)
    glVertex2f(eX,eY)
    glEnd()

def drawSquare(sX,sY,size,color):
    glBegin(GL_QUADS)
    glColor3f(color[0],color[1],color[2])
    glVertex2f(sX,sY)
    glVertex2f(sX+size,sY)
    glVertex2f(sX+size,sY+size)
    glVertex2f(sX,sY+size)
    glEnd()

def drawText(text,sX,sY,size):
    label = P.text.Label(str(text),
                         font_size=size,
                         x=sX,
                         y=sY,
                         anchor_x='center',
                         anchor_y='center')
    label.draw()

def checkerBoard(size):
    for i in range(int(WIN_WIDTH/size) + 1):
        drawLine(i*size,0,i*size,win.height)
        drawLine(0,i*size,win.width,i*size)

### mouse stuff
xPress = -1
yPress = -1

xMouse = -1
yMouse = -1

### constants
WIN_WIDTH = 800
BLOCK_SIZE = 10
DRAW_MAP = False

### pyglet win stuff
win = P.window.Window(WIN_WIDTH,WIN_WIDTH,caption="Grain sim")
#win.set_mouse_visible(False)
fps_display = P.window.FPSDisplay(window=win)
glClearColor(0.2,0.2,0.2, 1)

qtree = QuadTree(Rectangle(400,400,400,400), 6)

def drawTree(tree):
    drawLine(tree.area.x-tree.area.w,tree.area.y+tree.area.h, tree.area.x-tree.area.w+tree.area.w*2, tree.area.y+tree.area.h)
    drawLine(tree.area.x-tree.area.w,tree.area.y-tree.area.h, tree.area.x-tree.area.w+tree.area.w*2, tree.area.y-tree.area.h)

    drawLine(tree.area.x-tree.area.w,tree.area.y-tree.area.h, tree.area.x-tree.area.w, tree.area.y+tree.area.h)
    drawLine(tree.area.x+tree.area.w,tree.area.y-tree.area.h, tree.area.x+tree.area.w, tree.area.y+tree.area.h)

    try: 
        drawTree(tree.NW)
        drawTree(tree.NE)
        drawTree(tree.SW)
        drawTree(tree.SE)
    except:
        pass


@win.event
def on_draw():
    """ DRAW FUNCTION """
    win.clear()
    glColor3f(1,1,1)
    global qtree

    if(DRAW_MAP):
        checkerBoard(BLOCK_SIZE)

    global xPress,yPress,xMouse,yMouse
    if(xPress != -1):
        qtree.insert(PCell(xPress, yPress))

        xPress = yPress = -1

    elif(xMouse != -1):
        #cursorDrawing()
        pass

    drawTree(qtree)
    
    fps_display.draw()

@win.event
def on_key_press(s,mod):
    """ KEYBOARD INPUTS """
    if(s == P.window.key.F1):
        global DRAW_MAP
        if(DRAW_MAP):
            DRAW_MAP = False
        else:
            DRAW_MAP = True
    if(s == P.window.key.N):
        global GRAINLIST, static_GRAINLIST, BLOCK_SIZE 
        GRAINLIST = []
        static_GRAINLIST = []
        update_grain_map()

    global GRAIN_TYPE_SELECTED
    if(s == P.window.key.NUM_0):
        GRAIN_TYPE_SELECTED = 0
    if(s == P.window.key.NUM_1):
        GRAIN_TYPE_SELECTED = 1
    if(s == P.window.key.NUM_2):
        GRAIN_TYPE_SELECTED = 2
    if(s == P.window.key.NUM_3):
        GRAIN_TYPE_SELECTED = 3

    if(s == P.window.key.UP):
        BLOCK_SIZE += 2
    if(s == P.window.key.DOWN):
        if(BLOCK_SIZE > 4):
            BLOCK_SIZE -= 2

@win.event
def on_mouse_drag(x, y, dx, dy, c, d):
    """ MOUSE INPUT1 """
    global xPress, yPress 
    xPress = x
    yPress = y

@win.event
def on_mouse_press(x,y ,c,d):
    """ MOUSE INPUT2 """ 
    global xPress, yPress
    xPress = x
    yPress = y

@win.event
def on_mouse_motion(x,y ,c,d):
    """ MOUSE MOTION """ 
    global xMouse, yMouse
    xMouse = x
    yMouse = y

@win.event
def on_mouse_scroll(x,y,scroll_x,scroll_y):
    """ MOUSE WHEEL EVENT """ 
    global mouseWheel
    if(1 <= mouseWheel <= 10):
        mouseWheel += scroll_y

    if(mouseWheel == 0):
        mouseWheel = 1

    if(mouseWheel == 11):
        mouseWheel = 10

@win.event
def on_mouse_release(x, y, button, modifiers):
    """ MOUSE INPUT END """ 
    global xPress, yPress
    xPress = yPress = -1

@win.event
def tick(t):
    """ TICK """
    pass

if __name__ == "__main__":
    P.clock.schedule_interval(tick, 1/60)
    P.app.run()
