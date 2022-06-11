import numpy as np
import matplotlib.pyplot as plt
from algebra import * 
import math

class Camera:
    """
    Objeto Câmera
    
    Parameters:
        fov (int): campo de visão
        width (int): largura da imagem em pixels
        height (int): altura da imagem em pixels

        near (float): plano de projeção, a partir de onde a câmera enxerga
        far (float): raio da esfera do ambiente, até onde a câmera enxerga

        eye (np.array): centro de projeção da câmera
        at (np.array): posição da visada (Alvo), define o eixo z da câmera
        up (np.array): direção pra cima

        img360(np.array): imagem 360 que define o "background" da camera
        
    Returns:
        Camera: instância do objeto câmera
    """
    def __init__(self,fov,width,height,near,far,eye,at,up, img360):
        self.fov = fov # fov geralmente recebido em graus
        self.width = width
        self.height = height
        self.near = near
        self.far = far
        
        self.eye = eye
        #self.at = at   # - desnecessário salvar
        self.up = up   # - desnecessário salvar
        
        self.img360 = img360

        ## parametros derivados

        self.altura = 2*near*math.tan(math.radians(fov/2.0))
        self.base = width*(self.altura/height)

        self.aspect = self.base/self.altura

        # at -> posição que a camera está olhando, define o eixo z
        self.ze = Vector3.unitary(at-eye)# unitário da direção at - eye
        vectorXe = Vector3.cross(self.ze, up)
        self.xe = Vector3.unitary(vectorXe)
        self.ye = Vector3.cross(self.ze, self.xe)

        T = Matrix4.translationMatrix(-eye[0], -eye[1], -eye[2])
        R = Matrix4.changeBasisMatrix(self.xe, self.ye, self.ze)
        self.lookat = R@T

        
        cot = 1/math.tan(math.radians(fov/2))
        aspect = height/width

        self.projection = np.array([
            [aspect*cot, 0,0,0],
            [0, cot, 0, 0],
            [0, 0, (far + near)/(far - near), -(far*near)/(far - near)],
            [0, 0, 1, 0]
        ])

    
    def showConfigurations(self):
        """
        Exibe as informações da Câmera
        """
        print('Camera: ')
        print(f'\tField of Vision = {self.fov}, Near = {self.near}, Far = {self.far}')
        print(f'\tWidth = {self.width}, Height = {self.height}, Aspect = {self.aspect}')
        print(f'\tEye={self.eye}')
        print(f'\tXe = {self.xe}, Ye = {self.ye}, Ze = {self.ze} ')
        self.img360.show()
        
    def get_resolution(self):
        return self.height, self.width

    def get_image_resolution(self):
        return self.img360.get_resolution()

    def get_image(self):
        return self.img360

    def raio(self,x,y):
        # retorna a origem de um raio
        # raio vai da origem (eye) até o plano. 
        # os raios tem tamanhos diferentes.
        #  
        # o_m (origem da imagem), é o ponto tocado pelo raio que segue near, menos as metades
        # para chegar na ponta esquerda superior

        dr = self.near*self.ze + self.altura*(y/self.height - 0.5)*self.ye + self.base*(x/self.width - 0.5)*self.xe

        return self.eye, dr
 
    def look_at(self, at):
        self.ze = Vector3.unitary(at-self.eye)# unitário da direção at - eye

        vectorXe = Vector3.cross(self.ze, self.up)
        self.xe = Vector3.unitary(vectorXe)

        self.ye = Vector3.cross(self.ze, self.xe)

    def to_canvas(self, xn, yn, zn):
        # x, y e z do canvas
        xc = int( (self.width - 1)*(xn+1)/2 )
        yc = int( (self.height - 1)*(yn+1)/2 )
        zc = int( 4294967295*(zn + 1)/2 )

        return xc, yc, zc
