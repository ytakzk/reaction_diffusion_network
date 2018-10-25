from meshobjs import *
import math


class Sphere(object):
    """
    this is the sphere class
    """
    def __init__(self, cx=0, cy=0, cz=0, rad=1):
        self.loc = Vector(cx,cy,cz)
        self.r = rad
    
    def get_distance(self,x,y,z):
        """
        distance function
        """
        # long version
        d = math.sqrt((x-self.loc.x)**2 + (y-self.loc.y)**2 + (z-self.loc.z)**2) - self.r
        
        return d
