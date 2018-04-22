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
import pygame
import sys
from netmachine import get_host_ip
from netmachine import PORT
# import os

# print(sys.platform)
PATHhead = None
Utxt = None





if sys.platform == "linux2":
    PATHhead = ".//"
    Utxt = "u"
else:
    PATHhead = ".\\"
    Utxt = ""
    
SCREEN_SIZE = (1280,720)
CAPTION = "Black Face - the shadow of Big Head - alpha 0.0.3"

scr = pygame.display.set_mode(SCREEN_SIZE,0,32)
pygame.init()
clock = pygame.time.Clock()

ICON = pygame.image.load(PATHhead+"icon.jpg").convert_alpha()

##  item
MEDIMAGE = pygame.image.load(PATHhead+"medicine.png").convert_alpha()
AMIMAGE = pygame.image.load(PATHhead+"ammo.png").convert_alpha()


##  player self
PLAYERIMAGE = pygame.image.load(PATHhead+"playerf1_f4.png").convert_alpha()

##  attack
BULLETIMAGE = pygame.image.load(PATHhead+"ball2.png").convert_alpha()
HITWAVEIMAGE = pygame.image.load(PATHhead+"hitwavef1_f3.png").convert_alpha()

## enemy self
ENEMYIMAGE = pygame.image.load(PATHhead+"gang1f1_f3.png").convert_alpha()
ENEMYBULLETIMAGE = pygame.image.load(PATHhead+"ball3.png").convert_alpha()


## boss self
BOSSIMAGE = pygame.image.load(PATHhead+"dd200-600.png").convert_alpha()
BOSSBULLETIMAGE = pygame.image.load(PATHhead+"ballb.png").convert_alpha()

## map 
DUSTFLOORIMAGE = pygame.image.load(PATHhead+"dust20_20.png").convert_alpha()
BLOCKBACKIMAGE = pygame.image.load(PATHhead+"block4.png").convert_alpha()
BLOCKIMAGE = pygame.image.load(PATHhead+"block3.png").convert_alpha()
BACKEVE = pygame.image.load(PATHhead+"back.jpg").convert()

global USENET
USENET = 0

N_LEFT = "4"
N_RIGHT = "6"
N_JUMP = "8"
N_SHOOT = "5"
N_MELEE = "2"

N_EXIT = "q"

ACTLIST_FOR_NET = [N_LEFT,N_RIGHT,N_JUMP,N_SHOOT,N_MELEE]

import Tkinter


class TitleInput():
    def __init__(self,titlename,setin):
        self.frameinput = Tkinter.Frame(setin)
        self.textname = Tkinter.Label(self.frameinput,text = titlename+":")
        self.textname.pack(side="left")
        
        
        self.textnamein = Tkinter.Entry(self.frameinput)
        self.textnamein.pack(side="right")
        self.frameinput.pack()
    
    def get_data(self):
        rp = self.textnamein.get()
        return rp
    
        
class NetGui():
    def __init__(self):
        self.tk = Tkinter.Tk()
        
        self.var = Tkinter.IntVar()
        self.cbut = Tkinter.Checkbutton(self.tk,text = "use net control",variable = self.var)
        self.cbut.pack()
               
        self.ipportframe = Tkinter.Label(text = "game host -> " + get_host_ip() + " : " + str(PORT))
        self.ipportframe.pack()
        
        self.but1 = Tkinter.Button(self.tk,text = "set done",command = self._check_state)
        self.but1.pack()
        
        self.fromip = None
        self.fromport = None
        
        self.tk.mainloop()
        
    def _check_state(self):
        global USENET
        USENET = self.var.get()
        self.tk.destroy()
    
netgui = NetGui()



