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

from gameelement import *
from gameconfig import *





def readMap(file_name,marklist,mapW):
    x,y = 0,0
    ls = []
    f = open(file_name,'r')
    for i in f:
        y += 1
        for z in i:
            if x > mapW:
                x = 0
            if z in marklist:            
                ls.append([x,y])
            x += 1
    f.close()
    return ls

def buildMap(image,ls,x,y):
    Group = pygame.sprite.Group()   
    lsp = ls
    xl = x
    yl = y
    for i in lsp:
        items = Block(image)    
        items.rect.x = i[0]*xl - xl
        items.rect.y = i[1]*yl - yl
        Group.add(items)
#       items = None
    return Group


def set_location(ls,xp,yp):
    x = ls[0]*xp - xp
    y = ls[1]*yp - yp
    return [x,y]


class ChangeMapPoint(pygame.sprite.Sprite):
    def __init__(self,mapfilename,changesymbol,unitpix):
        self.mapfilename = mapfilename
        self.changesymbol = changesymbol
        self.unitpix = unitpix
        self.inpoint = readMap(self.mapfilename,self.changesymbol,SCREEN_SIZE[0]/self.unitpix)
        self.inmapx = self.inpoint[0][0]*self.unitpix
        self.inmapy = self.inpoint[0][1]*self.unitpix - self.unitpix
        if self.changesymbol == 'l':
            self.rect = pygame.rect.Rect(self.inmapx-30,self.inmapy-100,self.unitpix-10,self.unitpix+100)
        if self.changesymbol == 'r':
            self.rect = pygame.rect.Rect(self.inmapx+30,self.inmapy-100,self.unitpix-10,self.unitpix+100)
            
class MapState():
    def __init__(self,mapfilelist,GE,scr):
        self.screen = scr
        self.mapfilelist = mapfilelist
        #      print len(self.mapfilelist)
        self.mapNumber = 0
        self.mapfile = PATHhead + self.mapfilelist[self.mapNumber] + Utxt +".txt"
        #      print self.mapfile
        self.backeve = BACKEVE
        self.blockimage = BLOCKIMAGE
        self.blockbackimage = BLOCKBACKIMAGE
        self.dustfloorimage = DUSTFLOORIMAGE
        
        
        self.mapls = readMap(self.mapfile, ["f"],SCREEN_SIZE[0]/20)
        self.mapbls = readMap(self.mapfile, ["x","E"],SCREEN_SIZE[0]/20)
        self.mapdfls = readMap(self.mapfile, ["z"],SCREEN_SIZE[0]/20)
        
        
        self.mapLp = ChangeMapPoint(self.mapfile,'l',20)
        self.mapRp = ChangeMapPoint(self.mapfile,'r',20)
        
        self.inpoint = readMap(self.mapfile,"l",SCREEN_SIZE[0]/20)
        
        self.blockgroup = buildMap(self.blockimage, self.mapls, 20, 20)
        self.a = buildMap(self.blockbackimage, self.mapbls, 20, 20)
        self.b = buildMap(self.dustfloorimage, self.mapdfls,20,20)
        
        self.itemgroup = pygame.sprite.Group()
        
        self.blockbackgroup = pygame.sprite.Group()
        self.blockbackgroup.add(self.a.sprites())
        self.blockbackgroup.add(self.b.sprites())    
        
        self.GE = GE
        self.GE.mapblock = self.blockgroup
        self.GEsb = None
        
        self.GEgroup = pygame.sprite.Group()
        self.GEgroup.add(self.GE)
#        if 
        self.GE.set_default_loc(self.inpoint[0][0]+20,self.inpoint[0][1],False,19)
        
        self.mapboss = None
        self.bossbulletimage = BOSSBULLETIMAGE
        
        self.mapenemy = None
        self.enemybulletimage = ENEMYBULLETIMAGE
        self.enemygroup = pygame.sprite.Group()
        
        
        self.enemy_set()
        
    def enemy_set(self):
        
        self.mapboss = readMap(self.mapfile, "b",SCREEN_SIZE[0]/20)
        if self.mapboss != []:
            loc = set_location(self.mapboss[0], 20, 20)            
            bossimage = BOSSIMAGE
            boss = BossEntity(bossimage,200,200,3,self.bossbulletimage)
            boss.set_default_loc(loc[0],loc[1],False)
            self.enemygroup.add(boss)
        else:
            self.mapboss = None
            self.enemygroup.empty()
        
        self.mapenemy = readMap(self.mapfile, ["e","E"],SCREEN_SIZE[0]/20)
        
        if self.mapenemy != []:
            for i in self.mapenemy:
#                #      print i
                loc = set_location(i, 20, 20)            
                enemyimage = ENEMYIMAGE
                enemy = EnemyEntity(enemyimage,36,50,3,self.enemybulletimage)
                enemy.set_default_loc(loc[0],loc[1],False)
                enemy.mapblock = self.blockgroup
                enemy.target = self.GE
                enemy.giveitempool = self.itemgroup
                self.enemygroup.add(enemy)
        else:
            self.mapenemy = None
            self.enemygroup.empty()
    
    def reset_map(self):
        self.enemygroup.empty()
        self.blockgroup.empty()
        self.blockbackgroup.empty()
        self.itemgroup.empty()
        self.GE.bulletpool.empty()
#        del(self.GEsb)
        
    def running(self):
        self.GEsb = StateBoard(self.GE,self.screen)
        
        self.screen.fill((255,255,255),(0,0,SCREEN_SIZE[0],SCREEN_SIZE[1]))
        self.screen.blit(self.backeve,(0,0))
        
        self.blockbackgroup.draw(self.screen)

        self.GEgroup.update()
        
        
        self.GE.bulletpool.update()
        self.enemygroup.update()
                
        for i in self.enemygroup:
            i.bulletpool.update()
            i.bulletpool.draw(self.screen)
            i.lrc.rander(self.screen)
            if pygame.sprite.spritecollide(self.GE,i.bulletpool,1):
                self.GE.status["life"] -= 1
            if pygame.sprite.spritecollide(i, self.GE.bulletpool,0):
                i.lrc.counting()

        self.itemgroup.update()
        
        pygame.sprite.groupcollide(self.GE.bulletpool,self.blockgroup,1,0)
        pygame.sprite.groupcollide(self.GE.bulletpool,self.enemygroup,1,0)

        items = pygame.sprite.spritecollide(self.GE, self.itemgroup, 1)
        if items != []:
            for i in items:
                if i.effect.__contains__("life+"):
                    self.GE.status["life"] += i.effect["life+"]
                if i.effect.__contains__("ammo+"):
                    self.GE.status["ammo"] += i.effect["ammo+"]
         
#            #      print "hit"
        
        self.blockgroup.draw(self.screen)
        self.enemygroup.draw(self.screen)

        self.itemgroup.draw(self.screen)
        self.GEgroup.draw(self.screen)
        self.GE.bulletpool.draw(self.screen)
        
        if pygame.sprite.collide_circle(self.GE,self.mapLp):
#            #      print "pre act"
            if self.mapNumber != 0:
                self.reset_map()
            self.changepermap()
        if pygame.sprite.collide_circle(self.GE,self.mapRp):
#            #      print "next act"
            if self.mapNumber < len(self.mapfilelist) - 1:
                self.reset_map()
            self.changenextmap()
    
    def changepermap(self):
#        self.enemy_clean()
#        oldrect = self.GE.rect.bottom
        if self.mapNumber > 0:
            self.GE.set_stop()
            self.mapNumber -= 1
            self.mapfile = PATHhead + self.mapfilelist[self.mapNumber] + Utxt +".txt"
            
            self.mapls = readMap(self.mapfile, ["f"],SCREEN_SIZE[0]/20)
            self.mapbls = readMap(self.mapfile, ["x","E"],SCREEN_SIZE[0]/20)
            self.mapdfls = readMap(self.mapfile, ["z"],SCREEN_SIZE[0]/20)
            
            self.mapLp = ChangeMapPoint(self.mapfile,'l',20)
            self.mapRp = ChangeMapPoint(self.mapfile,'r',20)

            self.blockgroup = buildMap(self.blockimage, self.mapls, 20, 20)
            
            self.a = buildMap(self.blockbackimage, self.mapbls, 20, 20)
            self.b = buildMap(self.dustfloorimage, self.mapdfls,20,20)
        
            self.blockbackgroup = pygame.sprite.Group()
            self.blockbackgroup.add(self.a.sprites())
            self.blockbackgroup.add(self.b.sprites())  
            
            self.GE.mapblock = self.blockgroup
            self.inpoint = readMap(self.mapfile,"r",SCREEN_SIZE[0]/20)
#            #      print "pre:",self.inpoint
            self.GE.set_default_loc(self.inpoint[0][0]*20-50,self.inpoint[0][1],True,19)

            
            self.enemy_set()
            
#            #      print "change per map"
    
    def changenextmap(self):

        if self.mapNumber < len(self.mapfilelist) - 1:
            self.GE.set_stop()
            self.mapNumber += 1
#            #      print self.mapNumber
            self.mapfile = PATHhead + self.mapfilelist[self.mapNumber] + Utxt +".txt"

            self.mapls = readMap(self.mapfile, ["f"],SCREEN_SIZE[0]/20)
            self.mapbls = readMap(self.mapfile, ["x","E"],SCREEN_SIZE[0]/20)
            self.mapdfls = readMap(self.mapfile, ["z"],SCREEN_SIZE[0]/20)
            
            self.mapLp = ChangeMapPoint(self.mapfile,'l',20)
            self.mapRp = ChangeMapPoint(self.mapfile,'r',20)
      
            self.blockgroup = buildMap(self.blockimage, self.mapls, 20, 20)
            
            self.a = buildMap(self.blockbackimage, self.mapbls, 20, 20)
            self.b = buildMap(self.dustfloorimage, self.mapdfls,20,20)
        
            self.blockbackgroup = pygame.sprite.Group()
            self.blockbackgroup.add(self.a.sprites())
            self.blockbackgroup.add(self.b.sprites())  
            
            self.GE.mapblock = self.blockgroup

            
            self.inpoint = readMap(self.mapfile,"l",SCREEN_SIZE[0]/20)
#            #      print "next:",self.inpoint
            self.GE.set_default_loc(self.inpoint[0][0]+50,self.inpoint[0][1],False,19)
            
            
            self.enemy_set()
            
#            #      print "change next map"
#载入地图链
#取当前地图
#设置玩家方向和初始位置
#走出地图时设置状态，向前走，向后走
        