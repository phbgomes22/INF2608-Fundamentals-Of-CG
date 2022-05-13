# FCG22 - T2 Gattass
import numpy as np
from algebra import *
import matplotlib.pyplot as plt
from camera import Camera
from img360 import Img360
from cena import *
import math
import plotly as py
import plotly.express as px
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets


path = './img360/'
img_name ='Sunset_Southside_Slopes_Pittsburgh_Equirectangular_Panoramic.jpg'
fname = path+img_name
img360 = Img360(fname)

eye = Vector3.create(0,0,0)
at = Vector3.create(0,1,0)
up = Vector3.create(0,0,1)

camera = Camera(60,800,600,1,10, eye, at, up, img360)

cena = Cena(camera)


def plot_func(freq):
    y_ax = 1
    x_ax = 1
    if freq >= -math.pi/2.0 and freq <= 0.0: # ok
        x_ax = -math.tan(freq)
    elif freq > 0.0 and freq <= math.pi/2.0: # ok
        y_ax = 1 
        x_ax = -math.tan(freq)
    elif freq > math.pi/2.0 and freq <= math.pi: # ok
        y_ax = -1
        x_ax = math.tan(freq)
    else:   # 
        y_ax = -1
        x_ax = math.tan(freq)
    new_at = Vector3.create(x_ax,y_ax,0)
    cena.move_camera(new_at)
    img_render = cena.render()
    plt.imshow(img_render)

interact(plot_func, freq = widgets.FloatSlider(value=0.0,
                                               min=-math.pi,
                                               max=math.pi,
                                               step=0.2))