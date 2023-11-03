# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 13:15:34 2020

@author: MAHDY
"""
import numpy as np
import sympy as sp
from tools2 import *
import random
from collections import deque



############################### defining tasks positions ###################################
class Task (object) :
    def __init__(self):
        duration = random.uniform(3,6)
        posX = 49
        posY = 10
        pos = np.array([posX , posY])

task1 = Task()    
task1.duration = random.uniform(3,6)
task1.posX = 71
task1.posY = 10

task2 = Task()    
task2.duration = random.triangular(3,5,7)
task2.posX = 48
task2.posY = 36

task3 = Task()    
task3.duration = random.normalvariate(2,4)
task3.posX = 3
task3.posY = 25

task4 = Task()    
task4.duration = random.gammavariate(5,3)   
task4.posX = 60
task4.posY = 30

##############################################################################################    
   
class Agent1(object):
    def __init__(self, x=1, y=1):
        # random initialize a agent
        
        self.posX = random.uniform(69,71)
        self.posY = random.uniform(19,21)
        self.pos = np.array([self.posX , self.posY])
        #self.pos = np.array([0.0, 0.0])

        self.actualVX = 0 #random.uniform(0,1.6)
        self.actualVY = 0 #random.uniform(0,1.6)
        self.actualV = np.array([self.actualVX , self.actualVY])
        #self.actualV = np.array([0.0, 0.0])
        
        self.destX = 77
        self.destY = 13
        self.dest = np.array([self.destX,self.destY])
        self.direction = normalize(self.dest - self.pos)
        #self.direction = np.array([0.0, 0.0])
        
        self.desiredSpeed = 0.575   # human walking speed in this workshop is about 0.7 m/s
        self.desiredV = self.desiredSpeed*self.direction
        # rest time
        self.acclTime = random.uniform(4,6) # 5.0
        self.drivenAcc = (self.desiredV - self.actualV)/self.acclTime
               
        self.mass = 80
        self.radius = 2.6 # equal to 0.5 m 
        self.radiusO = 2.6
        self.interactionRange = 5.2 # equal to 1 meter
        self.p = 2.6
        
        self.bodyFactor = 120000
        self.slideFricFactor = 240000
        self.A = random.uniform(0.6,1.2)
        self.B = random.uniform(0.6,1.2) #0.8 #0.08
        
        self.Goal = 2
        self.timeOut = 0.0
        
        self.haul = []
        self.T2 = 0
        #self.T3 = 0
        self.activity = 1
        self.S = 0
        self.h = 1
        self.dT2 = 0
        #self.dT3 = 0
        self.D2 = 0
        
        #print('X and Y Position:', self.pos)
        #print('self.direction:', self.direction)
        
        self.times = deque([0])
        self.delay = 0
   
        self.TaskPosX = 5
        self.TaskPosY = 7
        self.TaskPos = [self.TaskPosX,self.TaskPosY]
        self.path = []
        self.crossline = []
        self.distanceP2W = []
        self.k = 1 
        self.walls = []
        self.Obstackles = []
        self.sumForce = np.array([0,0])
############################################################################################
############################################################################################
  
    def PathFinding(self, pos_x,pos_y , taskpos_x,taskpos_y , CrossWall ,obs) :
        self.pos[0] = pos_x
        self.pos[1] = pos_y
        self.TaskPos[0] = taskpos_x
        self.TaskPos[1] = taskpos_y
        self.walls = CrossWall
        self.Obstackles = obs
        from ShortestPath import ShortestPath
        
        return ShortestPath(round(self.pos[0]) ,round(self.pos[1]) , round(self.TaskPos[0]) ,round(self.TaskPos[1]) , self.walls ,self.Obstackles)


    def CrossLine (self , w , v) :
        
        x = sp.Symbol("x")
        y = sp.Symbol("y")
        
        if v[0] == self.pos[0] :
            EQ = sp.solve([x - self.pos[0] , y - (((w[3] - w[1]) / (w[2] - w[0])) * (x - w[0])) - w[1]])
        if v[1] == self.pos[1] :
            EQ = sp.solve([y - v[1] , y - (((w[3] - w[1]) / (w[2] - w[0])) * (x - w[0])) - w[1]])
        if w[2] == w[0] :
            EQ = sp.solve([y - (((v[1]-self.pos[1])/(v[0]-self.pos[0])) * (x-v[0])) - v[1] , x - w[0]])
        else :
            EQ = sp.solve([y - (((v[1]-self.pos[1])/(v[0]-self.pos[0])) * (x-v[0])) - v[1] , y - (((w[3] - w[1]) / (w[2] - w[0])) * (x - w[0])) - w[1]])
        X = EQ[x]
        Y = EQ[y]
        print(X , Y)
        Xindex = [w[0] , w[2] , v[0] , self.pos[0]]
        Xindex.sort()
        Yindex = [w[1] , w[3] , v[1] , self.pos[1]]
        Yindex.sort()
        if (Xindex[1]-0.1 <= X <= Xindex[2]+0.1) and (Yindex[1]-0.1 <= Y <= Yindex[2]+0.1) :
            return 'yes'
        else :
            return 'no'
            
            
   
    def command (self,TaskposX , TaskposY , t) :
        Xpos = self.pos[0]
        Ypos = self.pos[1]
        self.TaskPos[0] = TaskposX
        self.TaskPos[1] = TaskposY
        time = t
        if (self.activity == 1) :
            if (66 -1 < Xpos < 66 +1) and (28 -1 < Ypos < 28 +1): 
                return 'wait'
            else :
                if time >= (self.times[-1] + random.triangular(0.5 , 1 , 0.75)):
                    return 'go'
        if (self.activity == 2) :
            if time >= (self.times[-1] + random.triangular(0.5 , 1 , 0.75)):
                return 'go'
            else :
                return 'wait'
              
    def step(self):
    #     # Initial speed and position
        v0 = self.actualV
        r0 = self.pos
        self.direction = normalize(self.dest - self.pos)
    #     # Calculate the force
        adapt = self.adaptVel()
        
        peopleInter =  self.peopleInteraction()
        wallInter =  self.wallInteraction()
        obsInter =  self.obsInteraction()
        
        sumForce = adapt + peopleInter + wallInter + obsInter
    #     # Calculate acceleration
        accl = sumForce/self.mass
    #     # Computing speed
        self.actualV = v0 + accl*0.5 # consider dt = 0.5
    #     # Calculate displacement
        self.pos = r0 + v0*0.5 + accl*0.25
        print(accl,self.actualV,self.pos)

        
        
    def adaptVel(self):
        
        deltaV = self.desiredV - self.actualV
        
        if np.allclose(deltaV, np.zeros(2)):
            deltaV = np.zeros(2)

        return deltaV*self.mass/self.acclTime     

    def peopleInteraction(self, other, Dfactor=1, Afactor=1, Bfactor=1):
        rij = self.radius + other.radius
        dij = np.linalg.norm(self.pos - other.pos)
        nij = (self.pos - other.pos)/dij
        first = np.array([0.0 , 0.0])
        second = np.array([0.0 , 0.0])
        if dij <= self.interactionRange :
            first = Afactor*self.A*np.exp((rij*Dfactor-dij)/(self.B*Bfactor))*nij
            + self.bodyFactor*g(rij-dij)*nij / 10**9
            tij = np.array([-nij[1],nij[0]])
            deltaVij = (self.actualV - other.actualV)*tij
        if dij <= 2.6 :
            tij = np.array([-nij[1],nij[0]])
            deltaVij = (self.actualV - other.actualV)*tij
            second = self.slideFricFactor*g(rij-dij)*deltaVij*tij / 10**9

        return first - second

    def wallInteraction(self, wall):
        ri = self.radius
        diw,niw = distanceP2W(self.pos,wall)
        first = np.array([0.0 , 0.0])
        second = np.array([0.0 , 0.0])
        if diw <= self.interactionRange :
            first = -self.A*np.exp((ri-diw)/self.B)*niw
            + self.bodyFactor*g(ri-diw)*niw / 10**8
            tiw = np.array([round(-niw[1] ,1) , round(niw[0] ,1)])
        if diw <= 2.6 :   
            tiw = np.array([round(-niw[1] ,1) , round(niw[0] ,1)])
            second = self.slideFricFactor*g(ri-diw)*(self.actualV*tiw)*tiw / 10**9

        return first - second
    
    def obsInteraction(self, obs):
        ri = self.radiusO
        dio,nio = distanceP2O(self.pos,obs)
        first = np.array([0.0 , 0.0])
        second = np.array([0.0 , 0.0])
        if dio <= self.interactionRange :
            first = -self.A*np.exp((ri-dio)/self.B)*nio
            + self.bodyFactor*g(ri-dio)*nio/10**9
        return first 
    

    def Mass(self):
        if self.haul.__len__() == 1 :
            
            if self.haul[0] == 'water' :
                self.mass = 80 + 4 + 1.5 # worker weight + material weight + container weight
            if self.haul[0] == 'sand' :
                self.mass = 80 + 62 + 15 # worker weight + material weight + wheelbarrow weight
            if self.haul[0] == 'cement' :
                self.mass = 80 + 25 # worker weight + material bag weight
            if self.haul[0] == 'brick' :
                self.mass = 80 + 60 + 15 # worker weight + 25 brick weight + wheelbarrow weight
            
        if self.haul.__len__() == 0 :
            self.mass = 80

    def distance2wall(self, wall) :
        d2w = distanceP2W(self.pos,wall)
        
        return d2w[0]
    
    def InterRange(self) :
        ActualV = np.sqrt((self.actualV[0])**2 + (self.actualV[1])**2)
        self.interactionRange = (20.8/0.55)*(ActualV) + 5.2
        # more moving speed means bigger interaction radius
        return self.interactionRange
############################################################################
############################################################################
    
class Agent2(object):
    def __init__(self, x=1, y=1):
        # random initialize a agent
        
        self.posX = random.uniform(29,31)
        self.posY = random.uniform(22,24)
        self.pos = np.array([self.posX , self.posY])
        #self.pos = np.array([0.0, 0.0])

        self.actualVX = 0 #random.uniform(0,1.6)
        self.actualVY = 0 #random.uniform(0,1.6)
        self.actualV = np.array([self.actualVX , self.actualVY])
        #self.actualV = np.array([0.0, 0.0])
        
        self.destX = 77
        self.destY = 13
        self.dest = np.array([self.destX,self.destY])
        self.direction = normalize(self.dest - self.pos)
        #self.direction = np.array([0.0, 0.0])
        
        self.desiredSpeed = 0.575   # human walking speed in this workshop is about 0.7 m/s
        self.desiredV = self.desiredSpeed*self.direction
        # rest time
        self.acclTime = random.uniform(4,6) # 5.0
        self.drivenAcc = (self.desiredV - self.actualV)/self.acclTime
               
        self.mass = 80
        self.radius = 2.6 # equal to 0.5 m 
        self.radiusO = 2.6
        self.interactionRange = 5.2 # equal to 1 meter
        self.p = 2.6
        
        self.bodyFactor = 120000
        self.slideFricFactor = 240000
        self.A = random.uniform(0.6,1.2)
        self.B = random.uniform(0.6,1.2) #0.8 #0.08
        
        self.Goal = 2
        self.timeOut = 0.0
        
        self.haul = []
        self.T2 = 0
        #self.T3 = 0
        self.activity = 1
        self.S = 0
        self.h = 1
        self.dT2 = 0
        #self.dT3 = 0
        self.D2 = 0
        
        print('X and Y Position:', self.pos)
        print('self.direction:', self.direction)
        
        self.times = deque([0])
        self.delay = 0
   
        self.TaskPosX = 70
        self.TaskPosY = 30
        self.TaskPos = [self.TaskPosX,self.TaskPosY]
        self.path = []
        self.crossline = []
        self.k = 1 
        self.walls = []
        self.Obstackles = []
        self.sumForce = np.array([0,0])
############################################################################################
############################################################################################

    def PathFinding(self, pos_x,pos_y , taskpos_x,taskpos_y , CrossWall ,obs) :
        self.pos[0] = pos_x
        self.pos[1] = pos_y
        self.TaskPos[0] = taskpos_x
        self.TaskPos[1] = taskpos_y
        self.walls = CrossWall
        self.Obstackles = obs
        from ShortestPath import ShortestPath
        
        return ShortestPath(round(self.pos[0]) ,round(self.pos[1]) , round(self.TaskPos[0]) ,round(self.TaskPos[1]) , self.walls ,self.Obstackles)


    def CrossLine (self , w , v) :
        
        x = sp.Symbol("x")
        y = sp.Symbol("y")
        
        if v[0] == self.pos[0] :
            EQ = sp.solve([x - self.pos[0] , y - (((w[3] - w[1]) / (w[2] - w[0])) * (x - w[0])) - w[1]])
        if v[1] == self.pos[1] :
            EQ = sp.solve([y - v[1] , y - (((w[3] - w[1]) / (w[2] - w[0])) * (x - w[0])) - w[1]])
        if w[2] == w[0] :
            EQ = sp.solve([y - (((v[1]-self.pos[1])/(v[0]-self.pos[0])) * (x-v[0])) - v[1] , x - w[0]])
        else :
            EQ = sp.solve([y - (((v[1]-self.pos[1])/(v[0]-self.pos[0])) * (x-v[0])) - v[1] , y - (((w[3] - w[1]) / (w[2] - w[0])) * (x - w[0])) - w[1]])
        X = EQ[x]
        Y = EQ[y]
        print(X , Y)
        Xindex = [w[0] , w[2] , v[0] , self.pos[0]]
        Xindex.sort()
        Yindex = [w[1] , w[3] , v[1] , self.pos[1]]
        Yindex.sort()
        if (Xindex[1]-0.1 <= X <= Xindex[2]+0.1) and (Yindex[1]-0.1 <= Y <= Yindex[2]+0.1) :
            return 'yes'
        else :
            return 'no'
    
    def command (self,TaskposX , TaskposY , t) :
        Xpos = self.pos[0]
        Ypos = self.pos[1]
        self.TaskPos[0] = TaskposX
        self.TaskPos[1] = TaskposY
        time = t
        if (self.activity == 1) :
            if (72 -1 < Xpos < 72 +1) and (45 -1 < Ypos < 45 +1): 
                return 'wait'
            else :
                if time >= (self.times[-1] + random.triangular(0.5 , 1 , 0.75)):
                    return 'go'
        if (self.activity == 2) :
            if time >= (self.times[-1] + random.triangular(0.5 , 1 , 0.75)):
                return 'go'
            else :
                return 'wait'
        
    
    def step(self):
    #     # Initial speed and position
        v0 = self.actualV
        r0 = self.pos
        self.direction = normalize(self.dest - self.pos)
    #     # Calculate the force
        adapt = self.adaptVel()
        
        peopleInter =  self.peopleInteraction()
        wallInter =  self.wallInteraction()
        obsInter =  self.obsInteraction()
        
        sumForce = adapt + peopleInter + wallInter + obsInter
    #     # Calculate acceleration
        accl = sumForce/self.mass
    #     # Computing speed
        self.actualV = v0 + accl*0.5 # consider dt = 0.5
    #     # Calculate displacement
        self.pos = r0 + v0*0.5 + accl*0.25
        print(accl,self.actualV,self.pos)

        
        
    def adaptVel(self):
        
        deltaV = self.desiredV - self.actualV
        
        if np.allclose(deltaV, np.zeros(2)):
            deltaV = np.zeros(2)

        return deltaV*self.mass/self.acclTime

    def peopleInteraction(self, other, Dfactor=1, Afactor=1, Bfactor=1):
        rij = self.radius + other.radius
        dij = np.linalg.norm(self.pos - other.pos)
        nij = (self.pos - other.pos)/dij
        first = np.array([0.0 , 0.0])
        second = np.array([0.0 , 0.0])
        if dij <= self.interactionRange :
            first = Afactor*self.A*np.exp((rij*Dfactor-dij)/(self.B*Bfactor))*nij
            + self.bodyFactor*g(rij-dij)*nij /10**9
            tij = np.array([-nij[1],nij[0]])
            deltaVij = (self.actualV - other.actualV)*tij
        if dij <= 2.6 :
            tij = np.array([-nij[1],nij[0]])
            deltaVij = (self.actualV - other.actualV)*tij
            second = self.slideFricFactor*g(rij-dij)*deltaVij*tij / 10**9

        return first - second

    def wallInteraction(self, wall):
        ri = self.radius
        diw,niw = distanceP2W(self.pos,wall)
        first = np.array([0.0 , 0.0])
        second = np.array([0.0 , 0.0])
        if diw <= self.interactionRange :
            first = -self.A*np.exp((ri-diw)/self.B)*niw
            + self.bodyFactor*g(ri-diw)*niw / 10**8
            tiw = np.array([round(-niw[1] ,1) , round(niw[0] ,1)])
        if diw <= 2.6 :   
            tiw = np.array([round(-niw[1] ,1) , round(niw[0] ,1)])
            second = self.slideFricFactor*g(ri-diw)*(self.actualV*tiw)*tiw / 10**9

        return first - second
    
    def obsInteraction(self, obs):
        ri = self.radiusO
        dio,nio = distanceP2O(self.pos,obs)
        first = np.array([0.0 , 0.0])
        second = np.array([0.0 , 0.0])
        if dio <= self.interactionRange :
            first = -self.A*np.exp((ri-dio)/self.B)*nio
            + self.bodyFactor*g(ri-dio)*nio/10**9
        return first 

    def Mass(self) :
        if self.haul.__len__() == 1 :
            
            if self.haul[0] == 'water' :
                self.mass = 80 + 4 + 1.5 # worker weight + material weight + container weight
            if self.haul[0] == 'sand' :
                self.mass = 80 + 62 + 15 # worker weight + material weight + wheelbarrow weight
            if self.haul[0] == 'cement' :
                self.mass = 80 + 25 # worker weight + material bag weight
            if self.haul[0] == 'brick' :
                self.mass = 80 + 60 + 15 # worker weight + 25 brick weight + wheelbarrow weight
            
        if self.haul.__len__() == 0 :
            self.mass = 80

    def distance2wall(self, wall) :
        d2w = distanceP2W(self.pos,wall)
        
        return d2w[0]
    
    def InterRange(self) :
        ActualV = np.sqrt((self.actualV[0])**2 + (self.actualV[1])**2)
        self.interactionRange = (20.8/0.55)*(ActualV) + 5.2
        # more moving speed means bigger interaction radius
        return self.interactionRange