#coding: utf-8
import numpy as np        
import numpy as np 
import time
      
L4 = 9.30	#[cm]
L5 = 9.30
Lf = 5.30
Ltx = 0.50
Lty = 10.50
Ltz = 3.30

Mot = [(0), (0), (0), (np.pi/2), (0), (0)]
#Mot = [(10*np.pi/180), (-30*np.pi/180), (-20*np.pi/180), (-35*np.pi/180), (-45*np.pi/180), (60*np.pi/180)]

s7 = np.sin(Mot[0])
s9 = np.sin(Mot[2])
s11 = np.sin(Mot[1])
s13 = np.sin(Mot[3])
s15 = np.sin(Mot[5])
s17 = np.sin(Mot[4])
c7 = np.cos(Mot[0])
c9 = np.cos(Mot[2])
c11 = np.cos(Mot[1])
c13 = np.cos(Mot[3])
c15 = np.cos(Mot[5])
c17 = np.cos(Mot[4])
sabc = np.sin(Mot[2]+Mot[3]+Mot[4])
cabc = np.cos(Mot[2]+Mot[3]+Mot[4])
cab = np.cos(Mot[2]+Mot[3])
sab = np.sin(Mot[2]+Mot[3])

Prx = Lf*(c11*s15*s7 - c15*(-c7*sabc - cabc*s11*s7)) - (-(L4*s9+L5*sab)*c7 + (L4*c9+L5*cab)*s7*s11)
Prz = Lf*(-c11*c15*cabc + s11*s15) - Lty - c11*(L4*c9+L5*cab)
Pry = Lf*(-c11*c7*s15 + c15*(-c7*cabc*s11 + s7*sabc)) + ((L4*s9+L5*sab)*s7-(L4*c9+L5*cab)*c7*s11)

print("%f"% ( Prx))
print("%f"% ( Pry))
print("%f"% ( Prz))
 
 
