import numpy as np 
import time
L4 = 9.30	#[cm]
L5 = 9.30
Lf = 5.30
Ltx = 0.50
Lty = 10.50
Ltz = 3.30

#Perna Direita:
#Movimento -> ValorMotor -> ValorAngulo

#CinturaPitch -> Drobrar (+) ->	(-)
#CinturaRoll -> Abrir (+) ->	(-)
#joelhoPitch -> Drobrar (+) ->	(-)
#tornozeloPitch -> Drobrar_P_Cima (+) ->	(-)
#tornozeloRoll -> Abrir (-) ->	(-)

#Mot = [(0), (0), (-np.pi/2), (np.pi/2), (np.pi/2), (np.pi/2)]
Mot = [((576 - 577)*0.0051232757), ((451 - 445)*0.0051232757), ((418 - 571)*0.0051232757), ((693 - 423)*0.0051232757), ((605 - 454)*0.0051232757), ((512 - 531)*0.0051232757)]

s7 = np.sin(Mot[0])
s8 = np.sin(Mot[0])
s9 = np.sin(-Mot[2])
s10 = np.sin(Mot[2])
s11 = np.sin(-Mot[1])
s12 = np.sin(-Mot[1])
s13 = np.sin(-Mot[3])
s14 = np.sin(Mot[3])
s15 = np.sin(-Mot[5])
s16 = np.sin(-Mot[5])
s17 = np.sin(Mot[4])
s18 = np.sin(-Mot[4])
c7 = np.cos(Mot[0])
c8 = np.cos(Mot[0])
c9 = np.cos(-Mot[2])
c10 = np.cos(Mot[2])
c11 = np.cos(-Mot[1])
c12 = np.cos(-Mot[1])
c13 = np.cos(-Mot[3])
c14 = np.cos(Mot[3])
c15 = np.cos(-Mot[5])
c16 = np.cos(-Mot[5])
c17 = np.cos(Mot[4])
c18 = np.cos(-Mot[4])
sabc = np.sin(-Mot[2]-Mot[3]+Mot[4])
cabc = np.cos(-Mot[2]-Mot[3]+Mot[4])
cab = np.cos(-Mot[2]-Mot[3])
sab = np.sin(-Mot[2]-Mot[3])
slabc = np.sin(Mot[2]+Mot[3]-Mot[4])
clabc = np.cos(Mot[2]+Mot[3]-Mot[4])
clab = np.cos(Mot[2]+Mot[3])
slab = np.sin(Mot[2]+Mot[3])
cl14 = np.cos(Mot[3])
cl16 = np.cos(-Mot[5])
cl12 = np.cos(-Mot[1])
sl14 = np.sin(Mot[3])
sl16 = np.sin(-Mot[5])
sl12 = np.sin(-Mot[1])


#s7 = np.sin(Mot[0])
#s8 = np.sin(Mot[0])
#s9 = np.sin(-Mot[2])
#s10 = np.sin(Mot[2])
#s11 = np.sin(-Mot[1])
#sl12 = np.sin(-Mot[1])
#s13 = np.sin(-Mot[3])
#sl14 = np.sin(Mot[3])
#s15 = np.sin(Mot[5])
#sl16 = np.sin(-Mot[5])
#s17 = np.sin(Mot[4])
#s18 = np.sin(-Mot[4])
#c7 = np.cos(Mot[0])
#c8 = np.cos(Mot[0])
#c9 = np.cos(-Mot[2])
#c10 = np.cos(Mot[2])
#c11 = np.cos(-Mot[1])
#cl12 = np.cos(-Mot[1])
#c13 = np.cos(-Mot[3])
#cl14 = np.cos(Mot[3])
#c15 = np.cos(-Mot[5])
#cl16 = np.cos(-Mot[5])
#c17 = np.cos(Mot[4])
#c18 = np.cos(-Mot[4])
#sabc = np.sin(-Mot[2]-Mot[3]+Mot[4])
#cabc = np.cos(-Mot[2]-Mot[3]+Mot[4])
#cab = np.cos(-Mot[2]-Mot[3])
#sab = np.sin(-Mot[2]-Mot[3])
#slabc = np.sin(Mot[2]+Mot[3]-Mot[4])
#clabc = np.cos(Mot[2]+Mot[3]-Mot[4])
#clab = np.cos(Mot[2]+Mot[3])
#slab = np.sin(Mot[2]+Mot[3])

r33 = -c11*sabc

Prx = Lf*(c11*s15*s7 - c15*(-c7*sabc - cabc*s11*s7)) - (-(L4*s9+L5*sab)*c7 + (L4*c9+L5*cab)*s7*s11)
Prz = Lf*(-c11*c15*cabc + s11*s15) - Lty - c11*(L4*c9+L5*cab)
Pry = Lf*(-c11*c7*s15 + c15*(-c7*cabc*s11 + s7*sabc)) + ((L4*s9+L5*sab)*s7-(L4*c9+L5*cab)*c7*s11)


Plx = Lf*(cl12*sl16*s8 - cl16*(-c8*slabc - clabc*sl12*s8)) - (-(L4*s10+L5*slab)*c8 + (L4*c10+L5*clab)*s8*sl12)
Plz = Lf*(-cl12*cl16*clabc + sl12*sl16) - Lty - cl12*(L4*c10+L5*clab)
Ply = Lf*(-cl12*c8*sl16 + cl16*(-c8*clabc*sl12 + s8*slabc)) + ((L4*s10+L5*slab)*s8-(L4*c10+L5*clab)*c8*sl12)

print("%f, \t%f"% ( Prx, Plx))
print("%f, \t%f"% ( Pry, Ply))
print("%f, \t%f, \t%f"% ( Prz, Plz, r33))


#[[c11*s15*s7 - c15*(-c7*sabc - cabc*s11*s7)
#  c11*c15*s7 - s15*(c7*sabc + cabc*s11*s7) c7*cabc - s11*s7*sabc
#  Lf*(c11*s15*s7 - c15*(-c7*sabc - cabc*s11*s7)) - Ltx - Py]
# [-c11*c15*cabc + s11*s15 c11*cabc*s15 + c15*s11 c11*sabc
#  Lf*(-c11*c15*cabc + s11*s15) - Lty - Pz]
# [-c11*c7*s15 + c15*(-c7*cabc*s11 + s7*sabc)
#  -c11*c15*c7 + s15*(c7*cabc*s11 - s7*sabc) c7*s11*sabc + cabc*s7
#  Lf*(-c11*c7*s15 + c15*(-c7*cabc*s11 + s7*sabc)) + Ltz + Px]


