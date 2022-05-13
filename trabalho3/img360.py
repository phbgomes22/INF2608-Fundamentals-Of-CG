import matplotlib.pyplot as plt
from algebra import * 
import math


class Img360:
    def __init__(self, filename):
        self.filename = filename
        self.img360 = plt.imread(filename)/255.
        self.height = self.img360.shape[0]
        self.width = self.img360.shape[1]
        self.dcolor = self.img360.shape[2]

    def show(self):
        plt.imshow(self.img360)
        plt.show()

    def get_resolution(self):
        return self.height, self.width


    def coords(self, dir):
        # tan(phi) = y/x
        # phi = arc_tan(y/x)
        phi = math.atan2(dir[1],dir[0]) 

        dist_orig = math.sqrt(dir[1]*dir[1] + dir[0]*dir[0])
        theta = math.atan2(dist_orig, dir[2])

        u = (1+phi/math.pi)/2.0
        v = theta/math.pi

        ximg = int(u*(self.width - 1))
        yimg = int(v*(self.height - 1))

        return ximg, yimg
        
    # dir = (x, y, z)
    def cor(self, dir):

        ximg, yimg = self.coords(dir)
        return self.img360[yimg, ximg, :]


