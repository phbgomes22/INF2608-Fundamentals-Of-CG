import numpy as np
import math
from algebra import Vector3
import matplotlib.pyplot as plt


class Material:
    
    # Kd -> coeficiente difuso que diz quanto de cada cor o material tem
    # Ks -> coeficiente especular -> cor do brilho
    # Ke -> coeficiente de espelho, o quanto o material é espelhado
    def __init__(self, Kd, Ks, ns, textura=None, Ke=0):
        self.Kd = Kd
        self.Ks = Ks
        self.ns = ns
        self.Ke = Ke

        if textura is not None:
            self.textura = plt.imread(textura)/255.0
        else:
            self.textura = None
        
        
    def get_Kd(self, u, v):
        if self.textura is not None:
            h, w = self.textura.shape[:2]
            y = int(v*h)
            x = int(u*w)
            return self.textura[y,x]

        return self.Kd
    
    def get_Ks(self):
        return self.Ks
    
    def get_ns(self):
        return self.ns
        
    def get_Ke(self):
        return self.Ke

    def has_texture(self):
        return self.textura is not None