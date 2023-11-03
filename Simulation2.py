# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 10:14:30 2021

@author: Hp
"""
from typing import Any
import pygame
import pygame.draw
import numpy as np
from agent2 import *
from agent2 import Task
from tools2 import *
from config import *
import time
import matplotlib.pyplot as plt
import matplotlib 
import matplotlib.backends.backend_agg as agg
import random, math

SCREENSIZE = [1280, 680]
RESOLUTION = 500

AGENTS1NUM = 3
AGENTS2NUM = 3

AGENTSNUM = AGENTS1NUM + AGENTS2NUM
Productivity = 0
delivery = 0

BACKGROUNDCOLOR = [255,255,255]
AGENTCOLOR = [0,255,0]

LINECOLOR0 = [0,255,255] # for drawing shear walls
LINECOLOR1 = [0,0,255] # for drawing exterior walls
LINECOLOR2 = [0,255,55] # for drawing interior walls
LINECOLOR3 = [0,0,255] # for drawing headland edges

LINEWEIGHT0 = 15 # for drawing shear walls
LINEWEIGHT1 = 7 # for drawing finished walls
LINEWEIGHT3 = 2 # for drawing headland edges

Yellow = []
Orange = []
Red = []

AGENTSIZE = 9
AGENTSICKNESS = 2

TASKNUM = 4
TASKSIZE = 10
TASKCOLOR = [255,0,0]
#WALLSFILE = "walls.csv"

plan = pygame.image.load('plan2.jpg')
plan = pygame.transform.scale(plan , (960,540))
Stopwatch = pygame.image.load('Stopwatch.gif')
Stopwatch = pygame.transform.scale(Stopwatch, (110,110))
Job = pygame.image.load('Job.png')  
Job = pygame.transform.scale(Job, (40,40))
Loading = pygame.image.load('loading.png')
Loading = pygame.transform.scale(Loading, (110,110))

pygame.init()
screen = pygame.display.set_mode(SCREENSIZE)
pygame.display.set_caption('Social Force Model')
clock = pygame.time.Clock()

f1 = []
f2 = []
######################### displaying plot by pygame  ##################################

matplotlib.use('Agg')

def plot(data) :
  
    ax.plot(data)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    
    return pygame.image.fromstring(raw_data, size, 'RGB')

############################## walls and boundaries ##################################################
### shear walls
walls0 = [[7.6,17.9 , 17.1,17.9] , [8.3,18.49 , 8.3,29.2] , [7.6,28.5 , 17.2,28.5] , [16.5,27.9 , 16.5,23.5],
         [14.5,43 , 14.5,53],
         [66.8,52.2 , 89.4,52.2] , [88.7,52 , 88.7,36.8] , [88.7,36.8 , 88.7,27.1],
         [31,23 , 31,24]]
### exterior walls
walls1 = []
### interior walls
walls2 = [[47.3,1.7 , 47.3,17] , [34.5,15.2 , 47.3,15.2] ,  [34.7,15.4 , 34.7,18.7] , [47.3,17 , 47.3,23] , [34.6,17.2 , 33.1,17.2],
          [34.5,22.8 , 47.2,22.8] , [34.7,23 , 34.7,30.51] , [39.1,30.2 , 47.2,30.2] , [47.3,23 , 47.3,30.51] ,
          [25.1,1.7 , 25.1,6] , [24.9,5.8 , 23.3,5.8] , [23.51,6 , 23.51,18] , [23.8,17.3 , 27.3,17.3] ,
          [26.5,37.2 , 25.1,37.2] , [25.4,37 , 25.4,30.4] , [27.3,30.1 , 23.3,30.1] , [23.4,30.51 , 23.4,29],
          [16.5,23.7 , 23.6,23.7] , [7,43 , 13.6,43] , [26.6,43 , 26.6,37]]
          

HeadlandEdge = [[2,1.7 , 94.2,1.7] , [94.2,1.7 , 94.2,27.5] , [94.51,27.5 , 89.8,27.5] , [89,37 , 89,46.7] ,
                [2,1.7 , 2,52.4] , [2,52.4 , 66.5,52.4] ,
                [15.3,43.4 , 26.51,43.4] , [26.51,43.4 , 26.51,52.4] , [14.51,43.2 , 10.1,43.2] ,
                [9.5,26.2 , 15.5,26.2] , [10.1,43.49 , 10.1,45] , [10.1,45 , 14.51,45] ,
                [44.5,15.5 , 44.5,22.5] , [47.3,15.5 , 47.3,22.5] , [44.5,15.5 , 47.3,15.5] , [44.5,22.5 , 47.3,22.5] ,
                [59.49,47 , 64.3,47] , [64.3,47 , 64.3,52.51] ,
                [41,45 , 51.7,45] , [59.7,52.4 , 59.7,37.2] , [59.7,37.2 , 34.5,37.2] , [34.5,37.2 , 34.5,45.5]]

SupplyStorage = [[57,7 , 57,23] , [57,7 , 77,7] , [77,7 , 77,23] , [77,23 , 57,23]]

Wall1 = deque(walls1)
Wall2 = deque(walls2)         

SpaceLimits = walls0 + HeadlandEdge

print(SpaceLimits)
DevelopingWall = []
FinishWall = [[1.7,1.7 , 15.9,1.7] , [21.4,1.7 , 27,1.7] , [32.51,1.7 , 38,1.7] , [43.6,1.7 , 49.1,1.7] , [54.7,1.7 , 60.3,1.7] , [65.8,1.7 , 71.3,1.7] , [76.9,1.7 , 94.51,1.7],
              [2,1.8 , 2,7.9] , [2,13 , 2,17.51] , [1.7,17.51 , 7.51,17.51] , [2,28.49 , 2,29] , [2,36.51 , 2,52.8] ,
              [1.7,52.51 , 13.51,52.51] , [15.49,52.51 , 66.51,52.51] , [2,17.51 , 7.6,17.51] ,
              [59.7,52.1 , 59.7,37.1] , [60,37.2 , 34.2,37.2] , [34.5,37.51 , 34.51,45.8] , [15.4,43.4 , 26.7,43.4] ,
              [94.2,8.1 , 94.2,2] , [94.2,27.51 , 94.2,21.1] , [89.49,27.55 , 94.5,27.55]]

############################# columns ################################################

obstackles = [[24.5,6.7] , [59.5,6.7] , [88,6.7] , [26.8,37.5] , [26.8,43.3]] 
Barrier = []
CrossWall = []
CrossWall.extend(DevelopingWall)
CrossWall.extend(FinishWall)
CrossWall.extend(SpaceLimits)

######################################################################################
# initial tasks
task1 = Task()
task2 = Task()
task3 = Task()
tasks = [task1]
Task1 = []
Task2 = []
Task3 = []

# defining supply chain and material delivery
brick_num = 0
cement_volumeLitr = 0
sand_volumeLitr = 0
water_volumeLitr = 0
mortar_volumeLitr = 0
mortar = 0

brick = 0
cement = 0
sand = 0
water = 0
mortar = 0
DeliveredWork = 0

WallSurface = 0
Efficiency2 = 1
Efficiency3 = 1

D1 = []
D2 = []
M2 = []
M3 = []

demand1 = deque(D1)
demand2 = deque(D2)
material2 = deque(M2)
material3 = deque(M3)

##################### for representing charts ######################################

Water = [0]
Sand = [0]
Cement = [0]
MortarV = [0]
Brick = [0]
Mortar = [0]
Delivery = [0]
n = 1
m = 1
####################################################################################
T2 = 0
T3 = 0
# initialize agents

agents1 = []
agents2 = []
prd = [0]

for n in range(AGENTS1NUM):
    agent1 = Agent1()
    agents1.append(agent1)
for n in range(AGENTS2NUM):
    agent2 = Agent2()
    agents2.append(agent2)
agents = agents1 + agents2
   

time = 0
running = True
times = [0]

rr = 1.5
R = 1.25
# showing the results
x_axis = [0]
y_axis = [0]

realTime_productivity = 10
realTime_p = []
####################################################################################################        
#######################       START       ##########################################################
####################################################################################################
def main():
    global time, n, water, sand, cement, mortar, mortar_volumeLitr, ax, canvas, WallSurface , CrossWall , PATH
    global DeliveredWork, delivery, sand_volumeLitr, water_volumeLitr, cement_volumeLitr, brick_num, brick
    global realTime_productivity, realTime_p
    running = True
    while running :
        if (DeliveredWork + delivery) >= realTime_productivity :
            realTime_p.append(time)
            realTime_productivity += 10
        print("vvvvvvvvvv ",realTime_p ,DeliveredWork)
    #########################################################################    
        if DevelopingWall.__len__() == 0 and walls2.__len__() == 0 :
            Productivity = DeliveredWork / time
            running = False
           
    #####################################################################################################
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (mouseX, mouseY) = pygame.mouse.get_pos()
            # elif event.type == pygame.MOUSEBUTTONUP:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = True
                    
    ################# display ###########################################################################  
        time = time + (1/120)

        screen.fill(BACKGROUNDCOLOR)
        screen.blit(plan, (0 , 0))
        myfont = pygame.font.SysFont('Calibry', 18)
        timeDisplay = myfont.render(str(round(time, 3)) ,1 ,[250,0,50])
        screen.blit(timeDisplay , (1195,75))
        screen.blit(Stopwatch ,(1150,10))
        
        myfont1 = pygame.font.SysFont('Calibry', 26)
        SUPPLY = myfont1.render('Supply Storage' ,1 ,[0,0,50])
        Lifter = myfont1.render('Lifter' ,1 ,[0,0,50])
        screen.blit(SUPPLY , (590,90))
        screen.blit(Lifter , (840,140))
    
    ############## draw walls  ##########################################################################
        
        for wall in walls0 : # for drawing shear walls
            startPos = np.array([wall[0],wall[1]])
            endPos = np.array([wall[2],wall[3]])
            startPx = startPos*10 #worldCoord2ScreenCoord(startPos,SCREENSIZE,RESOLUTION)
            endPx = endPos*10 #worldCoord2ScreenCoord(endPos,SCREENSIZE,RESOLUTION)
            pygame.draw.line(screen, LINECOLOR0,startPx,endPx, LINEWEIGHT0)
            
        for wall in FinishWall : # for drawing exterior walls
            startPos = np.array([wall[0],wall[1]])
            endPos = np.array([wall[2],wall[3]])
            startPx = startPos*10 #worldCoord2ScreenCoord(startPos,SCREENSIZE,RESOLUTION)
            endPx = endPos*10 #worldCoord2ScreenCoord(endPos,SCREENSIZE,RESOLUTION)
            pygame.draw.line(screen, LINECOLOR1,startPx,endPx, LINEWEIGHT1)
            
        for edge in HeadlandEdge : # for drawing headland edges
            startPos = np.array([edge[0],edge[1]])
            endPos = np.array([edge[2],edge[3]])
            startPx = startPos*10 #worldCoord2ScreenCoord(startPos,SCREENSIZE,RESOLUTION)
            endPx = endPos*10 #worldCoord2ScreenCoord(endPos,SCREENSIZE,RESOLUTION)
            pygame.draw.line(screen, LINECOLOR3,startPx,endPx, LINEWEIGHT3)
    
    ############################ update walls ###########################################################
    
        for walls in DevelopingWall :
            
            # stimated time for each square meter of brick laying is about 21.34 minute but according to pdf of  our workshop records its about (random.uniform(19 , 24))
            WallSurface = 3.5 * (math.sqrt((DevelopingWall[0][0] - DevelopingWall[0][2])**2 + (DevelopingWall[0][1] - DevelopingWall[0][3])**2))
            WallSurface = WallSurface / 5.2 # each square meter in screen is equal to 5.2 units
            
            startPos = np.array([walls[0],walls[1]])
            endPos = np.array([walls[2],walls[3]])
            startPx = startPos*10 #worldCoord2ScreenCoord(startPos,SCREENSIZE,RESOLUTION)
            endPx = endPos*10 #worldCoord2ScreenCoord(endPos,SCREENSIZE,RESOLUTION)
            pygame.draw.line(screen, (200,200,200),startPx,endPx, 7)
            
    #####################################################################################################
    
        for point in Yellow :
            pygame.draw.circle(screen, [255,255,51], point, 5)
        for point in Orange :
            pygame.draw.circle(screen, [255,165,0], point, 5)
        for point in Red :
            pygame.draw.circle(screen, [255,0,0], point, 5)     
            
    #####################################################################################################      
        for task in tasks:
            #pygame.display.flip()  
            #pygame.draw.circle(screen, TASKCOLOR, T_scPos, TASKSIZE)
                
                
            if math.floor(time) == n :
                n += 1
    
                prd.append(DeliveredWork)
                #MortarV.append(mortar_volumeLitr)
                #Water.append(water)
                #Cement.append(cement)
                #Sand.append(sand)
                Delivery.append(delivery)
                #Brick.append(brick)
                Mortar.append(mortar)
                
            
                fig0 = plt.figure(figsize=[4.7, 2.6])
                ax = fig0.add_subplot(111)
                canvas = agg.FigureCanvasAgg(fig0)
                data0 = np.array(prd)
                surf0 = plot(data0)
                
                #fig1 = plt.figure(figsize=[5, 2.8])
                #ax = fig1.add_subplot(111)
                #canvas = agg.FigureCanvasAgg(fig1)
                #data1 = np.array(Water)
                #surf1 = plot(data1)
                
                #fig2 = plt.figure(figsize=[4.7, 2.6])
                #ax = fig2.add_subplot(111)
                #canvas = agg.FigureCanvasAgg(fig2)
                #data2 = np.array(Sand)
                #surf2 = plot(data2)
              
                #fig3 = plt.figure(figsize=[4.7, 2.6])
                #ax = fig3.add_subplot(111)
                #canvas = agg.FigureCanvasAgg(fig3)
                #data3 = np.array(Cement)
                #surf3 = plot(data3)
            
                #fig4 = plt.figure(figsize=[4.7, 2.6])
                #ax = fig4.add_subplot(111)
                #canvas = agg.FigureCanvasAgg(fig4)
                #data4 = np.array(MortarV)
                #surf4 = plot(data4)
            
                #fig5 = plt.figure(figsize=[5, 2.8])
                #ax = fig5.add_subplot(111)
                #canvas = agg.FigureCanvasAgg(fig5)
                #data5 = np.array(Brick)
                #surf5 = plot(data5)
            
                fig6 = plt.figure(figsize=[4.7, 2.6])
                ax = fig6.add_subplot(111)
                canvas = agg.FigureCanvasAgg(fig6)
                data6 = np.array(Mortar)
                surf6 = plot(data6)
            
                fig7 = plt.figure(figsize=[4.7, 2.6])
                ax = fig7.add_subplot(111)
                canvas = agg.FigureCanvasAgg(fig7)
                data7 = np.array(Delivery)
                surf7 = plot(data7)
                
            if math.floor(time) == 0 :
                
                surf0 = Loading
                surf1 = Loading
                surf2 = Loading
                surf3 = Loading
                surf4 = Loading
                surf5 = Loading
                surf6 = Loading
                surf7 = Loading
              
            screen.blit(surf0 , (950 , 120))
            #screen.blit(surf1 , (5 , 480))
            #screen.blit(surf2 , (330 , 480)) 
            #screen.blit(surf3 , (5 , 480))
            #screen.blit(surf4 , (950 , 300))
            #screen.blit(surf5 , (330 , 480))
            screen.blit(surf6 , (950 , 300))
            screen.blit(surf7 , (950 , 480))
            
            
    ################# defining workpackage delivery ratio in each activity  ############################       
        for task in tasks:
            
            if water < 0 :
                water = 0
            if sand < 0 :
                sand = 0
            if cement < 0 :
                cement = 0
            if mortar_volumeLitr < 0 :
                mortar_volumeLitr = 0
            if mortar < 0 :
                mortar = 0
            if brick < 0 :
                brick = 0
           
    
        for task in Task1 :
            
            myfont2 = pygame.font.SysFont('Calibry', 20)
            
            brickSupply = myfont.render(str(round(brick_num , 1)) ,1 ,[0,0,250])
            br = myfont2.render('brick : ' ,1 ,[0,0,250])
            
            cementSupply = myfont.render(str(round(cement_volumeLitr , 1)) ,1 ,[0,0,250])
            ce = myfont2.render('cement : ' ,1 ,[0,0,250])
            
            waterSupply = myfont.render(str(round(water_volumeLitr , 1)) ,1 ,[0,0,250])
            wa = myfont2.render('water : ' ,1 ,[0,0,250])
            
            sandSupply = myfont.render(str(round(sand_volumeLitr , 1)) ,1 ,[0,0,250])
            sa = myfont2.render('sand : ' ,1 ,[0,0,250])
            
            screen.blit(brickSupply , (670,130))
            screen.blit(br , (600,130))
            
            screen.blit(cementSupply , (670,150))
            screen.blit(ce , (600,150))
            
            screen.blit(waterSupply , (670,170))
            screen.blit(wa , (600,170))
            
            screen.blit(sandSupply , (670,190))
            screen.blit(sa , (600,190))
    
    ############################ drawing columns ##################################################
        for obs in obstackles:
            obs_scPos = [0.0 , 0.0] 
            obs_scPos[0] = obs[0] *10
            obs_scPos[1] = obs[1] *10
            
            #print (obs_scPos)
    
            pygame.draw.rect(screen ,(0,100,0) ,(obs_scPos[0]-5,obs_scPos[1]-5 , 12,12))
            
    ###############################################################################################
    ##########################                            #########################################
    ##########################         # agent 1 #        #########################################
    ##########################                            #########################################
    ###############################################################################################
       
        for agent in agents1:
                        
            agent.path = deque(agent.path)

            screen.blit(Job, [agent.TaskPos[0]*10 , agent.TaskPos[1]*10])
                           
            scPos = agent.pos*10 #worldCoord2ScreenCoord(agent.pos, SCREENSIZE, RESOLUTION)
            # scPos=screen position
            scPos = [0, 0]
            scPos[0] = int(agent.pos[0]*10)  #worldCoord2ScreenCoord(agent.pos, SCREENSIZE, RESOLUTION)
            scPos[1] = int(agent.pos[1]*10)
            
            scDest=[0,0]
            scDest[0]= int(agent.dest[0] *10)
            scDest[1]= int(agent.dest[1] *10)
            
            endPos = [0, 0]
            endPos[0] = int(agent.pos[0]*10 + agent.actualV[0]*10)
            endPos[1] = int(agent.pos[1]*10 + agent.actualV[1]*10)
    
            endPosDV = [0, 0]
            endPosDV[0] = int(agent.pos[0]*10 + agent.desiredV[0]*10)
            endPosDV[1] = int(agent.pos[1]*10 + agent.desiredV[1]*10)
    
            pygame.draw.circle(screen, AGENTCOLOR, scPos, AGENTSIZE, AGENTSICKNESS)
            pygame.draw.line(screen, [0,0,0], scPos, endPos, 2)
            pygame.draw.line(screen, [255,60,0], scPos, endPosDV, 2)
            
            print(scPos)
    
            pygame.display.flip()
            clock.tick(100) # 100 ticks per milisecond/1000
            clock.get_time()
            #print(pygame.time.Clock())
            
    ######################################################################################################

            for pp in agent.path :
                p_scPos = [0.0 , 0.0]
                p_scPos[0] = int(pp[0] *10)
                p_scPos[1] = int(pp[1] *10)
                
                pygame.draw.circle(screen, [255,0,0], p_scPos , 2)
    
    ######################################################################################################
                          
            if (water <= 4) and ('water' not in demand1) and (['water'] not in f1) :
                demand1.append('water')
                
            if (cement < 1) and ('cement' not in demand1) and (['cement'] not in f1) :
                demand1.append('cement')
                
            if (sand < 5) and ('sand' not in demand1) and (['sand'] not in f1) :
                demand1.append('sand')
                
            if (brick < 10) and ('brick' not in demand1) and (['brick'] not in f1) :
                demand1.append('brick')           
    
    ###################################################################################################
                    
        for aidai,ai in enumerate(agents1):
            ai.crossline.clear()
            if ai.haul not in f1 :
                f1.append(ai.haul) 
              
    ######################################################################################################
    
            if (ai.path.__len__() > 0) and ((ai.path[ai.S][0])-R <= ai.pos[0] <= (ai.path[ai.S][0])+R) and ((ai.path[ai.S][1])-R <= ai.pos[1] <= (ai.path[ai.S][1])+R):
                if ai.times.__len__() >= 2 :
                    ai.times.popleft()
                if ai.S < (ai.path.__len__()-1) :
                    ai.S = ai.S + 1
                                    
    ####################### defining hauling for each agent ##############################################     
            if ai.haul.__len__() == 0 :
                ai.TaskPos[0] = 70
                ai.TaskPos[1] = 20

                if ((70)-rr <= ai.pos[0] <= (70)+rr) and ((20)-rr <= ai.pos[1] <= (20)+rr) and (ai.activity == 1) :
                    if (demand1.__len__() > 0) and (demand1[0] != 'brick') and (ai.haul.__len__() == 0):
                            ai.haul.append(demand1[0])
                            demand1.popleft()
                            ai.path.clear()
                            ai.S = 0
                    if (demand1.__len__() > 0) and (demand1[0] == 'brick') and (ai.haul.__len__() == 0) :
                            ai.haul.append(demand1[0])
                            demand1.popleft()
                            ai.path.clear()
                            ai.S = 0
  
                if (ai.path.__len__() == 0) :
                    ai.S = 0
                    ai.path = ai.PathFinding(ai.pos[0],ai.pos[1] , ai.TaskPos[0],ai.TaskPos[1] , CrossWall ,[])

            if ai.haul.__len__() == 1 :
                
                if (len(ai.path) > 0) :
                    if ai.S == (len(ai.path) -1) :
                        ai.path.clear()
                                        
                if ((70)-rr <= ai.pos[0] <= (70)+rr) and ((20)-rr <= ai.pos[1] <= (20)+rr) and (ai.activity == 1) :
                    if ai.haul[0] == 'brick' :
                        brick_num = brick_num - 30
                        
                    if ai.haul[0] == 'cement' :
                        cement_volumeLitr = cement_volumeLitr - 20
                        
                    if ai.haul[0] == 'water' :
                        water_volumeLitr = water_volumeLitr - 4
                        
                    if ai.haul[0] == 'sand' :
                        sand_volumeLitr = sand_volumeLitr - 40
                    
                    if ai.activity - ai.haul.__len__() == 0 :
                            ai.times.append(round(time ,2))
                            
                    ai.activity = ai.activity +1
    
                if ('water' in ai.haul) or ('cement' in ai.haul) or ('sand' in ai.haul) :
                    ai.TaskPos[0] = 30
                    ai.TaskPos[1] = 23
                    
                    if (ai.path.__len__() == 0) :
                        ai.S = 0
                        ai.path = ai.PathFinding(ai.pos[0],ai.pos[1] , ai.TaskPos[0],ai.TaskPos[1] , CrossWall ,[])

                    if ((30)-rr <= ai.pos[0] <= (30)+rr) and ((23)-rr <= ai.pos[1] <= (23)+rr) and (ai.activity == 2):
     
                        if ai.haul.__len__() == 1 :
                            material2.append(ai.haul[0])
                            if ai.haul[0] == 'water' :
                                water = water + 8
                            if ai.haul[0] == 'cement' :
                                cement = cement + 20 
                            if ai.haul[0] == 'sand' :
                                sand = sand + 40
                                
                            if (water >= 8) and (cement >= 1) and (sand >= 5) :
                                T2 = time    
                        ai.path.clear()
                        ai.S = 0   
                        ai.haul.clear()                       
    
                        if ai.activity - ai.haul.__len__() == 2 :
                            ai.times.append(round(time ,2))
                            
                        ai.activity = ai.activity -1    
                                                            
                if 'brick' in ai.haul :
                    
                    if (DevelopingWall.__len__() != 0) and (ai.haul.__len__() == 1) :
                        
                        if DevelopingWall[0][0] == DevelopingWall[0][2] :
                            if DevelopingWall[0][0] >= 45 :
                                WS = -4
                            else :
                                WS = +4
                            ai.TaskPos[0] = ((DevelopingWall[0][0] + DevelopingWall[0][2]) /2) + WS
                            ai.TaskPos[1] = (DevelopingWall[0][1] + DevelopingWall[0][3]) /2
                        if DevelopingWall[0][1] == DevelopingWall[0][3] :
                            if DevelopingWall[0][1] <= 25 :
                                WS = +4
                            else :
                                WS = -4
                            ai.TaskPos[0] = (DevelopingWall[0][0] + DevelopingWall[0][2]) /2
                            ai.TaskPos[1] = ((DevelopingWall[0][1] + DevelopingWall[0][3]) /2) + WS 
                
                    if ((ai.TaskPos[0])-rr <= ai.pos[0] <= (ai.TaskPos[0])+rr) and ((ai.TaskPos[1])-rr <= ai.pos[1] <= (ai.TaskPos[1])+rr) and (ai.activity == 2):
                        if ai.haul.__len__() == 1 :
                            material3.append(ai.haul[0])
                            ai.haul.clear()
                            brick = brick + 30
                            
                            if (brick >= 15) or (mortar >= 6) or (material3.__len__() == 2):
                                T3 = time
                                
                            ai.TaskPos[0] = 70
                            ai.TaskPos[1] = 20
                            
                            ai.path.clear()
                            ai.S = 0
                            
                            if ai.activity - ai.haul.__len__() == 2 :
                                ai.times.append(round(time ,2))
                                
                            ai.activity = ai.activity -1
                            
                    if (ai.path.__len__() == 0) :
                        ai.S = 0
                        ai.path = ai.PathFinding(ai.pos[0],ai.pos[1] , ai.TaskPos[0],ai.TaskPos[1] , CrossWall ,[])
                        
    ###################################################################################################
                    
            if ai.haul.__len__() == 1 :
                if ai.haul[0] == 'water' :
                    ai.mass = 80 + 8 + 1.5 # worker weight + material weight + container weight
                if ai.haul[0] == 'sand' :
                    ai.mass = 80 + 62 + 7 # worker weight + material weight + wheelbarrow weight
                if ai.haul[0] == 'cement' :
                    ai.mass = 80 + 25 # worker weight + material bag weight
            else :
                ai.mass = 80
    ###################################################################################################
        
            if (-0.07 < ai.actualV[0] < +0.07) and (-0.07 < ai.actualV[1] < +0.07) and (ai.command(ai.TaskPos[0] , ai.TaskPos[1] , time) == 'go') :
                if (len(ai.path) > 0) :
                    ai.path.clear()

                ai.S = 0
                ai.path = ai.PathFinding(ai.pos[0],ai.pos[1] , ai.TaskPos[0],ai.TaskPos[1] , CrossWall ,Barrier)
                if (len(Barrier) > 0) :
                    Barrier.clear()
    ###################################################################################################
    ###################                                  ##############################################
    ###################             # agent 2 #          ##############################################
    ###################                                  ##############################################
    ###################################################################################################
            
        for agent in agents2:
            
            agent.path = deque(agent.path)

            scPos = agent.pos*10 #worldCoord2ScreenCoord(agent.pos, SCREENSIZE, RESOLUTION)
            # scPos=screen position
            scPos = [0, 0]
            scPos[0] = int(agent.pos[0]*10)  #worldCoord2ScreenCoord(agent.pos, SCREENSIZE, RESOLUTION)
            scPos[1] = int(agent.pos[1]*10)
            
            scDest=[0,0]
            scDest[0]= int(agent.dest[0] *10)
            scDest[1]= int(agent.dest[1] *10)
            
            endPos = [0, 0]
            endPos[0] = int(agent.pos[0]*10 + agent.actualV[0]*10)
            endPos[1] = int(agent.pos[1]*10 + agent.actualV[1]*10)
    
            endPosDV = [0, 0]
            endPosDV[0] = int(agent.pos[0]*10 + agent.desiredV[0]*10)
            endPosDV[1] = int(agent.pos[1]*10 + agent.desiredV[1]*10)
    
            pygame.draw.circle(screen, AGENTCOLOR, scPos, AGENTSIZE, AGENTSICKNESS)
            pygame.draw.line(screen, [0,0,0], scPos, endPos, 2)
            pygame.draw.line(screen, [255,60,0], scPos, endPosDV, 2)
            
            print(scPos)
    
            pygame.display.flip()
            clock.tick(50) # 100 ticks per milisecond/1000
            clock.get_time()
            #print(pygame.time.Clock())
    
    ######################################################################################################
    
            for p in agent.path :
                p_scPos = [0.0 , 0.0]
                p_scPos[0] = int(p[0] *10)
                p_scPos[1] = int(p[1] *10)
                
                pygame.draw.circle(screen, [0,0,255], p_scPos , 2)        
    
    ##################################################################################################
            
            if (mortar < 6) and ('mortar' not in demand2) and (['mortar'] not in f2) :
                demand2.append('mortar')
                
    ##################################################################################################
    
        for idbi,bi in enumerate(agents2):
            bi.crossline.clear()
            if bi.haul not in f2 :
                f2.append(bi.haul) 
                
    ######################################################################################################
    
            if (bi.path.__len__() > 0) and ((bi.path[bi.S][0])-R <= bi.pos[0] <= (bi.path[bi.S][0])+R) and ((bi.path[bi.S][1])-R <= bi.pos[1] <= (bi.path[bi.S][1])+R):
                if bi.times.__len__() >= 2 :
                    bi.times.popleft()
                if bi.S < (bi.path.__len__()-1) :
                    bi.S = bi.S + 1   
                                             
    ################################ defining hauling for each agent #####################################

            if bi.haul.__len__() == 0 :
                
                bi.TaskPos[0] = 30
                bi.TaskPos[1] = 21
                          
                if ((30)-rr <= bi.pos[0] <= (30)+rr) and ((21)-rr <= bi.pos[1] <= (21)+rr) :
                    if (demand2.__len__() >= 1) and (mortar_volumeLitr >= 6) and (bi.haul.__len__() == 0) and (bi.activity == 1):
                        bi.haul.append(demand2[0])
                        demand2.popleft()
                        mortar_volumeLitr = mortar_volumeLitr - 6
                        
                        if bi.activity - bi.haul.__len__() == 0 :
                            bi.times.append(round(time ,2))
                        bi.path.clear()    
                        bi.activity = bi.activity +1
                        
                else :
                    if (bi.path.__len__() == 0) :
                        bi.S = 0
                        bi.path = bi.PathFinding(bi.pos[0],bi.pos[1] , bi.TaskPos[0],bi.TaskPos[1] , CrossWall ,[])
                        
            if bi.haul.__len__() == 1 :
                
                if (len(bi.path) > 0) :
                    if bi.S == (len(bi.path) -1) :
                        bi.path.clear()
                                        
                if DevelopingWall.__len__() != 0 :
                    if DevelopingWall[0][0] == DevelopingWall[0][2] :
                        if DevelopingWall[0][0] >= 45 :
                            WS = -4
                        else :
                            WS = +4
                        bi.TaskPos[0] = ((DevelopingWall[0][0] + DevelopingWall[0][2]) /2) + WS
                        bi.TaskPos[1] = ((DevelopingWall[0][1] + DevelopingWall[0][3]) /2)
                    if DevelopingWall[0][1] == DevelopingWall[0][3] :
                        if DevelopingWall[0][1] <= 25 :
                            WS = +4
                        else :
                            WS = -4  
                        bi.TaskPos[0] = (DevelopingWall[0][0] + DevelopingWall[0][2]) /2
                        bi.TaskPos[1] = ((DevelopingWall[0][1] + DevelopingWall[0][3]) /2) + WS 
                
                if (bi.path.__len__() == 0) and (bi.activity == 2) :
                    bi.S = 0
                    bi.path = bi.PathFinding(bi.pos[0],bi.pos[1] , bi.TaskPos[0],bi.TaskPos[1] , CrossWall ,[])
                    
                if ((bi.TaskPos[0])-rr <= bi.pos[0] <= (bi.TaskPos[0])+rr) and ((bi.TaskPos[1])-rr <= bi.pos[1] <= (bi.TaskPos[1])+rr) and (bi.activity == 2):
                    material3.append(bi.haul[0])
                    bi.haul.clear()
                    mortar = mortar + 6
                    
                    if (brick >= 10) or (mortar >= 6) or (material3.__len__() == 2):
                        T3 = time
                        
                    if bi.activity - bi.haul.__len__() == 2 :
                        bi.times.append(round(time ,2))
                    
                    bi.activity = bi.activity -1 
                    bi.path.clear()
                    bi.S = 0   
                    
    ###################################################################################################
    
            if bi.haul.__len__() == 1 : 
                if bi.haul[0] == 'mortar' :
                    bi.mass = 80 + 12.6 + 7 # worker weight + material weight + wheelbarrow weight
                if bi.haul[0] == 'brick' :
                    bi.mass = 80 + 2*30 + 7 # worker weight + weight of each brick * number of hauling bricks + wheelbarrow weight
            else :
                bi.mass = 80
 
    ###################################################################################################
    
            if (-0.07 < bi.actualV[0] < +0.07) and (-0.07 < bi.actualV[1] < +0.07) and (bi.command(bi.TaskPos[0] , bi.TaskPos[1] , time) == 'go') :
                 if (len(bi.path) > 0) :
                     bi.path.clear()
      
                 bi.S = 0
                 bi.path = bi.PathFinding(bi.pos[0],bi.pos[1] , bi.TaskPos[0],bi.TaskPos[1] , CrossWall ,Barrier)
                 if (len(Barrier) > 0) :
                     Barrier.clear()
    ###################################################################################################             
    ##############################  movement of agents  ###############################################
    ###################################################################################################
                    
        for idxi,xi in enumerate(agents):
            
    ############################# movement forces ######################################################   
         
        # start first task action
            xi.timeOut = pygame.time.get_ticks() / 1000
            
            if xi.command(xi.TaskPos[0] , xi.TaskPos[1] , time) == 'go' :
                # Movement of the agent starts
                # Initial speed and position
                v0 = xi.actualV
                r0 = xi.pos
                
                if len(xi.path) > 0 :
                    xi.destX = xi.path[xi.S][0]
                    xi.destY = xi.path[xi.S][1]
                else :
                    xi.S = 0
                    xi.path = xi.PathFinding(xi.pos[0],xi.pos[1] , xi.TaskPos[0],xi.TaskPos[1] , CrossWall ,[])
                    
                    
                    
                xi.dest = np.array([xi.destX ,xi.destY])
                xi.direction = normalize(xi.dest - xi.pos)
                xi.desiredV = xi.desiredSpeed*xi.direction
            
                # Calculate the force
                xi.interactionRange = xi.InterRange()
                
                adapt = xi.adaptVel()                
                peopleInter = 0.0
                wallInter = 0.0
                obsInter = 0.0
                
                for idxj, xj in enumerate(agents):
                    if idxj == idxi:
                        continue
                    peopleInter += xi.peopleInteraction(xj)
            
                for wall in CrossWall:
                    wallInter += xi.wallInteraction(wall)
                    
                for obs in obstackles:
                    obsInter += xi.obsInteraction(obs)
                    
                #print('Atraction force :', adapt)
                #print('Forces from Walls :', wallInter)
                #print('Forces from people :', peopleInter)
                
                xi.sumForce = (adapt)*xi.k + (wallInter)/xi.k + (peopleInter)/xi.k + (obsInter)/xi.k
                
                if (-0.01 < xi.actualV[0] < +0.01) and (-0.01 < xi.actualV[1] < +0.01) :
                    if (-0.01 < xi.sumForce[0] < +0.01) and (-0.01 < xi.sumForce[1] < +0.01) :
                        xi.k = 10
                    else : 
                        xi.k = 1
                
                if (100 < abs(xi.sumForce[0])) :
                    xi.sumForce[0] = xi.sumForce[0]/20
                if (100 < abs(xi.sumForce[1])) :
                    xi.sumForce[1] = xi.sumForce[1]/20
                    
                print('SUM Force :', xi.sumForce)
                        
                # Calculate acceleration
                accl = xi.sumForce/xi.mass
                # Computing speed
                xi.actualV = xi.actualV + accl*0.5 # consider dt = 0.5
                # Calculate displacement
                xi.pos = xi.pos + xi.actualV*0.5
                xi.pos = r0 + v0*0.5 + accl*0.25
                
                #print(accl,ai.actualV)
               
                if (len(Barrier) < AGENTSNUM) :
                    Barrier.append(xi.pos)
                
                if 1 <= peopleInter[0] < 7 or 1 <= peopleInter[1] < 7 :
                    scPos = [0, 0]
                    scPos[0] = int(xi.pos[0]*10)  #worldCoord2ScreenCoord(agent.pos, SCREENSIZE, RESOLUTION)
                    scPos[1] = int(xi.pos[1]*10)
                    Yellow.append(scPos)
                    pygame.draw.circle(screen, [250,250,51], scPos, 6)
                    pygame.display.flip()
                if 7 <= peopleInter[0] < 20 or 7 <= peopleInter[1] < 20 :
                    scPos = [0, 0]
                    scPos[0] = int(xi.pos[0]*10)  #worldCoord2ScreenCoord(agent.pos, SCREENSIZE, RESOLUTION)
                    scPos[1] = int(xi.pos[1]*10)
                    Orange.append(scPos)
                    pygame.draw.circle(screen, [255,165,0], scPos, 6)
                    pygame.display.flip()
                if 20 <= peopleInter[0] or 20 <= peopleInter[1] :
                    scPos = [0, 0]
                    scPos[0] = int(xi.pos[0]*10)  #worldCoord2ScreenCoord(agent.pos, SCREENSIZE, RESOLUTION)
                    scPos[1] = int(xi.pos[1]*10)
                    Red.append(scPos)
                    pygame.draw.circle(screen, [255,0,0], scPos, 6)
                    pygame.display.flip()
                
    ###################################################################################################
    ################################################################################################### 
        if 'water' in material2 :
            if 'water' in demand1 :
                demand1.remove('water')
            if water <= 8 :
                material2.remove('water')
    
        if 'cement' in material2 :
            if 'cement' in demand1 :
                demand1.remove('cement')
            if cement < 1 :
                material2.remove('cement')
                
        if 'sand' in material2 :
            if 'sand' in demand1 :
                demand1.remove('sand')
            if sand < 5 :
                material2.remove('sand')
    
        if 'brick' in material3 :
            if 'brick' in demand1 :
                demand1.remove('brick')
            if (brick < 10) :
                material3.remove('brick')
    
        if 'mortar' in material3 :
            if 'mortar' in demand2 :
                demand2.remove('mortar')
            if (mortar < 6) :
                material3.remove('mortar')
    #############################################################################################
            
        for task in tasks :
            ### work delivery 
            if (water > 4) and (cement > 1) and (sand > 5) :
                
                Duration2 = time - T2
                Efficiency2 = random.gammavariate(557.06, 0.03083)
    
                water = (-(random.triangular(4.1283,9.0271,7.4))/Efficiency2)*Duration2 + water
                cement = (-(random.weibullvariate(6.4124, 6.7173))/Efficiency2)*Duration2 + cement
                sand = (-(random.weibullvariate(5.7807, 32.159))/Efficiency2)*Duration2 + sand
                mortar_volumeLitr = (30/Efficiency2)*Duration2 + mortar_volumeLitr
                    
        for task in tasks :
            
            if (brick > 10) and (mortar > 3) :
                Duration3 = time - T3
                Efficiency3 = random.normalvariate(4.9534, 0.37423)
                
                brick = (-(random.gammavariate(33.714, 2.1027))/Efficiency3)*Duration3 + brick
                mortar = (-(random.lognormvariate(3.5298, 0.15794))/Efficiency3)*Duration3 + mortar
                delivery = (1/Efficiency3)*Duration3 + delivery
                
            if (delivery > WallSurface) and (DevelopingWall.__len__() == 1) : # when one wall is finished
                DeliveredWork = delivery + DeliveredWork
                FinishWall.append(DevelopingWall[0])
                DevelopingWall.clear()
                delivery = 0
    
            if DevelopingWall.__len__() == 0 :
                if walls1.__len__() > 0 :
                    DevelopingWall.append(walls1[0])
                    CrossWall.append(walls1[0])
                    walls1.remove(walls1[0])
                if walls1.__len__() == 0 and walls2.__len__() > 0 :
                    DevelopingWall.append(walls2[0])
                    CrossWall.append(walls2[0])
                    walls2.remove(walls2[0])  
                    
    ###################################################################################################    
    
        print ('haul :    ' , bi.haul)
        print ('queue1 of demand :    ',  demand1)
        print ('queue2 of demand :    ',  demand2)
        print ('material3 : ',  material3)
        print ('position is     : ' ,ai.pos)
        print ('DevelopingWall :      ', DevelopingWall)
        print ('Path A is :     ',  ai.path)
        print ('Path B is :     ',  bi.path)
        print ('timer : ', round(time , 2) , ' minutes')
        print ('activity :     ' , ai.activity)
        print ('speed is :     ' , ai.actualV)
        print ('step :     ' , ai.S )
        print ('Barrier' ,Barrier)
if __name__=="__main__":
    main()