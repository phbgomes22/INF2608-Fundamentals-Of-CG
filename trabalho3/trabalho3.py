
#%%
from operator import truediv
import numpy as np
from algebra import *
from camera import *
import cena as cn
from img360 import *
from luz import *
from objetos import *
from material import *

# 01:20:16

## Criando camera

path = './'
img_name ='Sunset_Southside_Slopes_Pittsburgh_Equirectangular_Panoramic.jpg'
fname = path+img_name
img360 = Img360(fname)

eye = Vector3.create(40,100,40)
at = Vector3.create(0,0,0)
up = Vector3.create(0,0,1)

camera = Camera(90,600,600,30,230, eye, at, up, img360)


# - Instanciando cores

amarelo = Vector3.create(0.7,0.7,0.)
branco = Vector3.create(1,1,1)
azul = Vector3.create(0.3, 0.3, 1)


# criado o material da esfera e caixa
mat_caixa = Material(amarelo, branco, 40, None, 0.0)
mat_esfera = Material(azul, branco, 50, 'earth.jpg', 0.0)

## Criando esfera
centro = np.array(Vector3.create(0,20,0))
raio = 25.0
esfera = Esfera(centro, raio, mat_esfera)

esfera.show()

## Criando caixas

pmin1 = Vector3.create(-80.0, -50.0, -50.0)
pmax1 = Vector3.create(50.0, -45.0, 50.0)

caixa1 = Caixa(pmin1, pmax1, [mat_caixa]*6)

pmin2 = Vector3.create(-80.0, -50.0, -60.0)
pmax2 = Vector3.create(50.0, 50.0, -50.0)
caixa2 = Caixa(pmin2, pmax2, [mat_caixa]*6)

print("Caixa criada")

## Criando cena

posicao_luz = Vector3.create(100,40,40)
luz = Luz(posicao_luz, branco)

objetos_na_cena = []
objetos_na_cena.append(esfera)
#objetos_na_cena.append(caixa1)
# objetos_na_cena.append(caixa2)

cena = cn.Cena(camera, objetos_na_cena, [luz])


## Renderizando cena
 
buffer = cena.render()

print("Cena renderizada")


import matplotlib.pyplot as plt

plt.imshow(buffer)

plt.show()

