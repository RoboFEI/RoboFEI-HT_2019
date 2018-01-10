import numpy as np 
import time
ti = time.clock()       
L4 = 93.0
L5 = 93.0
Lf = 33.5
Ltx = 5
Lty = 122.2
Ltz = 37
Mot = [(10*np.pi/180), (-20*np.pi/180), (-30*np.pi/180), (-35*np.pi/180), (60*np.pi/180), (-45*np.pi/180)]
s7 = np.sin(Mot[0])
s9 = np.sin(Mot[1])
s11 = np.sin(Mot[2])
s13 = np.sin(Mot[3])
s15 = np.sin(Mot[4])
s17 = np.sin(Mot[5])
c7 = np.cos(Mot[0])
c9 = np.cos(Mot[1])
c11 = np.cos(Mot[2])
c13 = np.cos(Mot[3])
c15 = np.cos(Mot[4])
c17 = np.cos(Mot[5])
sabc = np.sin(Mot[1]+Mot[3]+Mot[5])
cabc = np.cos(Mot[1]+Mot[3]+Mot[5])
cab = np.cos(Mot[1]+Mot[3])
sab = np.sin(Mot[1]+Mot[3])

r11 = -((-c7*sabc-s7*s11*cabc)*c15-s7*c11*s15)
r12 = -(-(-c7*sabc-s7*s11*cabc)*s15-s7*c11*c15)
r13 = -(-c7*cabc+s7*s11*sabc)

r21 = -(-s11*s15+c11*c15*cabc)
r22 = -(-s11*c15-c11*s15*cabc)
r23 = -(-c11*sabc)

r31 = (s7*sabc-c7*s11*cabc)*c15-(c7*c11*s15)
r32 = (-c7*sabc-s7*s11*cabc)*c15-s7*c11*s15
r33 = -s11*s15+c11*c15*cabc

P_x = ((L4*s9+L5*sab)*s7-(L4*c9+L5*cab)*c7*s11) 
P_y = (-(L4*s9+L5*sab)*c7-(L4*c9+L5*cab)*s7*s11) 
P_z = ((L4*c9+L5*cab)*c11) 

#r11 = (s7*sabc-c7*s11*cabc)*c15-(c7*c11*s15)
#r21 = (-c7*sabc-s7*s11*cabc)*c15-s7*c11*s15
#r31 = -s11*s15+c11*c15*cabc

#r12 = -(s7*sabc-c7*s11*cabc)*s15-c7*c11*c15
#r22 = -(-c7*sabc-s7*s11*cabc)*s15-s7*c11*c15
#32 = -s11*c15-c11*s15*cabc

#r13 = s7*cabc+c7*s11*sabc
#r23 = -c7*cabc+s7*s11*sabc
#r33 = -c11*sabc

Px = Lf*r11 - Ltx - P_y
Py = Lf*r21 - Lty - P_z
Pz = Lf*r31 + Ltz + P_x
tf = time.clock()

T = tf - ti

print("%f \t %f \t %f \t %f"% (r11, r12, r13, Px))
print("%f \t %f \t %f \t %f"% (r21, r22, r23, Py))
print("%f \t %f \t %f \t %f"% (r31, r32, r33, Pz))
print(T)


