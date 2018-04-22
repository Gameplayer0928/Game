# coding=utf-8
#!/usr/bin/python
'''
Created on 2018��2��17��
 @author: Gameplayer0928 Qi Gao
#
#    This file is part of Black Face - the shadow of Big Head.
#
#    Black Face - the shadow of Big Head is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Black Face - the shadow of Big Head is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Black Face - the shadow of Big Head.  If not, see <http://www.gnu.org/licenses/>.
#
#    Copyright 2018, 2019, 2020 Qi Gao
#

'''
# import pygame
from random import randint

class state():
    def __init__(self,statename):
        self.statename = statename
    
    def action(self):
        pass
    
    def checktochange(self):
        pass
    
    def enteraction(self):
        pass
    
    def exitaction(self):
        pass

class StateMachine():
    def __init__(self):
        self.statepool = {}
        self.activestate = None
    
    def addstate(self,state):
        self.statepool[state.statename] = state
    
    def setstate(self,newstatename):
        if self.activestate is not None:
            self.activestate.exitaction()
        self.activestate = self.statepool[newstatename]
        self.activestate.enteraction()
    
    def think(self):
        
        if self.activestate is None:
            return
        self.activestate.action()
#        print self.activestate.statename
        newstatename = self.activestate.checktochange()
        if newstatename is not None:
            self.setstate(newstatename)
            
class moveandseekstate(state):
    def __init__(self,entity):
        state.__init__(self, "moveandseek")
        self.entity = entity
        self.movetime = 0
        self.alltime = 50
        self.currenttime = 0
#         self.deteblock = False
#     def framestop(self):
#         self.entity.currentF = 0
    

    def move(self):
        if self.entity.goleft == False:
            self.entity._valx += 2
                
        else:
            self.entity._valx -= 2
        
        self.movetime += 1       
            
    def action(self):
        self.entity.frame_act()
        self.move()
    

       
    def checktochange(self):
        if self.entity.check_to_shoot():
            return "shoot"
        
        if self.movetime > self.alltime:
            return "turn"
        

#             if self.detection() != 0:
#                 return "shoot"
#            
#             self.entity.currentF = -1
            
      
    def enteraction(self):
        pass
    
    def exitaction(self):
        self.movetime = 0
        self.entity._valx = 0

class followstate(state):
    def __init__(self,entity):
        state.__init__(self, "follow")
        self.entity = entity
        self.movetime = 0
        self.alltime = 100
        self.currenttime = 0
        self.xr = 0
        self.yr = 0
        self.needjump = False
#        print "follow"
    
    
    def move(self):
        
        if self.entity.goleft == False:
            self.entity._valx += 2             
        else:
            self.entity._valx -= 2

        if self.movetime > self.xr and self.needjump and self.entity.check_to_jump() and self.entity.jumping == False:
            self.entity.jump()
            self.needjump = False
        self.entity.currentF += 1
        self.movetime += 1
        
#        self.entity._valx = 0
#        self.currenttime = self.movetime

    def calculate(self):
        self.entity.memory["toloc"] = [self.entity.target.rect.x,self.entity.target.rect.y]
        self.xr = abs(self.entity.rect.x - self.entity.memory["toloc"][0])
        self.yr = abs(self.entity.memory["toloc"][1] - self.entity.rect.y)
        if self.yr > self.entity.rect.height:
            self.needjump = True        
        
    def action(self):
        self.calculate()
        self.move()
        self.entity.frame_act()
#         if self.xr > 100 or self.yr > 100:
#             self.entity.memory["toloc"] = []
   
    def checktochange(self):
        if self.alltime < self.movetime:
            return "moveandseek"
        
    def enteraction(self):
        self.calculate()
    
    def exitaction(self):
        self.movetime = 0
        self.entity.jumping = False
        pass

class turnstate(state):
    def __init__(self,entity):
        state.__init__(self, "turn")
        self.entity = entity
        self.pre = None

    def action(self):
        self.entity.goleft = not(self.entity.goleft)
#        self.entity._dirc(self.entity.goleft)
    
    def checktochange(self):
        if self.entity.goleft != self.pre:
            return "moveandseek"
        
    def enteraction(self):
#         self.entity.jump()
        self.pre = self.entity.goleft
        self.entity.detective_set()
#        self.entity.frame_set(0)
        
    def exitaction(self):
        self.pre = None
       
class shootstate(state):
    def __init__(self,entity):
        state.__init__(self, "shoot")
        self.entity = entity
#        print "shoot init"

    def shoot(self):
        self.entity.bulletpool.add(self.entity.bullet)
#         self.entity.frame_set(0)
    
    def action(self):
#        self.entity.currentF -= 1
        self.entity.frame_stop()
        if randint(1,100) % 20 == 0:   
            self.shoot()
        
    def checktochange(self):
        if self.entity.check_to_shoot() == False:
            return "follow"
        
    def enteraction(self):
        self.entity.memory["toloc"] = [self.entity.target.rect.x,self.entity.target.rect.y]
        self.entity.frame_stop()
        pass
#        if self.entity.bulletpool.sprites() == []:
#            self.entity.frame_set(0)
#             self.entity.frame_set(0)
            #self.entity.set_stop()
        
    def exitaction(self):
        pass
#        self.entity.frame_set(0)
        
        