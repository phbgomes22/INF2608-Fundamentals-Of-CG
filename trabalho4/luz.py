import numpy as np
import math
from algebra import Vector3



class Luz:
    
    def __init__(self,posicao,intensidade):
        self.posicao = posicao
        self.intensidade = intensidade
        
    def show(self):
        print(f'Luz: posicao:{self.posicao}, intensidade:{self.itnensidade}')
        
        
    def get_posicao(self):
        return self.posicao
    
    def get_intensidade(self):
        return self.intensidade
    
    