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


SCREEN_SIZE = (1280,720)
CAPTION = "Black Face - the shadow of Big Head - alpha 0.0.3"

scr = pygame.display.set_mode(SCREEN_SIZE,0,32)
pygame.init()
clock = pygame.time.Clock()

ICON = pygame.image.load(".\\icon.jpg").convert_alpha()