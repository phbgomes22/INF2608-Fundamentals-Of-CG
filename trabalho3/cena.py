from algebra import * 
import numpy as np
import matplotlib.pyplot as plt
import math
from objetos import *
from luz import *

class Cena:
    def __init__(self,camera, objetos, luzes):
        self.camera = camera 
        self.objetos = objetos
        self.luzes = luzes

        img360 = self.camera.get_image()
        h, w = self.camera.get_resolution()
        self.color_buffer = np.zeros((h,w,3), dtype=np.float32)


    def show(self):
        print('Camera')
        self.camera.show()
        print("Objetos")
        for obj in self.objetos:
            obj.show()
        print("Luzes")
        for luz in luzes:
            luz.show()

            
    def render(self):
        
        h, w = self.camera.get_resolution()
 
        for y in range(h):
            for x in range(w):
                # pega origem e raio
                ori, dir = self.camera.raio(x,y)
                
                cor = self.trace(ori, dir)
                self.color_buffer[y,x,:] = np.clip(cor, 0, 1)
        
        return self.color_buffer
    
    
    
    def trace(self, ori, dir):
        ti = np.inf
        obji = None
        # vetor normal
        ni = Vector3.create(0,0,0)
        # rodo todos os objetos
        for obj in self.objetos:
            tx, objx, nx = obj.intercepta(ori, dir)

            if ~np.isnan(tx):
                # vendo qual objeto tem o menor t,
                # isto é, qual a interseção
                # mais próxima
                if tx < ti:
                    ti = tx
                    obji = objx
                    ni = nx
                    
        if obji is not None:
            # ponto de intersecao
            # pi(t) = ori + ti*dir
            pi = ori + ti*dir
            # passa o objeto, ponto pi e a normal
            cor = self.shade(obji, dir, pi, ni)
            
        # se nenhum objeto faz interseção
        else:
            img360 = self.camera.get_image()
            # pego a cor da imagem do fundo
            cor = img360.cor(dir)
            
        return cor
    
    
    
    def shade(self, obj, dir, pi, nx):
        material = obj.get_material()
        kd = material.get_Kd()
        ks = material.get_Ks()
        ns = material.get_ns()
        ke = material.get_Ke()
        
        cor = 0.05*kd
        
        dir_eye = - Vector3.unitary(dir)
        refl = Vector3.reflect(dir_eye, nx) # r
        
        # direcao da luz
        for luz in self.luzes:
            
            luz_p = luz.get_posicao() - pi
            dir_luz = Vector3.unitary(luz_p) # L
            val_luz = luz.get_intensidade() # RGB
            
            val_luz_amb = 0.1*val_luz
            cor += val_luz_amb*kd
            
            cos_teta = Vector3.dot(nx,dir_luz)
            
            if cos_teta > 0:
                cor += val_luz*kd*cos_teta 
                cos_alfa = Vector3.dot(dir_luz, refl)
                
                if cos_alfa > 0:
                    cor += val_luz*ks*(cos_alfa**ns)
        
        if ke > 0:
            cor_esp = self.trace(pi, refl)
            cor_final = ke*cor_esp + (1-ke)*cor
        else:
            cor_final = cor
            
        return cor_final
 
        

    def move_camera(self, at):
        self.camera.look_at(at)
        return self.render()

