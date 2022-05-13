import numpy as np
import math
import sys 

TOL = sys.float_info.epsilon

class Vector3:
    """
    Funções algébricas com vetores [x, y, z]
    """
    @staticmethod
    def create(x, y, z):
        """
        Dadas três coordenadas, cria um vetor XYZ

        Parameters:
            x (float): Coordenada X
            y (float): Coordenada Y
            z (float): Coordenada Z

        Returns:
            np.array: Vetor XYZ
        """
        return np.array([x,y,z], dtype=np.float64)
    
    def toCartesian(vector4):
        """
        Torna um Vector 4 em um Vetor Cartesiano

        Parameters:
            vector4 (np.array): Vetor XYZW

        Returns:
            np.array: Vetor XYZ
        """
        if vector4[3]>TOL:
            return Vector3.create(vector4[0]/vector4[3],vector4[1]/vector4[3],vector4[2]/vector4[3])
        else:
            return None
    
    @staticmethod
    def angle(u, v):
        """
        Calcula o ângulo entre dois vetores

        Parameters:
            u (np.array): Vetor 1
            v (np.array): Vetor 2

        Returns:
            float: Ângulo entre os dois vetores 
        """  
        num = Vector3.dot(u,v)
        den = Vector3.norm(u)*Vector3.norm(v)
        
        return np.arccos(num/den) * 180/np.pi if den>TOL else 0
    
    @staticmethod
    def norm(v):
        """
        Calcula a norma de um vetor

        Parameters:
            v (np.array): Vetor

        Returns:
            float: Norma de um vetor
        """
        #return sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2])
        return np.linalg.norm(v)
    
    @staticmethod
    def unitary(v):
        """
        Calcula a vetor unitário de um vetor

        Parameters:
            v (np.array): Vetor

        Returns:
            np.array: Vetor unitário de um vetor
        """
        s = Vector3.norm(v)
        if( s > TOL):
            return v/s
        else:
            return None
    
    @staticmethod
    def dot(u, v):
        """
        Calcula o produto entre dois vetores

        Parameters:
            u (np.array): Vetor 1
            v (np.array): Vetor 2

        Returns:
            float: Produto entre os dois vetores 
        """
        #return u[0]*v[0]+u[1]*v[1]+u[2]*v[2]
        return np.dot(u, v)
    
    @staticmethod
    def reflect(v, n):
        """
        Calcula o vetor refratado

        Parameters:
            v (np.array): Vetor
            n (np.array): Normal

        Returns:
            np.array: Vetor refratado
        """
        r = 2*Vector3.dot(v,n)*n-v
        return r
    
    @staticmethod
    def cross(u, v):
        """
        Calcula o produto cruzado entre dois vetores

        Parameters:
            u (np.array): Vetor 1
            v (np.array): Vetor 2

        Returns:
            np.array: Produto Cruzado entre os dois vetores 
        """
        return np.cross(u, v)

class Vector4:
    """
    Funções Algébricas com Vetores [x, y, z, z]
    """
    @staticmethod
    def create(x, y, z, w):
        """
        Dado quatro coordenadas, cria um vetor XYZW

        Parameters:
            x (float): Coordenada X
            y (float): Coordenada Y
            z (float): Coordenada Z
            w (float): Coordenada Homogênea
        Returns:
            np.array: Vetor XYZW
        """
        return np.array([x,y,z, w], dtype=float)
    
    @staticmethod
    def toVector4(vector3, w = 1):
        """
        Dado um Vector 3 e um W, cria um vetor XYZW

        Parameters:
            vector3 (np.array): Vector3
            w (float): Coordenada Homogênea
        Returns:
            np.array: Vetor XYZW
        """
        return Vector4.create(vector3[0], vector3[1], vector3[2], w)

class Matrix4:
    """
    Funções Algébricas com Matrizes 4x4
    """
    @staticmethod
    def identity():
        """
        Retorna uma matriz Identidade

        Returns:
            np.array: Matriz indentidade
        """
        return np.eye(4,dtype=np.float64)

    @staticmethod
    def translationMatrix(tx,ty,tz):
        """
        Retorna uma matriz de translação

        Parameters:
            tx (float): Coordenada X
            ty (float): Coordenada Y
            tz (float): Coordenada Z
        Returns:
            np.array: Matriz de translação
        """
        T = Matrix4.identity()

        T[0,3]=tx
        T[1,3]=ty
        T[2,3]=tz

        return T

    @staticmethod
    def scaleMatrix(sx,sy,sz):
        """
        Retorna uma matriz de escala

        Parameters:
            sx (float): Escala em X
            sy (float): Escala em Y
            sz (float): Escala em Z
        Returns:
            np.array: Matriz de escala
        """
        S = Matrix4.identity()

        S[0,0]=sx
        S[1,1]=sy
        S[2,2]=sz

        return S

    @staticmethod
    def rotationMatrix(ang, ex,ey,ez):
        """
        Retorna uma matriz de rotação

        Parameters:
            ang (float): AnguloS
            ex (float): Eixo em X
            ey (float): Eixo em Y
            ez (float): Eixo em Z
        Returns:
            np.array: Matriz de rotação
        """
        size = math.sqrt(ex*ex+ey*ey+ez*ez)
        R = Matrix4.identity()
        if size>TOL:
            ang = math.radians(ang)
            sin_a = math.sin(ang)
            cos_a = math.cos(ang)
            ex /= size
            ey /= size
            ez /= size
            R[0,0]  = cos_a + (1 - cos_a)*ex*ex    #Linha 1
            R[0,1]  = ex*ey*(1 - cos_a) - ez*sin_a
            R[0,2]  = ez*ex*(1 - cos_a) + ey*sin_a

            R[1,0]  = ex*ey*(1 - cos_a) + ez*sin_a
            R[1,1]  = cos_a + (1 - cos_a)*ey*ey
            R[1,2]  = ey*ez*(1 - cos_a) - ex*sin_a

            R[2,0]  = ex*ez*(1 - cos_a) - ey*sin_a
            R[2,1]  = ey*ez*(1 - cos_a) + ex*sin_a
            R[2,2] = cos_a + (1 - cos_a)*ez*ez
        
        return R

    @staticmethod
    def changeBasisMatrix(xe, ye, ze):
        """
        Retorna uma matriz com uma nova base

        Parameters:
            xe (float): Coordenada X
            ye (float): Coordenada Y
            ze (float): Coordenada Z
        Returns:
            np.array: Matriz
        """
        R = Matrix4.identity()
        R[0,:3] = xe 
        R[1,:3] = ye
        R[2,:3] = ze
        return R

    @staticmethod
    def transf4x3(M,v):
        """
        Aplica uma tranformação em um vetor

        Parameters:
            M (np.array): Matriz
            v (np.array): Vector
        Returns:
            np.array: Vector3
        """
        x = M[0,0]*v[0]+M[0,1]*v[1]+M[0,2]*v[2]+M[0,3]
        y = M[1,0]*v[0]+M[1,1]*v[1]+M[1,2]*v[2]+M[1,3]
        z = M[2,0]*v[0]+M[2,1]*v[1]+M[2,2]*v[2]+M[2,3]
        return Vector3.create(x,y,z)
