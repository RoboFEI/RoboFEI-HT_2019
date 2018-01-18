import numpy as np 
import time
L4 = 93.0
L5 = 93.0
Lf = 33.5
Ltx = 5
Lty = 122.2
Ltz = 37
#Mot = [(0), (0), (0), (0), (0), (0)]
Mot = [(10*np.pi/180), (-20*np.pi/180), (-30*np.pi/180), (-35*np.pi/180), (60*np.pi/180), (-45*np.pi/180)]
s7 = np.sin(Mot[0])
s8 = np.sin(Mot[0])
s9 = np.sin(Mot[1])
s10 = np.sin(Mot[1])
s11 = np.sin(Mot[2])
s12 = np.sin(Mot[2])
s13 = np.sin(Mot[3])
s14 = np.sin(Mot[3])
s15 = np.sin(Mot[4])
s16 = np.sin(Mot[4])
s17 = np.sin(Mot[5])
s18 = np.sin(Mot[5])
c7 = np.cos(Mot[0])
c8 = np.cos(Mot[0])
c9 = np.cos(Mot[1])
c10 = np.cos(Mot[1])
c11 = np.cos(Mot[2])
c12 = np.cos(Mot[2])
c13 = np.cos(Mot[3])
c14 = np.cos(Mot[3])
c15 = np.cos(Mot[4])
c16 = np.cos(Mot[4])
c17 = np.cos(Mot[5])
c18 = np.cos(Mot[5])
sabc = np.sin(Mot[1]+Mot[3]+Mot[5])
cabc = np.cos(Mot[1]+Mot[3]+Mot[5])
cab = np.cos(Mot[1]+Mot[3])
sab = np.sin(Mot[1]+Mot[3])
slabc = np.sin(Mot[1]+Mot[3]+Mot[5])
clabc = np.cos(Mot[1]+Mot[3]+Mot[5])
clab = np.cos(Mot[1]+Mot[3])
slab = np.sin(Mot[1]+Mot[3])
cl14 = np.cos(Mot[3])
cl16 = np.cos(Mot[4])
cl12 = np.cos(Mot[2])
sl14 = np.sin(Mot[3])
sl16 = np.sin(Mot[4])
sl12 = np.sin(Mot[2])

Pr_x = ((L4*s9+L5*sab)*s7-(L4*c9+L5*cab)*c7*s11) 
Pr_y = (-(L4*s9+L5*sab)*c7-(L4*c9+L5*cab)*s7*s11) 
Pr_z = ((L4*c9+L5*cab)*c11) 

Prx = Lf*(c11*s15*s7 - c15*(-c7*sabc - cabc*s11*s7)) - Ltx - Pr_y
Prz = Lf*(-c11*c15*cabc + s11*s15) - Lty - Pr_z
Pry = Lf*(-c11*c7*s15 + c15*(-c7*cabc*s11 + s7*sabc)) + Ltz + Pr_x



Pl_x = ((L4*s10+L5*slab)*s8-(L4*c10+L5*clab)*c8*sl12) 
Pl_y = (-(L4*s10+L5*slab)*c8-(L4*c10+L5*clab)*s8*sl12) 
Pl_z = ((L4*c10+L5*clab)*cl12) 

Plx = Lf*(cl12*sl16*s8 - cl16*(-c8*slabc - clabc*sl12*s8)) - Ltx - Pl_y
Plz = Lf*(-cl12*cl16*clabc + sl12*sl16) - Lty - Pl_z
Ply = Lf*(-cl12*c8*sl16 + cl16*(-c8*clabc*sl12 + s8*slabc)) - Ltz + Pl_x

print("%f, \t%f"% ( Prx, Plx))
print("%f, \t%f"% ( Pry, Ply))
print("%f, \t%f"% ( Prz, Plz))


#[[c11*s15*s7 - c15*(-c7*sabc - cabc*s11*s7)
#  c11*c15*s7 - s15*(c7*sabc + cabc*s11*s7) c7*cabc - s11*s7*sabc
#  Lf*(c11*s15*s7 - c15*(-c7*sabc - cabc*s11*s7)) - Ltx - Py]
# [-c11*c15*cabc + s11*s15 c11*cabc*s15 + c15*s11 c11*sabc
#  Lf*(-c11*c15*cabc + s11*s15) - Lty - Pz]
# [-c11*c7*s15 + c15*(-c7*cabc*s11 + s7*sabc)
#  -c11*c15*c7 + s15*(c7*cabc*s11 - s7*sabc) c7*s11*sabc + cabc*s7
#  Lf*(-c11*c7*s15 + c15*(-c7*cabc*s11 + s7*sabc)) + Ltz + Px]


