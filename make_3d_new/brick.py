from meshobjs import *
import math


class Brick(object):
    """
    this is the torus class
    """
    def __init__(self, cx, cy, cz, cells, y_size, x_size):
        self.loc = Vector(cx,cy,cz)
        self.cells = cells
        self.y_size = y_size
        self.x_size = x_size
        
    def z_bounds(self, y, x):
        cell = self.cells[y * self.x_size + x]
        return self.loc.z + cell.loc.z - cell.c * 0.5, self.loc.z + cell.loc.z + cell.c * 0.5 
    
    def get_distance(self,x,y,z):
        
        """
        distance function
        """
        # return d
        
        dx = x-self.loc.x
        dy = y-self.loc.y
        dz = z-self.loc.z
                
        indx = int(dx + self.x_size * 0.5)
        indy = int(dy + self.y_size * 0.5)
        
        # return max([abs(dx) - self.x_size * 0.5, abs(dy) - self.y_size * 0.5, abs(dz) - 25])
        
        if indx < 0 or indx > self.x_size - 1 or indy < 0 or indy > self.y_size - 1:
            
            xx = constrain(indx, 0, self.x_size - 1)
            yy = constrain(indy, 0, self.y_size - 1)
            
            bottom_z, top_z = self.z_bounds(yy, xx)
            
            xxx = constrain(dx, -self.x_size * 0.5, self.x_size * 0.5)
            yyy = constrain(dy, -self.y_size * 0.5, self.y_size * 0.5)
            
            diff1 = dist(dx, dy, dz, xxx, yyy, top_z)
            diff2 = dist(dx, dy, dz, xxx, yyy, bottom_z)

            return max([abs(dx) - self.x_size * 0.5, abs(dy) - self.y_size * 0.5, min(diff1, diff2)])
        
        else:
            
            bottom_z, top_z = self.z_bounds(indy, indx)
            return min(z - top_z, bottom_z - z)
