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
        self.alltime = 0
        self.currenttime = 0
    
    def frameact(self):
        if self.entity.currentF < self.entity.allF:
            self.entity.frame_set(self.entity.currentF)
#            self.entity._dirc(self.entity.goleft)
        else:
            self.entity.currentF = 0
            self.entity.frame_set(self.entity.currentF)
#            self.entity._dirc(self.entity.goleft)
        self.entity._dirc(self.entity.goleft)
    
    def move(self):
        if self.entity.goleft == False:
#             if self.movetime < self.alltime:
#                 self.entity._valx += 0.1
#                 self.movetime += 1
#                 self.entity.currentF += 1
            self.entity._valx += 0.1
            self.entity.currentF += 1
                
        else:
#         if randint(1,100) % 33 == 0:
#             if self.movetime < self.alltime:
#                 self.entity._valx -= 0.1
#                 self.movetime += 1
#                 self.entity.currentF += 1
            self.entity._valx -= 0.1
            self.entity.currentF += 1
        self.movetime += 1
#        self.currenttime = self.movetime
        
    
    def shoot(self):
        if randint(1,100) % 23 == 0:
            self.entity.bulletpool.add(self.entity.bullet)
#        self.entity._valx = 0
#        self.entity.frame_set(0)
        
#        self.movetime = 0
        
            
    def action(self):
        self.move()
        self.frameact()
#        self.currenttime = self.movetime
        
    def checktochange(self):
        
        if self.movetime > self.alltime:
            return "turn"
        
#        if self.entity.shootrect != None:
        if self.entity.shootrect.colliderect(self.entity.target.rect):
            self.entity.currentF = -1
            return "shoot"
#            self.movetime = self.currenttime
#            self.shoot()
#                self.entity.frame_set(0)
#                print "finded and shoot"
#                return "shoot"

        
    def enteraction(self):
#        self.entity.goleft = randint(1,100) % 2
        
#         self.alltime = randint(10,50)
        self.alltime = 50
        
        
    
    def exitaction(self):
#        if self.movetime == self.alltime:
        self.movetime = 0
        self.entity._valx = 0

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
        self.pre = self.entity.goleft
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
#        self.entity.frame_set(0)
    
    def action(self):
#        self.entity.frame_set(0)
        if randint(1,100) % 23 == 0:
            
            self.shoot()
        
    def checktochange(self):
        if self.entity.bulletpool.sprites() != []:
            return "moveandseek"
        
    def enteraction(self):
        pass
#        if self.entity.bulletpool.sprites() == []:
#            self.entity.frame_set(0)
#             self.entity.frame_set(0)
            #self.entity.set_stop()
        
    def exitaction(self):
        pass
#        self.entity.frame_set(0)
        
        