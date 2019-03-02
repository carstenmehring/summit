#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Carsten Mehring

"""

from fitparse import FitFile
import datetime
import os
import numpy as np
import math
from geopy import distance


# name of directory with fit files
directory='./Moves/'

# latitude and longitude of starting and end point 
latP=[45.918505,45.833166]
longP=[6.869781,6.865082]

# tolerance for starting and end point
r=0.00010


T=[]
A=[]
S=[]
N=[]
print("Analzing files...")
for filename in os.listdir(directory):

    if filename.endswith("Running.fit") & (filename.find('2019')!=-1):
        print(filename)
        fitfile = FitFile(directory+filename)

        lat=[]
        long=[]
        alt=[]
        temp=[]
        heart=[]
        d0=datetime.datetime(2000,1,1,0,0,0)
        
        # Get all data messages that are of type record
        for record in fitfile.get_messages('record'):
        
            la=record.get_value("position_lat")
            lo=record.get_value("position_long")            
            t=record.get_value("timestamp")
            aa=record.get_value("altitude")
            hh=record.get_value("heart_rate")
            
            if (la is not None) & (lo is not None) & (t is not None) & (aa is not None) & (hh is not None):
                if (record.get("position_lat").units!='semicircles'):
                    print("Latitude must be in semicircles")
                    break
                if (record.get("position_long").units!='semicircles'):
                    print("Latitude must be in semicircles")
                    break
                
                lat.append(la/(2**31/180))
                long.append(lo/(2**31/180))
                tt=t-d0;
                temp.append(tt.total_seconds())
                alt.append(aa)
                heart.append(hh)
                                       
        
        dist=np.zeros((len(lat),2)) 
        ind=np.empty(2,dtype=np.object)
        ind[0]=[]
        ind[1]=[]
        for k in range(0,len(lat)):      
            if (lat[k]!=None) & (long[k]!=None):
                for i in range(0,2):
                    d=math.sqrt((lat[k]-latP[i])**2+(long[k]-longP[i])**2)
                    if (d<r):
                        ind[i].append(k)
                              
        if (len(ind[0])>0) & (len(ind[1])>0):
            i2=ind[1][0]
            i1=[i for i in ind[0] if i < i2]
            if len(i1)>0:
                i1=max(i1)
                T.append(temp[i2]-temp[i1])
                N.append(filename)
                
                s=0; a=0;
                for k in range(i1,i2):
                    dist2D=distance.geodesic((lat[k],long[k]),(lat[k+1],long[k+1]))
                    s=s+math.sqrt((dist2D.meters)**2+(alt[k]-alt[k+1])**2)
                    if (alt[k+1]>alt[k]):
                        a=a+alt[k+1]-alt[k]
                S.append(s)
                A.append(a)
                
print("")
print("Results:")                
ind=np.argsort(T)   
for i in range(0,len(T)):        
    print (" * %s: T=%ds distance=%dm ascent=%dm" % (N[ind[i]],T[ind[i]],S[ind[i]],A[ind[i]]))
             

        
