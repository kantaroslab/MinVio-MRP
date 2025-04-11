#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 12:41:25 2022

@author: samarth
"""
import numpy as np

class lm_motion(object):
    """
    define the workspace where robots reside
    """
    def __init__(self, pos, func, vel = 0, direction = 0, dist = 0, rotation = "cw"):
        # dimension of the workspace
        self.pos = pos
        self.func = func
        self.vel = vel
        self.dist = dist
        self.dist_travelled = 0
        self.heading = direction
        self.direction = direction 
        
        # circle params
        if dist>0:
            self.circle_center = np.array(pos) + np.array([np.cos(direction)*dist,\
                                                       np.sin(direction)*dist]) 
            self.pos_wrt_center = direction - np.pi
            self.rotation = rotation
            self.d_theta = vel/dist # vel = r*theta
        
    def move_lm(self):
        if self.vel == 0:
            return self.pos
        
        if self.func == 1:
            self.pos[0] += self.vel*np.cos(self.direction)
            self.pos[1] += self.vel*np.sin(self.direction)
            return self.pos
        
        if self.func == 2:
            if self.heading == self.direction:
                 self.dist_travelled+=self.vel
            else:
                self.dist_travelled-=self.vel
            if self.dist_travelled>self.dist:
                self.heading-=np.pi
                self.dist_travelled-=self.vel*2
            elif self.dist_travelled<0:
                self.heading+=np.pi
                self.dist_travelled+=self.vel*2
            self.pos[0] += self.vel*np.cos(self.heading)
            self.pos[1] += self.vel*np.sin(self.heading)
            return self.pos
        
        if self.func == 3:
            if self.rotation == "cw":
                self.pos_wrt_center -= self.d_theta
            elif self.rotation == "acw":
                self.pos_wrt_center += self.d_theta
            self.pos = self.circle_center + np.array([np.cos(self.pos_wrt_center)*self.dist,\
                                                       np.sin(self.pos_wrt_center)*self.dist]) 
            return self.pos