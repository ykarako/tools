#!/usr/bin/env python
import pygame
from pygame.locals import *

pygame.joystick.init()

try:
   joystick = pygame.joystick.Joystick(0)
   joystick.init()
   print('joystick name: {}'.format(joystick.get_name()))
   print('num buttons: {}'.format(joystick.get_numbuttons()))
except pygame.error:
   print('joystick is not connected')

pygame.init()

active = True
while active:
   for e in pygame.event.get():
       if e.type == QUIT:
           active = False

       if e.type == pygame.locals.JOYAXISMOTION:
           print('axis: {}, {}'.format(joystick.get_axis(0), joystick.get_axis(1)))
       elif e.type == pygame.locals.JOYBUTTONDOWN:
           print('button '+str(e.button)+' is pushed')
       elif e.type == pygame.locals.JOYBUTTONUP:
           print('button '+str(e.button)+' is released')
