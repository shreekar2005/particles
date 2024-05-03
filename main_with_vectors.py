# Importing pygame module
import pygame
from pygame.locals import *
import time
import math
import numpy as np 
from pygame import mixer 
from timeit import default_timer as timer 
from pygame.math import Vector2

# pygame setup
pygame.init()
mixer.init() 

mixer.music.load("pop_pp.mp3") 
mixer.music.set_volume(1) 
mixer.music.play() 

width=1920
height=1080
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
running = True
g=Vector2(0,0) #gravity
particle_pos=[]
particle_vel=[]
particle_mass=[]
rad=5
e_pp=0.1 #coeff of res between particle particle
e_pg=0.7 #coeff of res between particle and ground
dt=0
m=1 #mass of particle
G=10 #gravity constant


white = (155, 155, 155)
green = (0, 255, 0)
blue = (0, 0, 128)

font = pygame.font.Font('freesansbold.ttf', 50)
text1 = font.render('Gravity OFF', True, white)
text2 = font.render('Gravity ON', True, white)
text3 = font.render('Slow motion OFF', True, white)
text4 = font.render('Slow motion ON', True, white)
textRect = text1.get_rect()
textRect.center = (width/2,height/2)
textRect2 = text3.get_rect()
textRect2.center = (width/2,height/2+50)
slowmotion=False
maxmass=1


#######################################################################################################################################

def masscolor(mass):
    fraction=mass*mass/(10000)
    if(fraction>1):
        fraction=1
    fraction=math.sqrt(fraction)
    color=(255,255*(1-fraction),255*(1-fraction))
    return color

def moveparticle(id):
         
    if(particle_pos[id][1]>height-rad or particle_pos[id][1]<rad):
            #mixer.music.play() 
        if particle_pos[id][1]>height-rad:
            particle_pos[id][1]=height-rad
        else:
            particle_pos[id][1]=rad
        particle_vel[id][1]=-e_pg*particle_vel[id][1]
                  
    elif(particle_pos[id][0]>width-rad or particle_pos[id][0]<rad):
        #mixer.music.play() 
        particle_vel[id][0]=-e_pg*particle_vel[id][0]
        if(particle_pos[id][0]>width-rad):
            particle_pos[id][0]=width-rad
        else:
            particle_pos[id][0]=rad 
                    
    else:
        particle_pos[id][0]+=particle_vel[id][0]*dt
        particle_pos[id][1]+=particle_vel[id][1]*dt


def gravity(id1,id2,dist):
    global particle_pos,particle_vel
    posvec1 = particle_pos[id1]
    posvec2 = particle_pos[id2]
    velvec1 = particle_vel[id1]
    velvec2 = particle_vel[id2]
    relvel=velvec2-velvec1
    relpos=posvec2-posvec1
    accn1=G*particle_mass[id2]/dist/dist/dist*relpos
    accn2=G*particle_mass[id1]/dist/dist/dist*relpos
    velvec1=velvec1+accn1*dt
    velvec2=velvec2-accn2*dt
        
    particle_vel[id1]=velvec1
    particle_vel[id2]=velvec2

def collision(id1,id2,dist) :
    mixer.music.play() 
    global particle_pos,particle_vel
    posvec1 = particle_pos[id1]
    posvec2 = particle_pos[id2]
    velvec1 = particle_vel[id1]
    velvec2 = particle_vel[id2]
    
    vcom=(particle_mass[id1]*velvec1+particle_mass[id2]*velvec2)/(particle_mass[id1]+particle_mass[id2])
    relpos=posvec2-posvec1
    relvel=velvec2-velvec1
    if relvel.length()==0:
        relvel=relpos
    relvelcap=relvel.normalize()
    relpos=posvec2-posvec1
    normal_vec=relpos.normalize()
    if relvelcap.dot(normal_vec)>0 :
        return
    
    d=2*rad-dist
    if(d>0):
        try:
            posvec1-=d*normal_vec #idk what error is this :(
            posvec2+=d*normal_vec
        except:
            print("error")
    
    relvel_mag=relvel.dot(relvel)
    vel=e_pp*normal_vec*(normal_vec.dot(relvel))
    if(vel.dot(vel)<1):
        vel=2*normal_vec
           
    velvec1=vcom+vel*particle_mass[id2]/(particle_mass[id1]+particle_mass[id2])
    velvec2=vcom-vel*particle_mass[id1]/(particle_mass[id1]+particle_mass[id2])
    
    particle_vel[id1]=velvec1
    particle_vel[id2]=velvec2
    particle_pos[id1]=posvec1
    particle_pos[id2]=posvec2
    
##################################################################################################################################    
    
start = timer() 
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
    keys=pygame.key.get_pressed()
    if keys[K_q]:
        running = False  
                
    screen.fill("black")
    
    if(g==0):
        screen.blit(text1, textRect)
    else:
        screen.blit(text2, textRect)
    if(slowmotion):
        screen.blit(text4, textRect2)
    else:
        screen.blit(text3, textRect2)
    
    if pygame.mouse.get_pressed()[0]==True: #for interaction with balls
        mousepos=Vector2(pygame.mouse.get_pos())
        for id in range(0,len(particle_pos)):
            if(math.dist(particle_pos[id].distance_to(mousepos))<=rad):
                keys=pygame.key.get_pressed()
                if keys[K_d]:
                    particle_vel[id]+=Vector2(0.1,0)
                if keys[K_a]:
                    particle_vel[id]-=Vector2(0.1,0)
                    
    keys=pygame.key.get_pressed()
    if keys[K_f]:
        canspawn=True
        for particle in particle_pos:
            if(Vector2(pygame.mouse.get_pos()).distance_to(particle)<2*rad):
                canspawn=False
        if(canspawn==True):
                particle_pos.append(Vector2(pygame.mouse.get_pos()))
                particle_vel.append(Vector2(0,0))
                particle_mass.append(1000)
                
    keys=pygame.key.get_pressed()
    if keys[K_e]:
        canspawn=True
        for particle in particle_pos:
            if(Vector2(pygame.mouse.get_pos()).distance_to(particle)<2*rad):
                canspawn=False
        if(canspawn==True):
                particle_pos.append(Vector2(pygame.mouse.get_pos()))
                particle_vel.append(Vector2(0,0))
                particle_mass.append(10)               
    
        
    if pygame.mouse.get_pressed()[2]==True:
        canspawn=True
        for particle in particle_pos:
            if(Vector2(pygame.mouse.get_pos()).distance_to(particle)<2*rad):
                canspawn=False
        if(canspawn==True):
                particle_pos.append(Vector2(pygame.mouse.get_pos()))
                particle_vel.append(Vector2(0,0))
                particle_mass.append(0.1)
                    
#####################################################################################################################################   
    
    for id in range(0,len(particle_pos)):
        particle_vel[id]+=g*dt
        
    for id in range(0,len(particle_pos)): 
        collisiondone=False
        for id2 in range(id+1,len(particle_pos)): #for collision
            print(particle_pos[id])
            dist=particle_pos[id].distance_to(particle_pos[id2])          
            if(dist<2*rad):
                if dist!=0:
                    collision(id,id2,dist)
                    collisiondone=True
            #if(dist>2.1*rad):
                #gravity(id,id2,dist)
    
    for id in range(len(particle_pos)-1,-1,-1): 
        collisiondone=False
        for id2 in range(id-1,-1,-1): #for collision
            dist=particle_pos[id].distance_to(particle_pos[id2])          
            if(dist<2*rad):
                if dist!=0:
                    collision(id,id2,dist)
                    collisiondone=True
    
                
    for id in range(0,len(particle_pos)):
        moveparticle(id)
    
                          
#####################################################################################################################################    
    
    for id in range(0,len(particle_pos)):
        pygame.draw.circle(screen,masscolor(particle_mass[id]),particle_pos[id], rad)
    
    # flip() the display to put your work on screen
    pygame.display.flip()
    dt=clock.tick(144)/100  # limits FPS to 144
    if pygame.mouse.get_pressed()[0]==True:
        dt=dt/10
        slowmotion=True
    else:
        slowmotion=False
    keys=pygame.key.get_pressed()
    if keys[K_g]:
        g=Vector2(0,9.8)
    if keys[K_h]:
        g=Vector2(0,0)
        
#print(particle_pos)
pygame.quit()