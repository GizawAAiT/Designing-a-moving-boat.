
import pygame
from OpenGL.GL import *
import numpy as np
from OpenGL.GLU import *
from pygame.locals import *

from math import *

def init():
    pygame.init()
    display = (600, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(-10.0, 10.0, -10.0, 10.0)

def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(1.4)
    # glBegin(GL_POLYGON)
    # # x =0
    # # y = 0
    # glColor3f(0,0,0)
    # for i in range(360):
    #     angle_theta = i * 3.142 / 180
    #     glVertex2f(np.multiply(50,np.cos(angle_theta)),
    #              np.multiply(50,np.sin(angle_theta)))
        
    # glEnd()
    
    
    glBegin(GL_POLYGON)
    glColor3f(0,0,1)

    glVertex2f(-100,0)
    glVertex2f(100,0)
    glVertex2f(-100,-100)
    glVertex2f(100,-100)
    
    glEnd()
    glBegin(GL_POLYGON)
    glColor3f(0.5,0.5,1)

    glVertex2f(-100,0)
    glVertex2f(100,0)
    glVertex2f(-100,100)
    glVertex2f(100,100)
    
    glEnd()
    glBegin(GL_POLYGON)
    glColor3f(1.0,0,0)

    glVertex2f(-4,2)
    glVertex2f(-3,-1)
    glVertex2f(3,-1)
    glVertex2f(4,2)
    
    glEnd()
    glBegin(GL_POLYGON)
    glColor3f(1,1,0)

    glVertex2f(-2,2)
    glVertex2f(0,2)
    glVertex2f(0,4)
    glVertex2f(-2,4)
    
    glEnd()
    posx, posy = 7,8    
    sides = 32    
    radius = 1.5 
    glBegin(GL_POLYGON)   
    glColor3f(1,1,0) 
    for i in range(100):    
        cosine= radius * cos(i*2*pi/sides) + posx    
        sine  = radius * sin(i*2*pi/sides) + posy    
        glVertex2f(cosine,sine)

    glEnd()
    glFlush()

def main():
    init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        draw()
        pygame.display.flip()
        pygame.time.wait(10)

main()
