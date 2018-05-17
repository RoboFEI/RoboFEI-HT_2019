# coding: utf-8

import pandas as pd
import numpy as np

observacao = pd.DataFrame([
    ["L", 0.98, [3./4, 1./3]],
    ["base_gol", 0.98, [4./4, 2./3]],
    ["penalt_mark", 0.98, [2./4, 3./3]],
], columns = [
        "classes",
        "scores",
        "boxes",
    ]
)
observacao

# Landmark corner
lista = []
num = 1
pos = [
    [10.4, 0],
    [10.4, 7.4],
    [0, 7.4],
    [0, 0],
]
for horizonte in ["frente", "atrás"]:
    for vertical in ["esq", "dir"]:
        lista.append(["corner"+str(num), pos.pop(0), "corner", horizonte, vertical, 1.0/4])
        num += 1

# Landmark L
num = 1
pos = [
    [9.7, 0.7],
    [8.7, 1.2],
    [8.7, 6.2],
    [9.7, 6.7],
    [1.7, 1.2],
    [0.7, 0.7],
    [0.7, 6.7],
    [1.7, 6.2],
]
for horizonte in ["frente", "atrás"]:
    for vertical in ["esq", "dir"]:
        for __ in xrange(2):
            lista.append(["L"+str(num), pos.pop(0), "L", horizonte, vertical, 1.0/8])
            num += 1

# Landmark base_gol
num = 1
pos = [
    [9.7, 2.4],
    [9.7, 5.0],
    [0.7, 2.4],
    [0.7, 5.0],
]
for horizonte in ["frente", "atrás"]:
    for vertical in ["esq", "dir"]:
        lista.append(["base_gol"+str(num), pos.pop(0), "base_gol", horizonte, vertical, 1.0/4])
        num += 1

# Landmark T
num = 1
pos = [
    [9.7, 1.2],
    [9.7, 6.2],
    [5.2, 0.7],
    [5.2, 6.7],
    [0.7, 1.2],
    [0.7, 6.2],
]
for horizonte in ["frente", "meio", "atrás"]:
    for vertical in ["esq", "dir"]:
        lista.append(["T"+str(num), pos.pop(0), "T", horizonte, vertical, 1.0/6])
        num += 1

# Landmark X
num = 1
pos = [
    [5.2, 2.95],
    [5.2, 4.45],
]
for vertical in ["esq", "dir"]:
    lista.append(["X"+str(num), pos.pop(0), "X", "meio", vertical, 1.0/2])
    num += 1

# Landmark penalt_mark
num = 1
pos = [
    [7.6, 10.4],
    [2.8, 10.4],
]
for horizonte in ["frente", "atrás"]:
    lista.append(["penalt_mark"+str(num), pos.pop(0), "penalt_mark", horizonte, "meio", 1.0/2])
    num += 1

lista.append(["centro", [5.2, 3.7], "centro", "meio", "meio", 1.0/2])
lista = pd.DataFrame(lista, columns = ["tag", "pos", "classes", "vertical", "horizontal", "propabilidade"])
lista

lista.loc[lista.vertical == "frente","propabilidade"] *= 1.1
lista.loc[lista.vertical == "atrás","propabilidade"] *= 0.9

# lista.loc[lista.horizontal == "esq","propabilidade"] *= 1.1
# lista.loc[lista.horizontal == "dir","propabilidade"] *= 0.9

lista

condition = 0
for i, __, __ in observacao.drop_duplicates(["classes"]).values:
    condition |= lista.classes == i
lista = lista[condition]
lista = lista.reset_index()
lista

x = 0
y = 1

for i in xrange(len(observacao)-1):
    for j in xrange(i+1,len(observacao)):
        print "Dado:"
        print observacao.classes[i], "-",observacao.classes[j], ":",
        print observacao.boxes[i][0] - observacao.boxes[j][0], ",", 
        print observacao.boxes[i][1] - observacao.boxes[j][1]
        print "Teste:"
        for k in xrange(len(lista)-1):
            for l in xrange(k+1,len(lista)):
                if observacao.classes[i] == lista.classes[k] and observacao.classes[j] == lista.classes[l]:
                    print lista.classes[k], "-",lista.classes[l], ":",
                    print lista.pos[k][0] - lista.pos[l][0], ",", 
                    print lista.pos[k][1] - lista.pos[l][1]
                    if (observacao.boxes[i][0] - observacao.boxes[j][0]) * (lista.pos[k][0] - lista.pos[l][0]) >= 0 and (observacao.boxes[i][1] - observacao.boxes[j][1]) * (lista.pos[k][1] - lista.pos[l][1]) >= 0:
                        print "Aumentou"
                        lista.loc[k, "propabilidade"] *= 1.3
                        lista.loc[l, "propabilidade"] *= 1.3
                    else:
                        print "Abaixou"
                        lista.loc[k, "propabilidade"] *= 0.7
                        lista.loc[l, "propabilidade"] *= 0.7
                        
        print "\n"
lista

lista.sort_values(["propabilidade"], ascending=False)