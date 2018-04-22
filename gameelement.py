# coding=utf-8
#!/usr/bin/python
'''
Created on 2018��2��10��
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

from gameconfig import *
from random import randint
import math
import AI

# from netmachine import get_remes

class Block(pygame.sprite.Sprite):
    def __init__(self,image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()

class Item(pygame.sprite.Sprite):
    def __init__(self,name = "None",image = "None"):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = image
        self.rect = self.image.get_rect()
        self.mapblock = None
        self.effect = {}
        self._valy = 0.0
        self.uptime = 0
        
    def update(self):
        
#         if self.uptime < 10:
#             self._valy -= 0.1
#             self.uptime += 1
#         else:
#             self._valy += 0.2    
        self._valy += 0.2
        self.rect.move_ip((0,self._valy))
        
        for block in self.mapblock:
            top,bottom,left,right = collide_edge(self.rect, block.rect)
            if top:
                self._valy = 0 
                self.rect.top = block.rect.bottom
            if bottom:
                self._valy = 0
                self.rect.bottom = block.rect.top
            if left:
                self._valx = 0 
                self.rect.left = block.rect.right
            if right:
                self._valx = 0
                self.rect.right = block.rect.left
                
class Medicine(Item):
    def __init__(self,name = "medicine",image = MEDIMAGE):
        Item.__init__(self, name, image)
        self.effect = {"life+":50}

class Ammo(Item):
    def __init__(self,name = "ammo",image = AMIMAGE):
        Item.__init__(self, name, image)
        self.effect = {"ammo+":10}
        

class GameEntity(pygame.sprite.Sprite):
    def __init__(self,image,frameW,frameH,allF,bulletimage):
        pygame.sprite.Sprite.__init__(self)
        self.main_image = image
        self.frameW = frameW
        self.frameH = frameH
        self.allF = allF
        self.currentF = 0
        
        self.status = {"life":100,"ammo":10}
        
        self.image = self.main_image.subsurface(pygame.Rect(0,0,self.frameW,self.frameH))
        self.rect = pygame.Rect(0,0,self.frameW,self.frameH)
        
        self.goleft = False
        self.jumping = True
        self.onfloor = False
        self._valx = 0
        self._valy = 0
        
        self.mapblock = None
        
        self.bulletimage = bulletimage
        self.bulletpool = pygame.sprite.Group()
        
        self.collidestatepool = {self.rect.top:0,self.rect.bottom:0,self.rect.left:0,self.rect.right:0}
        self.collideblockpool = []
        
        self.shootdelay = 0
        self.shootlock = False
        
        self.meleedelay = 0
        self.meleelock = False
        
        self.NETCOMMEND = None
        
    def set_default_loc(self,fx,fy,goleft = False,pix=1):
        self.rect.x = fx
        self.rect.y = fy * pix
        self.goleft = goleft
        
    def frame_set(self,s = 0):
        currentRect = pygame.Rect(self.frameW * s,0,self.frameW,self.frameH)
        self.image = pygame.transform.flip(self.main_image.subsurface(currentRect),self.goleft,0)
    
    def _dirc(self,s):
        self.image = pygame.transform.flip(self.image,s,0)
    
    def set_stop(self):
        self._valx = 0
        self._valy = 0
    
    def update(self):
        keys = pygame.key.get_pressed()
#         ncresult = None
        global USENET
        if USENET:

            ncresult = self.NETCOMMEND
            
            if ncresult == N_LEFT:
                self._valx -= 1
                self.goleft = True
                if self.rect.x < 0:
                    self._valx = 0
                
            if ncresult == N_RIGHT:
                self._valx += 1
                self.goleft = False
                if self.rect.x > SCREEN_SIZE[0] - self.rect.width:
                    self._valx = 0
            self._valx *= 0.8
            
            if ncresult == N_JUMP and self.onfloor == True:
                self._valy -= 11
                self.onfloor = False
            
            self._valy += 0.5
            
            self.rect.move_ip((self._valx,self._valy))
                  
            if ncresult == N_SHOOT and self.status["ammo"] > 0  :
                self.shootdelay += 1
                if self.shootdelay < 20:
                    if self.shootlock == False:
                        self.shootlock = True
                        bt = Bullet(self.rect.x,self.rect.y,self.goleft,self.bulletimage,25,8)
                        self.bulletpool.add(bt)
                        self.status["ammo"] -= 1
                else:
                    self.shootlock = False
                    self.shootdelay = 0
            else:
                self.shootdelay = 0
                self.shootlock = False
            
    
            
            if ncresult == N_MELEE:
                self.meleedelay += 1
                if self.meleedelay < 20:
                    if self.meleelock == False:
                        self.meleelock = True
                        self.frame_set(3)
                        hw = HITWAVEIMAGE(self.rect.x,self.rect.y,self.rect.width,self.goleft)
                        self.bulletpool.add(hw)
                else:
                    self.meleelock = False
                    self.meleedelay = 0
            else:
                self.meleelock = False
                self.meleedelay = 0
            
            if ncresult == N_LEFT or ncresult == N_RIGHT:
                
                if self.currentF < self.allF - 1:
                    self.frame_set(self.currentF)
                else:
                    self.currentF = 0
                    self.frame_set(self.currentF)
                self.currentF += 1
                
            self.NETCOMMEND = None
            ncresult = None
#             else:
#                 pass
     ###################################################################################
     ############                      up use net, down dont use net     ###############
     ###################################################################################   
        else:
            if keys[pygame.K_a]:
                self._valx -= 1
                self.goleft = True
                if self.rect.x < 0:
                    self._valx = 0
                
            if keys[pygame.K_d]:
                self._valx += 1
                self.goleft = False
                if self.rect.x > SCREEN_SIZE[0] - self.rect.width:
                    self._valx = 0
            self._valx *= 0.8
            
            if keys[pygame.K_SPACE] and self.onfloor == True:
                self._valy -= 11
                self.onfloor = False
            
            self._valy += 0.5
            
            self.rect.move_ip((self._valx,self._valy))
                  
            if keys[pygame.K_k] and self.status["ammo"] > 0  :
                self.shootdelay += 1
                if self.shootdelay < 20:
                    if self.shootlock == False:
                        self.shootlock = True
                        bt = Bullet(self.rect.x,self.rect.y,self.goleft,self.bulletimage,25,8)
                        self.bulletpool.add(bt)
                        self.status["ammo"] -= 1
                else:
                    self.shootlock = False
                    self.shootdelay = 0
            else:
                self.shootdelay = 0
                self.shootlock = False
            
    
            
            if keys[pygame.K_l]:
                self.meleedelay += 1
                if self.meleedelay < 20:
                    if self.meleelock == False:
                        self.meleelock = True
                        self.frame_set(3)
                        hw = HITWAVEIMAGE(self.rect.x,self.rect.y,self.rect.width,self.goleft)
                        self.bulletpool.add(hw)
                else:
                    self.meleelock = False
                    self.meleedelay = 0
            else:
                self.meleelock = False
                self.meleedelay = 0
            
            if keys[pygame.K_d] or keys[pygame.K_a]:
                
                if self.currentF < self.allF - 1:
                    self.frame_set(self.currentF)
                else:
                    self.currentF = 0
                    self.frame_set(self.currentF)
                self.currentF += 1

        for block in self.mapblock:
            if block.rect.colliderect(self.rect):
                    
                    top,bottom,left,right = collide_edge(self.rect,block.rect)
                    if top:
                        self._valy = 0
                        self.rect.top = block.rect.bottom
                    elif bottom:
                        self._valy = 0
                        self.rect.bottom = block.rect.top
                        self.onfloor = True
                    elif right:
                        self._valx = 0
                        self.rect.right = block.rect.left
                    elif left:
                        self._valx = 0
                        self.rect.left = block.rect.right
                    else:
                        pass
#                         #      print "============OPPS============="  
                    
#         if self.rect.x < 0 or self.rect.x > SCREEN_SIZE[0] or self.rect.y < 0 or self.rect.y > SCREEN_SIZE[1]:
        if self.status["life"] < 0:
            self.kill()

class LineRectCount(): #pygame.sprite.Sprite
    def __init__(self,who,shift = [0,0],MAX = 100.0,backc = (255,0,0),countc = (0,255,0),rectH = 5,sub = True):
#        pygame.sprite.Sprite.__init__(self)
        self.who = who
        self.MAX = MAX
        self.shift = shift
        self.rectH = rectH
        self.backc = backc
        self.countc = countc
        self.sub = sub
        self.width,self.height = self.who.rect.width,self.who.rect.height
        self.onelife = self.width / self.MAX
        if self.sub:
            self.alllife = self.width
        else:            
            self.alllife = 0
            
            
    def counting(self):
        if self.sub:
            if self.alllife > 0.0:
                self.alllife -= self.onelife
        else:
            if self.alllife < self.MAX:
                self.alllife += self.onelife
    
    def dead(self):
        if self.sub:
            if self.alllife < 0.1:
#                #      print "sub true dead"
                return True
#            else:
#                return False
        else:
            if self.alllife > self.MAX:
#                #      print "sub false dead"
                return True
#            else:
#                return False
 
    def rander(self,sur):

        sur.fill(self.backc,(self.who.rect.x + self.shift[0],self.who.rect.y + self.shift[1],self.who.rect.width,self.rectH))
        sur.fill(self.countc,(self.who.rect.x + self.shift[0],self.who.rect.y + self.shift[1], self.alllife, self.rectH))
 
class BossEntity(GameEntity):
    def __init__(self,image,frameW,frameH,allF,bulletimage):
        GameEntity.__init__(self,image,frameW,frameH,allF,bulletimage)
#        pygame.sprite.Sprite.__init__(self)
        self.frametimebuff = 0
        self._valy = 2
        self.lrc = LineRectCount(self,[0,-10])
    
    def shoot(self):
        bt = Bullet2(self.rect.x,self.rect.y,1,self.bulletimage,150,150)
        if self.bulletpool.sprites() == []:
         #   #      #      print "bullet in"
            self.bulletpool.add(bt)
            self.frame_set(1)
    
    def update(self):
        
        if randint(1,100)%19 == 0:
            self.shoot()
        #    #      print "shooting"
        self.frametimebuff += 1
        if self.rect.y > 400:
            self._valy -= 2
        if self.rect.y < 50:
            self._valy += 2
        if self.frametimebuff > 50:
            self.frame_set(0)
            self.frametimebuff = 0
        self.rect.move_ip((self._valx,self._valy))
        
        if self.lrc.dead():
            self.kill()
#        #      print self.rect.x,self.rect.y

class EnemyEntity(GameEntity):
    def __init__(self,image,frameW,frameH,allF,bulletimage):
        GameEntity.__init__(self,image,frameW,frameH,allF,bulletimage)
        self.brain = AI.StateMachine()
        SHOOTSTATE = AI.shootstate(self)
        MOVEANDSEEK = AI.moveandseekstate(self)
        TURN = AI.turnstate(self)
        FOLLOW = AI.followstate(self)
        
        self.lrc = LineRectCount(self,MAX = 3.0,shift = [0,-10])
        
        self.brain.addstate(SHOOTSTATE)
        self.brain.addstate(MOVEANDSEEK)
        self.brain.addstate(TURN)
        
        self.brain.addstate(FOLLOW)
        
        self.bullet = Bullet(self.rect.x,self.rect.y,self.goleft,self.bulletimage,32,22)
        
        self.memory = {"toloc":[]}
        self.shootrect = None
        self.uprect = None
        
        self.target = None
        
        self.giveitempool = None
        self.detective_set()
        self.brain.setstate("moveandseek")
        
        self.jumping = False
        
    def detective_set(self):
        if self.target != None:
            if self.goleft == False:
                self.shootrect = pygame.Rect(self.rect.x,self.rect.y,SCREEN_SIZE[0]/2+self.rect.x,10)
            else:
                self.shootrect = pygame.Rect(self.rect.x-SCREEN_SIZE[0]/2,self.rect.y,SCREEN_SIZE[0]/2,10)
            self.uprect = pygame.Rect(self.rect.x,self.rect.y - 15,self.rect.width,self.rect.y+15)
    
#     def set_dead_pos(self):
#         self.deadpos=[self.rect.x,self.rect.y]
    def give_item(self):
        if randint(1,100) % 15 == 0:
            item = Medicine()
            
        else:
            item = Ammo()
        item.rect.x = self.rect.x
        item.rect.y = self.rect.y
        item.mapblock = self.mapblock
        self.giveitempool.add(item)
    
    def frame_act(self):
        if self.currentF < self.allF:
            self.frame_set(self.currentF)
        else:
            self.currentF = 0
            self.frame_set(self.currentF)
        self.currentF += 1
    
    def frame_stop(self):
        self.currentF = 0
    
    def detection_block(self,detef,axis = 'x'):
        pe = []
        for i in self.mapblock:
            if detef.colliderect(i.rect):
#                print "block:",i.rect
                if axis == 'x':
                    pe.append(abs(self.rect.x - i.rect.x))
                if axis == 'y':
                    pe.append(abs(self.rect.y - i.rect.y))
#        print len(pe)
        if pe != []:
            pe.sort()
            return pe[0]
        else:
            return 0
    
#     def detection_up_block(self):
#         pe = []
#         for i in self.mapblock:
#             if self.shootrect.colliderect(i.rect):
# #                print "block:",i.rect
#                 pe.append(abs(self.rect.x - i.rect.x))
# #        print len(pe)
#         if pe != []:
#             pe.sort()
#             return pe[0]
#         else:
#             return 0
    
    def detection(self,detef,axis = 'x'):
        if detef.colliderect(self.target.rect):
            if axis == 'x':
                return abs(self.rect.x - self.target.rect.x)
            if axis == 'y':
                return abs(self.rect.y - self.target.rect.y)
        else:
            return 0
    
    def check_to_jump(self):    
        re = self.detection_block(self.uprect, 'y')
        if re < 15:
            return False
        else:
            return True
        
    def check_to_shoot(self):
        db = self.detection_block(self.shootrect,'x')
        dt = self.detection(self.shootrect,'x')
        if db:
            if db > dt and dt != 0:
                return 1
        else:
            if dt:
                return 1
        return 0
    
    
    def jump(self):
        self._valy -= 12
        self.jumping = True
    
    def update(self):
        self.detective_set()
        self.brain.think()
        self._valy += 0.5
        self.rect.move_ip((self._valx,self._valy))
        self._valx = 0
        
        for block in self.mapblock:
#             blockedgestorge={"top":0,"bottom":0,"left":0,"right":0}
            if block.rect.colliderect(self.rect):
                top,bottom,left,right = collide_edge(self.rect,block.rect)
#                     #      print (top,bottom,left,right)
                if top:
                    self._valy = 0
                    self.rect.top = block.rect.bottom
#                         #      print "top"
                elif bottom:
                    self._valy = 0
                    self.rect.bottom = block.rect.top
#                     self.onfloor = True
#                         #      print "bottom"
                elif right:
                    self._valx = 0
                    self.rect.right = block.rect.left
#                         #      print "right"
                elif left:
                    self._valx = 0
                    self.rect.left = block.rect.right
#                         #      print "left"
                else:
                    pass
        self.bullet = Bullet(self.rect.x,self.rect.y,self.goleft,self.bulletimage,32,22)
        self.bullet.speed = 4
        pygame.sprite.groupcollide(self.bulletpool, self.mapblock, 1, 0)
        
#        #      print self.lrc.dead()
        if self.lrc.dead():
            self.give_item()
            self.kill()
                  
class Bullet(pygame.sprite.Sprite):
    def __init__(self,xp,yp,shootD,image,shiftW,shiftH):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.shootD = shootD
        self.speed = 6.0
        self._valx = 0
        self._valy = 0
        
        if self.shootD == 0:
            self.shiftW = shiftW
            self.rect.x = xp + self.shiftW
        else:
            self.rect.x = xp
            
        self.shiftH = shiftH

        self.rect.y = yp + shiftH
        
    def update(self):
        if self.shootD == 0:
            self._valx += self.speed
        if self.shootD == 1:
            self._valx -= self.speed
        
        self.rect.move_ip((self._valx ,self._valy))
        self._valx = 0
        
        if self.rect.x < 0 or self.rect.x > SCREEN_SIZE[0] or self.rect.y < 0 or self.rect.y > SCREEN_SIZE[1]:
            self.kill()

class HITWAVEIMAGE(pygame.sprite.Sprite):
    def __init__(self,xp,yp,width,shootD,image = HITWAVEIMAGE,frameW = 20,frameH = 50,allF = 3):
        pygame.sprite.Sprite.__init__(self)
        self.main_image = image
        
        self.frameW = frameW
        self.frameH = frameH
        
        self.image = self.main_image.subsurface(pygame.Rect(0,0,self.frameW,self.frameH))
        self.rect = pygame.Rect(0,0,self.frameW,self.frameH)
        self.shootD = shootD
        self.currentF = 0
        self.allF = allF
        
        self.xp = xp         #from user rect x
        self.yp = yp
        self.width = width   #from user rect width

#         self._dirc(self.shootD)
        if self.shootD == True:
            self.rect.x = self.xp - self.frameW
            
        if self.shootD == False:
            self.rect.x = self.xp + self.width

        self.rect.y = self.yp
#         print "HITWAVEIMAGE : ",self.shootD
    
    def frame_set(self,s = 0):
        currentRect = pygame.Rect(self.frameW * s,0,self.frameW,self.frameH)
        self.image = pygame.transform.flip(self.main_image.subsurface(currentRect),self.shootD,0)
        
 
        
    def update(self):
#        self._dirc(self.shootD)
        if self.allF > self.currentF:
#            self._dirc(self.shootD)            
            self.frame_set(self.currentF)
            self.currentF += 1
        else:
#             self.currentF = 0
            self.kill()
                
class Bullet2(Bullet):
    def __init__(self,xp,yp,shootD,image,shiftW,shiftH):
        Bullet.__init__(self, xp, yp, shootD, image, shiftW, shiftH)
        
        self.speed = 5.0
        self.count = 0
        self.rcount = 0
        
    def update(self):
        if self.shootD == 0:
            self._valx += self.speed
        if self.shootD == 1:
            self._valx -= self.speed
        
        if self.rcount > 5:
            self._valy += math.radians(self.count)*math.sin(self.count)*50
            self.count+=1
            self.rcount = 0
        self.rcount += 1
        
        self.rect.move_ip((self._valx ,self._valy))
        self._valx = 0
        
        if self.rect.x < 0 or self.rect.x > SCREEN_SIZE[0] or self.rect.y < 0 or self.rect.y > SCREEN_SIZE[1]:
            self.kill()

class StateBoard():
    def __init__(self,GE,todraw):
        self.todraw = todraw
        self.GE = GE
        self.xp = self.GE.rect.x - 90
        self.yp = self.GE.rect.y - 40
        self.back = pygame.rect.Rect(self.xp,self.yp,80,80)
        self.text1 = pygame.font.SysFont("arial",15)
        self.text1sur = self.text1.render("status :",1,(0,0,0))
        
        self.text2 = pygame.font.SysFont("arial",15)
        self.text2sur = self.text1.render("life:"+str(self.GE.status["life"]),1,(0,0,0))
        
        self.text3 = pygame.font.SysFont("arial",15)
        self.text3sur = self.text1.render("ammo:"+str(self.GE.status["ammo"]),1,(0,0,0))
        
    def show(self):
        if self.GE.status["life"] > 0:
            pygame.draw.rect(self.todraw,(255,255,255),self.back,0)
            self.todraw.blit(self.text1sur,(self.xp,self.yp,80,20))
            self.todraw.blit(self.text2sur,(self.xp+10,self.yp+20,80,20))
            self.todraw.blit(self.text3sur,(self.xp+10,self.yp+40,80,20))

def collide_edge(a,b):
    lt,rt,tp,bm = False,False,False,False
    Rect = pygame.Rect
    
    left = Rect(a.left,a.top+1,1,a.height-2)
    right = Rect(a.right,a.top+1,1,a.height-2)
    top = Rect(a.left+1,a.top,a.width-2,1)
    bottom = Rect(a.left+1,a.bottom,a.width-2,1)

    
    if left.colliderect(b):
        lt = True
    if right.colliderect(b):
        rt = True
    if top.colliderect(b):
        tp = True
    if bottom.colliderect(b):
        bm = True
    return (tp,bm,lt,rt)    