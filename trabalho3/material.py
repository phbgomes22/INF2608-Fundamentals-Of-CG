import numpy as np
import math
from algebra import Vector3


class Material:
    
    # Kd -> coeficiente difuso que diz quanto de cada cor o material tem
    # Ks -> coeficiente especular -> cor do brilho
    # Ke -> coeficiente de espelho, o quanto o material é espelhado
    def __init__(self, Kd, Ks, ns, textura=None, Ke=0):
        self.Kd = Kd
        self.Ks = Ks
        self.ns = ns
        self.textura = textura
        self.Ke = Ke
        
        
    def get_Kd(self):
        return self.Kd
    
    def get_Ks(self):
        return self.Ks
    
    def get_ns(self):
        return self.ns
        
    def get_Ke(self):
        return self.Ke