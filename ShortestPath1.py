"""Djikstra's Path Finding"""
#import pygame
import numpy as np
import sys, random, math
from collections import deque
#from tkinter import messagebox, Tk
from Simulation2 import CrossWall
'''
pygame.init()
win = pygame.display.set_mode(size)
pygame.display.set_caption("Dijktdtra's Path Finding")
clock = pygame.time.Clock()
'''

class Spot:
    def __init__(self, i, j):
        self.x, self.y = i, j
        self.f, self.g, self.h = 0, 0, 0
        self.neighbors = []
        self.prev = None
        self.wall = False
        self.visited = False
        if (i+j)%7 == 0:
            self.wall == True
        #if random.randint(0, 100) < 20:
            #self.wall = True
        
    '''
    def show(self, win, col, shape= 1):
        if self.wall == True:
            col = (70, 0, 100)
        if shape == 1:
            pygame.draw.rect(win, col, (self.x*w, self.y*h, w-1, h-1))
        else:
            pygame.draw.circle(win, (0,0,200), (self.x*w+w//2, self.y*h+h//2), w//3)
    '''
    def add_neighbors(self, grid):
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x+1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x-1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y+1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y-1])
        #Add Diagonals
        if self.x < cols - 1 and self.y < rows - 1:
            self.neighbors.append(grid[self.x+1][self.y+1])
        if self.x < cols - 1 and self.y > 0:
            self.neighbors.append(grid[self.x+1][self.y-1])
        if self.x > 0 and self.y < rows - 1:
            self.neighbors.append(grid[self.x-1][self.y+1])
        if self.x > 0 and self.y > 0:
            self.neighbors.append(grid[self.x-1][self.y-1])


def clickWall(pos, state):
    i = pos[0] #// w
    j = pos[1] #// h
    grid[i][j].wall = True
    
def place(pos):
    i = pos[0] // w
    j = pos[1] // h
    return w, h
    
   
cols, rows = 95, 54
size = (width, height) = 950, 540
w = width//cols
h = height//rows 
grid = [] 
 
 
def ShortestPath(i1,j1 , i2,j2 , CrossWall , OBS):
    
    global grid, w, h, size, cols, rows
    
    grid = []
    wall = [] + CrossWall
    queue, visited = deque(), []
    path = []
    PATH = []
    for i in range(cols):
        arr = []
        for j in range(rows):
            arr.append(Spot(i, j))
        grid.append(arr)
    
    for i in range(cols):
        for j in range(rows):
            grid[i][j].add_neighbors(grid)
    
    i1 = int(random.uniform(i1-1, i1 +2))
    i2 = int(random.uniform(i2-1, i2 +2))
    j1 = int(random.uniform(j1-1, j1 +2))
    j2 = int(random.uniform(j2-1, j2 +2))
        
    start = grid[i1][j1]
    end = grid[i2][j2]
    start.wall = False
    end.wall = False
    
    queue.append(end)
    end.visited = True
    
    for obs in OBS :
        if type(obs) != list :
            obs = obs.tolist()
        if (len(obs) == 2) :
            obs.append(1)
            obs.append(1)
        obs[2] = obs[0]
        obs[3] = obs[1]
        if len(wall) < (len(CrossWall) +4) :
            wall.append(obs)
    #print("zzzzzzzzzzzzzzzzz",wall)
    
    for item in wall :
        if (item[0]) == (item[2]) and (item[1]) == (item[3]) :
                for i in range((round(item[0])-1), (round(item[0])+1)) :
                    for j in range((round(item[1])-1), (round(item[1])+1)) :
                        grid[i][j].wall = True
        else :
            if (item[0]) > (item[2]) :
                X1 = item[0]
                X2 = item[2]
            if (item[2]) > (item[0]) :
                X1 = item[2]
                X2 = item[0]
            if (item[1]) > (item[3]) :
                Y1 = item[1]
                Y2 = item[3]
            if (item[3]) > (item[1]) :
                Y1 = item[3]
                Y2 = item[1]
               
            if (item[1]) == (item[3]) :
                Y1 = round(item[1]) +1
                Y2 = round(item[1]) -1
                
            if (item[0]) == (item[2]) :
                X1 = round(item[0]) +1
                X2 = round(item[0]) -1
                
            for i in range((int(X2)), (round(X1))) :
                for j in range((int(Y2)), (round(Y1))) :
                    grid[i][j].wall = True
                    if i >= 65 :
                        grid[i-1][j].wall = True
                    if j >= 31 :
                        grid[i][j-1].wall = True
                    if i < 65 :
                        grid[i+1][j].wall = True
                    if j < 31 :
                        grid[i][j+1].wall = True
                    #clickWall([i, j], True)
                    
    flag = False
    noflag = True
    startflag = True
    

    '''
    if startflag == True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in (1, 3):  
                clickWall(pygame.mouse.get_pos(), event.button == 1)
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0] or event.buttons[2]:
                    clickWall(pygame.mouse.get_pos(), event.buttons[0])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    startflag = True
    '''            
    while startflag:

        if len(queue) > 0 :
            current = queue.popleft()
            if current == start:
                temp = current
                while temp.prev:
                    path.append(temp.prev)
                    temp = temp.prev 
                for item in path:
                    PATH.append([item.x, item.y])
                    PATH = deque(PATH)
                #print(PATH)
                del grid
                startflag = False
                return PATH

                if not flag:
                    flag = True
                    print("Done")
                
                elif flag:
                    continue 
            if flag == False:
                for i in current.neighbors:
                    if not i.visited and not i.wall:
                        i.visited = True
                        i.prev = current
                        queue.append(i)
        
        else:
            if noflag and not flag :
                #Tk().wm_withdraw()
                # messagebox.showinfo("No Solution", "There was no solution" )
                print("There was no solution" )
                noflag = False
                return []
            else :
                continue
        
    '''
    win.fill((0, 20, 20))
    for i in range(cols):
        for j in range(rows):
            spot = grid[i][j]
            spot.show(win, (144, 240, 240))
            if spot in path:
                spot.show(win, (246, 204, 53))
                spot.show(win, (192, 57, 43), 0)
    
            elif spot.visited:
                spot.show(win, (15, 180, 130))
            if spot in queue and not flag:
                spot.show(win, (255, 162, 80))
                spot.show(win, (39, 200, 56), 0)
            if spot == start:
                spot.show(win, (0, 255, 120))
            if spot == end:
                spot.show(win, (0, 120, 255))
    
    pygame.display.flip()
    '''
ShortestPath(2, 2, 5 ,5 , [[3,1 , 3,10]] , [[1,2,1,2]])