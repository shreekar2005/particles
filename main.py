# Importing pygame module
import pygame
from pygame.locals import *
import time
import math
import numpy as np 
from pygame import mixer 
from timeit import default_timer as timer 


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
g=0 #gravity
particle_pos=[]
particle_prepos=particle_pos.copy()
particle_vel=[]
particle_mass=[]
particle_rad=[]
rad=5
e_pp=0.9 #coeff of res between particle particle
e_pg=0.9 #coeff of res between particle and ground
dt=0
m=1 #mass of particle
G=0 #gravity constant


white = (55, 55, 55)
green = (0, 255, 0)
blue = (0, 0, 128)

font = pygame.font.Font('freesansbold.ttf', 50)
font2 = pygame.font.Font('freesansbold.ttf', 30)
text1 = font.render('Gravity OFF(G)', True, white)
text2 = font.render('Gravity ON(H)', True, white)
text3 = font.render('Slow motion OFF(leftclick)', True, white)
text4 = font.render('Slow motion ON(release)', True, white)
text5 = font.render('grnd Gravity OFF(j)', True, white)
text6 = font.render('grnd Gravity ON(k)', True, white)
text7 =  font2.render(''''rightclick' to create light particle, 'f' for create heavy particle, 'e' for creating normal particle, 'q' to quit''', True, white)

textRect = text1.get_rect()
textRect.center = (width/2+60,height/2)
textRect2 = text3.get_rect() 
textRect2.center = (width/2,height/2+50)
textRect3 = text1.get_rect()
textRect3.center = (width/2,height/2+100) 
textRect4= text7.get_rect()
textRect4.center = (width/2,height/2+150) 
slowmotion=False
maxmass=1 


#######################################################################################################################################

def mass_to_rad(mass):
    fraction=math.cbrt(mass)/(10)*20
    if fraction<=8:
        fraction=8
    return fraction

def mass_to_color(mass):
    '''
    fraction=mass*mass/(10000)
    if(fraction>1):
        fraction=1
    if(fraction<0.06):
        fraction=0.06
    fraction=math.sqrt(fraction)
    color=(255,255*(1-fraction),255*(1-fraction))
    '''
    if(mass==10):
        color=(255,90,90)
    if(mass==100000):
        color=(255,0,0)
    if(mass==0.1):
        color=(255,255,255)
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
    posvec1 = np.array(particle_pos[id1])
    posvec2 = np.array(particle_pos[id2])
    velvec1 = np.array(particle_vel[id1])
    velvec2 = np.array(particle_vel[id2])
    relvel=velvec2-velvec1
    relpos=posvec2-posvec1
    accn1=G*particle_mass[id2]/dist/dist/dist*relpos
    accn2=G*particle_mass[id1]/dist/dist/dist*relpos
    velvec1=velvec1+accn1*dt
    velvec2=velvec2-accn2*dt
        
    particle_vel[id1]=velvec1.tolist()
    particle_vel[id2]=velvec2.tolist()

def collision(id1,id2,dist) :
    mixer.music.play() 
    global particle_pos,particle_vel
    posvec1 = np.array(particle_pos[id1])
    posvec2 = np.array(particle_pos[id2])
    velvec1 = np.array(particle_vel[id1])
    velvec2 = np.array(particle_vel[id2])
    vcom=(particle_mass[id1]*velvec1+particle_mass[id2]*velvec2)/(particle_mass[id1]+particle_mass[id2])
    relpos=posvec2-posvec1
    relvel=velvec2-velvec1
    relvelcap=relvel/math.sqrt(relvel.dot(relvel))
    relpos=posvec2-posvec1
    if relvel.dot(relpos)>0 :
        return
    normal_vec=relpos/dist
    d=2*rad-dist
    
    if(1):
        try:
            posvec1-=d*normal_vec #idk what error is this :(
            posvec2+=d*normal_vec
        except:
            print("error")
    
    relvel_mag=relvel.dot(relvel)
    vel=e_pp*normal_vec*(normal_vec.dot(relvel))
    vel=vel-(relvel-normal_vec*(normal_vec.dot(relvel)))
    if(vel.dot(vel)<1):
        vel=2*normal_vec
           
    velvec1=vcom+vel*particle_mass[id2]/(particle_mass[id1]+particle_mass[id2])
    velvec2=vcom-vel*particle_mass[id1]/(particle_mass[id1]+particle_mass[id2])
    
    particle_vel[id1]=velvec1.tolist()
    particle_vel[id2]=velvec2.tolist()
    particle_pos[id1]=posvec1.tolist()
    particle_pos[id2]=posvec2.tolist()
    
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
    
    if(G==0):
        screen.blit(text1, textRect)
    else:
        screen.blit(text2, textRect)
    if(g==0):
        screen.blit(text5, textRect3)
    else:
        screen.blit(text6, textRect3)
    if(slowmotion):
        screen.blit(text4, textRect2)
    else:
        screen.blit(text3, textRect2)
        
    screen.blit(text7, textRect4)
    
    if pygame.mouse.get_pressed()[0]==True: #for interaction with balls
        mousepos=pygame.mouse.get_pos()
        for id in range(0,len(particle_pos)):
            if(math.dist(particle_pos[id],mousepos)<=2*rad):
                keys=pygame.key.get_pressed()
                if keys[K_d]:
                    particle_vel[id][0]+=0.1
                if keys[K_a]:
                    particle_vel[id][0]-=0.1
    
    
    keys=pygame.key.get_pressed()
    if keys[K_f]:
        canspawn=True
        for particle in particle_pos:
            if(math.dist(pygame.mouse.get_pos(),particle)<2*rad):
                canspawn=False
        if(canspawn==True):
                particle_pos.append(list(pygame.mouse.get_pos()))
                particle_vel.append([0,0])
                particle_mass.append(100000)
                particle_rad.append(mass_to_rad(100000))
                
    keys=pygame.key.get_pressed()
    if keys[K_e]:
        canspawn=True
        for particle in particle_pos:
            if(math.dist(pygame.mouse.get_pos(),particle)<2*rad):
                canspawn=False
        if(canspawn==True):
                particle_pos.append(list(pygame.mouse.get_pos()))
                particle_vel.append([0,0])
                particle_mass.append(10) 
                particle_rad.append(mass_to_rad(50))              

        
    if pygame.mouse.get_pressed()[2]==True:
        if(pygame.mouse.get_pos() not in particle_pos):
            canspawn=True
            for particle in particle_pos:
                if(math.dist(pygame.mouse.get_pos(),particle)<2*rad):
                    canspawn=False
            if(canspawn==True):
                    particle_pos.append(list(pygame.mouse.get_pos()))
                    particle_vel.append([0,0])
                    particle_mass.append(0.1)
                    particle_rad.append(mass_to_rad(0.1))
                    
#####################################################################################################################################   
    
    for id in range(0,len(particle_pos)):
        particle_vel[id][1]+=g*dt
    
    collisiondone=False
      
    for id in range(0,len(particle_pos)):  
        for id2 in range(id+1,len(particle_pos)): #for collision
            dist=math.dist(particle_pos[id],particle_pos[id2])          
            if(dist<2*rad):
                if dist!=0:
                    collision(id,id2,dist)
                    collisiondone=True
            
            if(dist>2.1*rad):
                gravity(id,id2,dist)

    for id in range(len(particle_pos)-1,-1,-1): 
        for id2 in range(id-1,-1,-1): #for collision
            dist=math.dist(particle_pos[id],particle_pos[id2])          
            if(dist<2*rad):
                if dist!=0:
                    collision(id,id2,dist)
                    collisiondone=True
        
    for id in range(0,len(particle_pos)):
        moveparticle(id)
                
    
    
                          
#####################################################################################################################################    
    
    for id in range(0,len(particle_pos)):
        pygame.draw.circle(screen,mass_to_color(particle_mass[id]),particle_pos[id],rad)
    
    # flip() the display to put your work on screen
    pygame.display.flip()
    dt=clock.tick(144)/100 # limits FPS to 144
    if pygame.mouse.get_pressed()[0]==True:
        dt=dt/10
        slowmotion=True
    else:
        slowmotion=False
    keys=pygame.key.get_pressed()
    if keys[K_g]:
        G=0.5
    if keys[K_h]:
        G=0
    if keys[K_j]:
        g=9.8
    if keys[K_k]:
        g=0
        
#print(particle_pos)
pygame.quit()