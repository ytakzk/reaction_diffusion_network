from meshobjs import *
import math

class RDNBox(object):
    """
    this is the box class
    """
    def __init__(self, cx=0, cy=0, cz=0, a=1, b=1, c=1):
        self.loc = Vector(cx,cy,cz)
        self.a = a
        self.b = b
        self.c = c
        
    def get_mesh(self):
        m = Mesh()
        
        ha = self.a/2.0
        hb = self.b/2.0
        hc = self.c/2.0
        nodes = []
        nodes.append(Node(-ha,-hb,-hc))
        nodes.append(Node( ha,-hb,-hc))
        nodes.append(Node( ha, hb,-hc))
        nodes.append(Node(-ha, hb,-hc))
        nodes.append(Node(-ha,-hb, hc))
        nodes.append(Node( ha,-hb, hc))
        nodes.append(Node( ha, hb, hc))
        nodes.append(Node(-ha, hb, hc))
        
        for i in range(len(nodes)):
            vadd = nodes[i].addition(self.loc)
            nodes[i] = Node(vadd.x, vadd.y, vadd.z)
        
        m.add_face(Face([nodes[3],nodes[2],nodes[1],nodes[0]]))
        m.add_face(Face([nodes[4],nodes[5],nodes[6],nodes[7]]))
        m.add_face(Face([nodes[0],nodes[1],nodes[5],nodes[4]]))
        m.add_face(Face([nodes[2],nodes[3],nodes[7],nodes[6]]))
        m.add_face(Face([nodes[1],nodes[2],nodes[6],nodes[5]]))
        m.add_face(Face([nodes[4],nodes[7],nodes[3],nodes[0]]))
        return m
    
    def get_distance(self,x,y,z):
        """
        distance function
        """
        dx = abs(x-self.loc.x)-self.a/2.0
        dy = abs(y-self.loc.y)-self.b/2.0
        dz = abs(z-self.loc.z)-self.c/2.0
        d = max([dx,dy,dz])
        
        return d
    
    def get_bounds(self):
        return (self.loc.x-self.a/2.0, self.loc.y-self.b/2.0, self.loc.z-self.c/2.0,
                self.loc.x+self.a/2.0, self.loc.y+self.b/2.0, self.loc.z+self.c/2.0)
        
    def draw(self):
        pushMatrix()
        translate(self.loc.x, self.loc.y, self.loc.z)
        box(self.a, self.b, self.c)
        popMatrix()
