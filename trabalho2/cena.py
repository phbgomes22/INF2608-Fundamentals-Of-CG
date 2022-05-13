from algebra import * 
import numpy as np
import matplotlib.pyplot as plt
import math

class Cena:
    def __init__(self,camera):
        self.camera = camera 

        img360 = self.camera.get_image()
        h, w = self.camera.get_resolution()
        self.color_buffer = np.zeros((h,w,3), dtype=np.float32)


    def show(self):
        print('Camera')
        self.camera.show()

    def pre_render(self):
        # vou fazer o render previamente de toda a imagem,
        # assim qualquer movimentacao da camera será fluida
        img360 = self.camera.get_image()
        hi, wi = img360.get_resolution()

        for y in range(hi):
            for x in range(wi):
                # pega origem e raio
                _, dir = self.camera.raio(wi - x,y)
                cor = img360.cor(dir)
                self.color_buffer[y,x,:]=cor/255.

        


    def render(self):
        img360 = self.camera.get_image()
        h, w = self.camera.get_resolution()
        '''
        _, dir = self.camera.raio(w - 0,0)
        ximg, yimg = img360.coords(dir)
        print(ximg, yimg)

        x_left =  ximg - int(w/2)
        x_right =  ximg + int(w/2)
        print(x_left, x_right)
        y_bottom = yimg -int(h/2)
        y_top = yimg + int(h/2)
        print(y_bottom, y_top)


        buffer = self.color_buffer[x_left:x_right,y_bottom:y_top,:]
        '''
        for y in range(h):
            for x in range(w):
                # pega origem e raio
                _, dir = self.camera.raio(w - x,y)

                cor = img360.cor(dir)
                self.color_buffer[y,x,:]=cor/255.
        
        

        return self.color_buffer


    def move_camera(self, at):
        self.camera.look_at(at)
        return self.render()
