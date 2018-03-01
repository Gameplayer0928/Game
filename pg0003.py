# coding=utf-8
#!/usr/bin/python
'''
Created on 2018年2月2日
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
#from gameelement import *
from mapmachine import *
#from AI import *

from gameelement import GameEntity
import sys


print """W S A D key to move\n
       SPACE key to jump\n
       K key to shoot\n
       TAB key to show status\n
       L  key to Melee Attack\n
       [shoot enemy to collect ammo to kill the Big Head!!!]
       """



pygame.display.set_caption(CAPTION)
pygame.display.set_icon(ICON)



background = pygame.surface.Surface(SCREEN_SIZE)

playerimage = pygame.image.load(".\\playerf1_f4.png").convert_alpha()

bulletimage = pygame.image.load(".\\ball2.png").convert_alpha()





# ab.main_image = playerimageddddddddd

ab = GameEntity(playerimage,36,50,4,bulletimage)

# boss.set_default_loc(900, 300, False)

# enemygroup = pygame.sprite.Group()
# enemygroup.add(boss)
# ab.set_default_loc(inpoint[0][0],inpoint[0][1],19)

maplink = None

mlfile = open('.\\maplink.txt',"r")
for i in mlfile:
    maplink = i.split(",")
mlfile.close()



# pg = pygame.sprite.Group()
# pg.add(ab)


mapcurrent = MapState(maplink,ab,scr)

mapcurrent.mapNumber = 0                               
# ab.mapblock = blockgroup

tabhold = False

while True:
#    absb = StateBoard(ab,scr)
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_TAB:
                tabhold = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_TAB:
                tabhold = False
     

    mapcurrent.running()
    
    if tabhold:
        mapcurrent.GEsb.show()
    
    #background.blit(screen,(0,0))
    pygame.display.update()