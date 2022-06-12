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
        far = self.camera.get_far()

        self.color_buffer = np.zeros((h,w,3), dtype=np.float32)
        max_int = np.iinfo(np.uint32).max
        self.z_buffer = max_int*np.ones((h,w, 3), dtype=np.int32)


    def show(self):
        print('Camera')
        self.camera.show()
        print("Objetos")
        for obj in self.objetos:
            obj.show()
        print("Luzes")
        for luz in self.luzes:
            luz.show()

            
    def glrender(self):
        lookat = self.camera.get_lookat()
        projection = self.camera.get_projection()
        view = self.camera.get_view()

        buffer = plt.imread('fig1.png')/255.
        plt.imshow(buffer)
        plt.show()
        return
        for obj in self.objetos:
            triangles = obj.get_triangles()
            for triangle in triangles:
                vs = triangle.get_vertices()
                ve = np.dot(vs, lookat.T)
                vp = np.dot(ve, projection.T)

                vpp = np.zeros((3,4))
                for i in range(3):
                    vpp[i] = vp[i]/vp[i,3]

                vc = np.dot(vpp, view.T)

                for i in range(3):
                    xi = int(vc[i,0])
                    yi = int(vc[i,1])
                    buffer[yi, xi, 0] = 1.0
                    buffer[yi, xi, 1] = 0.0
                    buffer[yi, xi, 2] = 0.0

        plt.imshow(buffer)
        plt.show()


    def render(self):

        h, w = self.camera.get_resolution()
 
        for y in range(h):
            for x in range(w):
                # pega origem e raio
                ori, dir = self.camera.raio(x,y)
                
                cor = self.trace(None, ori, dir)
                self.color_buffer[y,x,:] = np.clip(cor, 0, 1)
        
        return self.color_buffer
    
    
    
    def trace(self, obj_ori, ori, dir):
        ti = np.inf
        obji = None
        # vetor normal
        ni = Vector3.create(0,0,0)
        # rodo todos os objetos
        for obj in self.objetos:
            if obj_ori == obj:
                continue
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
    
    
    def is_in_shadow(self, obi, ori, dir):
        for obj in self.objetos:
            if obj is not obi:
                tx, objx, nx = obj.intercepta(ori, dir)
                if tx > 0.0001 and tx < 1.0:
                    return True
        
        return False

    
    def shade(self, obj, dir, pi, ni):

        material = obj.get_material()

        u = 0
        v = 0
        if obj.has_texture():
            u, v = obj.get_uv(pi)
        kd = material.get_Kd(u, v)
        ks = material.get_Ks()
        ns = material.get_ns()
        ke = material.get_Ke()
        
        cor = 0.05*kd
        
        dir_eye = - Vector3.unitary(dir)
        refl = Vector3.reflect(dir_eye, ni) # r
        
        # direcao da luz
        for luz in self.luzes:

            pi2luz = luz.get_posicao() - pi

            if self.is_in_shadow(obj, pi, pi2luz):
                continue
            
            dir_luz = Vector3.unitary(pi2luz) # L
            val_luz = luz.get_intensidade() # RGB
            
            val_luz_amb = 0.1*val_luz
            cor += val_luz_amb*kd
            
            cos_teta = Vector3.dot(ni,dir_luz)
            
            if cos_teta >= 0:
                cor += val_luz*kd*cos_teta 
                cos_alfa = Vector3.dot(dir_luz, refl)
                
                if cos_alfa > 0: # and cos_alfa <= 1:
                    cor += val_luz*ks*(cos_alfa**ns)
        
        if ke > 0:
                cor_esp = self.trace(obj, pi, refl)
                cor_final = ke*cor_esp + (1-ke)*cor
        else:
            cor_final = cor
            
        return cor_final
 
        
    def get_color_render(self):
        return

    def move_camera(self, at):
        self.camera.look_at(at)
        return self.render()

