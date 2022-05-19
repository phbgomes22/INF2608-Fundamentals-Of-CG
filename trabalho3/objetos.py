import numpy as np
import math
from algebra import Vector3
import sys
from material import *

TOL = sys.float_info.epsilon


class Objeto:
    def __init__(self):
        pass

    def get_uv(self, pi):
        return 0,0

class Triangulo(Objeto):
    
    # três vertices
    # e o material
    def __init__(self, v0, v1, v2, material):
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.material = material
        
    def show(self):
        print(f'Triangulo: {self.v0}, {self.v1}, {self.v2}')
        self.material.show()
        
    def intercepta(self, origem, direcao):
        
        a01 = self.v1 - self.v0
        a02 = self.v2 - self.v0
        normal = Vector3.unitary(Vector3.cross(a01, a02))
        
        if Vector3.dot(direcao,normal) > +TOL:
            return np.nan, self, Vector3.create(0,0,0)
        
        A = np.zeros((3,3), dtype=np.float64)
        
        A[:,0] = -direcao
        A[:,1] = a01
        A[:,2] = a02
        
        b = origem - self.v0
        
        x = np.linalg.solve(A,b)
        
        ti, L1, L2 = x[:]

        L0 = 1 - L1 - L2

        if L0 < 0 or L0 > 1 or L1 < 0 or L1 > 1 or L2 < 0 or L2 > 1:
            return np.nan, self, Vector3.create(0,0,0)
        
        self.L1 = L1
        self.L2 = L2
        self.normal = normal
        return ti, self, normal
    
    
    def normal(self, ponto):
        return self.normal
    
    
    def get_material(self):
        return self.material

    
    def has_texture(self):
        return self.material.has_texture()



class Caixa(Objeto):
    def __init__(self,pmin,pmax,materiais):
        self.pmin = pmin
        self.pmax = pmax
        self.materiais = materiais
        self.material = materiais[0]
        
        xm, xM, ym, yM, zm, zM  = pmin[0], pmax[0], pmin[1], pmax[1], pmin[2], pmax[2]

        v0 = Vector3.create(xm, ym, zm)
        v1 = Vector3.create(xM, ym, zm)
        v2 = Vector3.create(xM, yM, zm)
        v3 = Vector3.create(xm, yM, zm)
        v4 = Vector3.create(xm, ym, zM)
        v5 = Vector3.create(xM, ym, zM)
        v6 = Vector3.create(xM, yM, zM)
        v7 = Vector3.create(xm, yM, zM )

        text0 = np.array([0., 0.])
        text1 = np.array([])
        #tex

        t0 = Triangulo(v0, v2, v1, materiais[0]) #, text0, text1, text2)
        t2 = Triangulo(v0, v1, v5, materiais[0])
        t3 = Triangulo(v0, v5, v4, materiais[1])
        t1 = Triangulo(v0, v3, v2, materiais[1])
        t4 = Triangulo(v1, v2, v6, materiais[2])
        t5 = Triangulo(v1, v6, v5, materiais[2])
        t6 = Triangulo(v2, v7, v6, materiais[3])
        t7 = Triangulo(v2, v3, v7, materiais[3])
        t8 = Triangulo(v3, v4, v7, materiais[4])
        t9 = Triangulo(v3, v0, v4, materiais[4])
        t10 = Triangulo(v4, v5, v6, materiais[5])
        t11 = Triangulo(v4, v6, v7, materiais[5])

        self.triangulos = [t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11]


    def intercepta(self, origem, direcao):
        for triangulo in self.triangulos:
            tx, objx, nx = triangulo.intercepta(origem, direcao)
            if ~np.isnan(tx):
                self.material = triangulo.get_material()
                return tx, objx, nx
        return np.nan, self, Vector3.create(0,0,0)

    def get_material(self):
        return self.material

    
    def has_texture(self):
        return self.material.has_texture()



class Esfera:
    
    # material é 
    def __init__(self,centro,raio, material):
        self.centro = centro
        self.raio = raio
        self.material = material
        
    def show(self): 
        print(f'Esfera: origem:{self.centro}, raio:{self.raio}')
        
        
    # origem e direcao sao vetores, e definem o raio
    def intercepta(self, origem, direcao):
        # a = d.d
        a = Vector3.dot(direcao, direcao)
        
        # b = 2d . (o - c)
        b = Vector3.dot(2*direcao, origem-self.centro)
        
        # (o - c) . (o - c) - r^2
        c = Vector3.dot(origem-self.centro, origem-self.centro) - self.raio**2
        
        # delta
        delta = b**2 - 4*a*c
        
        if delta > TOL:
            t1 = ( -b - math.sqrt(delta) ) / (2*a)
            
            t2 = ( -b + math.sqrt(delta) ) / (2*a)
            
            tmin = min(t1,t2)
            
            if tmin > TOL:
              

                return tmin, self, Vector3.unitary(origem + tmin*direcao - self.centro)
            else:
                return np.nan, self, Vector3.create(0,0,0)
        
        return np.nan, self, Vector3.create(0,0,0)
        
    def get_uv(self, pi):
        pi -= self.centro
        x, y, z = pi
        phi = math.atan2(y,x) 

        dist_orig = math.sqrt(x*x+ y*y)
        theta = math.atan2(dist_orig, z)

        u = (1+phi/math.pi)/2.0
        v = theta/math.pi
        return u, v

    # calcula a normal
    def normal(self, ponto):
        return Vector3.unitary(ponto-self.centro)
    
    
    def cor(self):
        Kd = self.material.get_Kd()
        return Kd
    
    def get_material(self):
        return self.material
    
    def has_texture(self):
        return self.material.has_texture()
    

    
    
class Plano(Objeto):
    def __init__(self,n,d, material):
        self.n = Vector3.unitary(n)
        self.d = d
        self.material = material
        
    def show(self):
        print(self.n, self.d)
        
    def get_n(self):
        return self.n
    
    def get_d(self):
        return self.d
    
    def get_pp(self):
        return -self.d*self.n
    
    def get_material(self):
        return self.material

    def has_texture(self):
        return self.material.has_texture()
    
    
    
    
class PoliConvexo(Objeto):
    
    def __init__(self, planos):
        self.planos = planos
        self.plano_x = None # plano interceptado
         
    def show(self):
        print("PoliConvexo")
        for p in self.planos:
            p.show()
            
    def intercepta(self, ori, dir):
        te = 0.0 # entrada
        ts = np.inf #saída
        
        for plano in self.planos:
            n = plano.get_n()
            pp = plano.get_pp()
            
            den = Vector3.dot(dir, n)
            num = Vector3.dot(pp-ori,n)
            
            if den > TOL:
                ts = min(num/den,ts)
            elif den < -TOL:
                t = num/den
                if t>te:
                    te = t
                    self.plano_x = plano
            elif num < 0:
                te = np.nan
                break
            
            if ts<te:
                te = np.nan
                break
                
        return te, self, self.plano_x.get_n()
    
    
    def get_material(self):
        return self.plano_x.get_material()

    
    def has_texture(self):
        return self.plano_x.has_texture()
        
    

class Cubo(PoliConvexo):
    def __init__(self,pmin,pmax,materiais):
        self.pmin = pmin
        self.pmax = pmax
        self.materiais = materiais
        
        pps = [pmin, pmin, pmin, pmax, pmax, pmax]
        ns = [ Vector3.create(-1,0,0), Vector3.create(0,-1,0), Vector3.create(0,0,-1),
               Vector3.create(1,0,0), Vector3.create(0,1,0), Vector3.create(0,0,1)]
        
        
        planos = []
        for i in range(6):
            d = -Vector3.dot(ns[i], pps[i])
            plano = Plano(ns[i],d,materiais[i])
            
            planos.append(plano)
            
        PoliConvexo.__init__(self, planos)
        
        
    
    def cor(self):
        material = self.get_material()
        Kd = material.get_Kd()
        return Kd
    