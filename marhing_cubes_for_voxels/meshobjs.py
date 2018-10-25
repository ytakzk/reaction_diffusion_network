import math

class Vector(object):
    """
    this is the class for all the vector math.
    """
    def __init__(self,x=0,y=0,z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def cross_product(self, other):
        xc = self.y*other.z - self.z*other.y
        yc = self.z*other.x - self.x*other.z
        zc = self.x*other.y - self.y*other.x
        return Vector(xc,yc,zc)

    def addition(self, other):
        return Vector(self.x+other.x, self.y+other.y, self.z+other.z)
        
    def subtract(self, other):
        return Vector(self.x-other.x, self.y-other.y, self.z-other.z)

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def normalized(self):
        nmag = self.magnitude()
        return Vector(self.x/nmag, self.y/nmag, self.z/nmag)
    
    def multiply(self, f):
        return Vector(self.x*f, self.y*f, self.z*f)

class Node(Vector):
    """
    this is the node class.
    """
    def __init__(self,x=0,y=0,z=0):
        super(Node, self).__init__(x,y,z)
        self.id = -1
        
    def __repr__(self):
        return "Node at {} {} {}".format(self.x,self.y,self.z)

class Face(object):
    """
    this is our face class.
    """
    def __init__(self, nodes=[]):
        self.nodes = nodes
        
    def add_node(self, n):
        self.nodes.append(n)
        
    def get_centroid(self):
        num = len(self.nodes)
        # xlist = []
        # for n in self.nodes:
        #     xlist.append(n.x)    
        # avx = sum(xlist)/num
        avx = sum([n.x for n in self.nodes])/num
        avy = sum([n.y for n in self.nodes])/num
        avz = sum([n.z for n in self.nodes])/num
        return Node(avx,avy,avz)
    
    def get_normal_of_length(self, l):
        fn = self.get_normal()
        unit_normal = fn.normalized()
        lennorm = unit_normal.multiply(l)
        return lennorm
    
    def get_normal(self):
        e1 = self.nodes[1].subtract(self.nodes[0])
        e2 = self.nodes[-1].subtract(self.nodes[0])
        face_normal = e1.cross_product(e2)
        return face_normal
    
    def get_funky_point(self):
        cn = self.get_centroid()
        betw = cn.subtract(self.nodes[0])
        betw = betw.multiply(0.8)
        return self.nodes[0].addition(betw)
    
class Mesh(object):
    """
    this is our brandnew mesh class.
    """
    def __init__(self):
        self.nodes = []
        self.faces = []
        
    def add_face(self, f):
        self.faces.append(f)
        
    def add_faces(self, facelist):
        self.faces.extend(facelist)
        
    def add_node(self, n):
        self.nodes.append(n)
        n.id = len(self.nodes)
        
    def collect_nodes(self):
        for n in self.nodes:
            n.id = -1
        self.nodes = []
        for f in self.faces:
            for n in f.nodes:
                if n.id < 0:
                    self.nodes.append(n)
                    n.id = len(self.nodes)
