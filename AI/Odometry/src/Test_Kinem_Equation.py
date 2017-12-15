import numpy as np        
L4 = 93.0
L5 = 93.0
Lf = 33.5
Ltx = 5
Lty = 122.2
Ltz = 37
Mot = [(10*np.pi/180), (-20*np.pi/180), (-30*np.pi/180), (-35*np.pi/180), (60*np.pi/180), (-45*np.pi/180)]
s7 = np.sin(Mot[0])
#s8 = np.sin(Mot[1])
s9 = np.sin(Mot[1])
#s10 = np.sin(Mot[3])
s11 = np.sin(Mot[2])
#s12 = np.sin(Mot[5])
s13 = np.sin(Mot[3])
#s14 = np.sin(Mot[7])
s15 = np.sin(Mot[4])
#s16 = np.sin(Mot[9])
s17 = np.sin(Mot[5])
#s18 = np.sin(Mot[11])
c7 = np.cos(Mot[0])
#c8 = np.cos(Mot[1])
c9 = np.cos(Mot[1])
#c10 = np.cos(Mot[3])
c11 = np.cos(Mot[2])
#c12 = np.cos(Mot[5])
c13 = np.cos(Mot[3])
#c14 = np.cos(Mot[7])
c15 = np.cos(Mot[4])
#c16 = np.cos(Mot[9])
c17 = np.cos(Mot[5])
#c18 = np.cos(Mot[11])
sabc = np.sin(Mot[1]+Mot[3]+Mot[5])
cabc = np.cos(Mot[1]+Mot[3]+Mot[5])
cab = np.cos(Mot[1]+Mot[3])
sab = np.sin(Mot[1]+Mot[3])
#slabc = np.sin(Mot[3]+Mot[7]+Mot[11])
#clabc = np.cos(Mot[3]+Mot[7]+Mot[11])
#clab = np.cos(Mot[3]+Mot[7])
#slab = np.sin(Mot[3]+Mot[7])

r11 = -s11*s15+c11*c15*cabc
r12 = -((s7*sabc-c7*s11*cabc)*c15-c7*c11*s15)
r13 = -((-c7*sabc-s7*s11*cabc)*c15-s7*c11*s15)

r21 = -c7*cabc+s7*s11*sabc
r22 = -((-c7*sabc-s7*s11*cabc)*s15-s7*c11*c15)
r23 = -(-(-c7*sabc-s7*s11*cabc)*s15-s7*c11*c15)

r31 = -c11*sabc
r32 = -(s11*s15+c11*c15*cabc)
r33 = -(-s11*c15-c11*s15*cabc)
#r11 = ((s7*sabc)-(c7*s11*cabc))*c15-(c7*c11*s15)
#r21 = (-c7*sabc-s7*s11*cabc)*c15-s7*c11*s15
#r31 = -s11*s15+c11*c15*cabc

#r12 = -(s7*sabc-c7*s11*cabc)*s15-c7*c11*c15
#r22 = -(-c7*sabc-s7*s11*cabc)*s15-s7*c11*c15
#r32 = -s11*c15-c11*s15*cabc

#r13 = s7*cabc+c7*s11*sabc
#r23 = -c7*cabc+s7*s11*sabc
#r33 = -c11*sabc

Prx = (L4*s9+L5*sab)*s7-(L4*c9+L5*cab)*c7*s11+Lf*(-r21)-Ltx*(-r21)-Lty*(-r13)+Ltz*r11
Pry = -(L4*s9+L5*sab)*c7-(L4*c9+L5*cab)*s7*s11+Lf*r21-Ltx*r21-Lty*r22+Ltz*r23
Prz = (L4*c9+L5*cab)*c11 + Lf*r31 -Ltx*r31 - Lty*r32 + Ltz*r33

print("\nr11 = %f = "% r11)
print("\nr21 = %f = "% r21)
print("\nr31 = %f = "% r31)
print("\nr12 = %f = "% r12)
print("\nr22 = %f = "% r22)
print("\nr32 = %f = "% r32)
print("\nr13 = %f = "% r13)
print("\nr23 = %f = "% r23)
print("\nr33 = %f = "% r33)
print("\nPx = %f = "% Prx)
print("\nPy = %f = "% Pry)
print("\nPz = %f = "% Prz)

