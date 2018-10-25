from meshobjs import *
import math

class Box(object):
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

class RBox(object):
    """
    this is the box class
    """
    def __init__(self, cx=0, cy=0, cz=0, a=1, b=1, c=1, r=0):
        self.loc = Vector(cx,cy,cz)
        self.a = a
        self.b = b
        self.c = c
        self.r = r
        
    def get_distance(self,x,y,z):
        """
        distance function
        """
        dx = abs(x-self.loc.x)-(self.a/2.0-self.r)
        dy = abs(y-self.loc.y)-(self.b/2.0-self.r)
        dz = abs(z-self.loc.z)-(self.c/2.0-self.r)
        inside = max([dx,dy,dz])-self.r
        dx = max(dx,0)
        dy = max(dy,0)
        dz = max(dz,0)
        if inside+self.r>0:
            #rounded corner case
            return math.sqrt(dx**2 + dy**2 + dz**2) - self.r 
        else:
            return inside
        
    def get_bounds(self):
        return (self.loc.x-self.a/2.0, self.loc.y-self.b/2.0, self.loc.z-self.c/2.0,
                self.loc.x+self.a/2.0, self.loc.y+self.b/2.0, self.loc.z+self.c/2.0)

class Sphere(object):
    """
    this is the sphere class
    """
    def __init__(self, cx=0, cy=0, cz=0, rad=1):
        self.loc = Vector(cx,cy,cz)
        self.r = rad
        
    def get_mesh(self, n1=10, n2=20):
        m = Mesh()
        
        np = Node(0,0,self.r)
        sp = Node(0,0,-self.r)
        theta = math.pi/n1
        phi = 2*math.pi/n2
        hp = math.pi*0.5
        
        for i in range(1,n1):
            for j in range(n2):
                tx = self.r * math.cos(i*theta-hp) * math.cos(j*phi)
                ty = self.r * math.cos(i*theta-hp) * math.sin(j*phi)
                tz = self.r * math.sin(i*theta-hp)
                m.add_node(Node(tx,ty,tz))
 
        # south pole cap of triangles
        for j in range(n2):
            nc = m.nodes[j]
            nn = m.nodes[(j+1)%n2]
            m.add_face(Face([sp,nn,nc]))
            
        # mid part quads
        for i in range(n1-2):
            for j in range(n2):
                jj = (j+1)%n2
                a = m.nodes[i*n2+j]
                b = m.nodes[i*n2+jj]
                c = m.nodes[(i+1)*n2+jj]
                d = m.nodes[(i+1)*n2+j]
                m.add_face(Face([a,b,c,d]))
                
        # north pole cap of triangles
        for j in range(n2):
            nc = m.nodes[len(m.nodes)-1-j]
            nn = m.nodes[len(m.nodes)-1-(j+1)%n2]
            m.add_face(Face([np,nn,nc]))
        
        m.add_node(np)
        m.add_node(sp)
        return m
    
    def get_distance(self,x,y,z):
        """
        distance function
        """
        # long version
        d = math.sqrt((x-self.loc.x)**2 + (y-self.loc.y)**2 + (z-self.loc.z)**2) - self.r
        
        return d
    
    def get_bounds(self):
        return (self.loc.x-self.r, self.loc.y-self.r, self.loc.z-self.r,
                self.loc.x+self.r, self.loc.y+self.r, self.loc.z+self.r)


class Torus(object):
    """
    this is the torus class
    """
    def __init__(self, cx=0, cy=0, cz=0, raddonut=2, radpipe=1):
        self.loc = Vector(cx,cy,cz)
        self.rd = raddonut
        self.rp = radpipe
        
    def get_mesh(self, n1=20, n2=10):
        m = Mesh()
        
        theta = (math.pi*2.0)/n1
        phi = (math.pi*2.0)/n2
        
        for i in range(n1):
            for j in range(n2):
                tx = math.cos(i*theta)*(self.rd + self.rp*math.cos(j*phi))
                ty = math.sin(i*theta)*(self.rd + self.rp*math.cos(j*phi))
                tz = self.rp*math.sin(j*phi)
                m.add_node(Node(tx,ty,tz))
                
        for i in range(n1):
            for j in range(n2):
                ii = (i+1)%n1
                jj = (j+1)%n2
                a = m.nodes[ i*n2 + j ]
                b = m.nodes[ii*n2 + j ]
                c = m.nodes[ii*n2 + jj]
                d = m.nodes[ i*n2 + jj]
                m.add_face(Face([a,b,c,d]))
        
        return m

    def get_distance(self,x,y,z):
        """
        distance function
        """
        dx = x-self.loc.x
        dy = y-self.loc.y
        dz = z-self.loc.z
        
        dxy = math.sqrt(dx**2 + dy**2)
        d2 = math.sqrt((dxy-self.rd)**2 + dz**2)
        d = d2-self.rp
        
        return d


class Cylinder(object):
    """
    this is the torus class
    """
    def __init__(self, cx=0, cy=0, cz=0, r=1, h=1):
        self.loc = Vector(cx,cy,cz)
        self.r = r
        self.h = h
        
    def get_mesh(self, n=20):
        m = Mesh()
        
        theta = (math.pi*2.0)/n
        
        np = Node(0,0, self.h/2.0)
        sp = Node(0,0,-self.h/2.0)
        
        for i in range(n):
            tx = self.r * math.cos(i*theta)
            ty = self.r * math.sin(i*theta)
            tz1 =  self.h/2.0
            tz2 = -self.h/2.0
            m.add_node(Node(tx,ty,tz1))
            m.add_node(Node(tx,ty,tz2))
            
        for i in range(n):
            a = m.nodes[i*2]
            b = m.nodes[i*2+1]
            c = m.nodes[((i+1)%n)*2+1]
            d = m.nodes[((i+1)%n)*2]
            m.add_face(Face([a,b,c,d]))
            m.add_face(Face([c,b,sp]))
            m.add_face(Face([a,d,np]))
        
        m.add_node(np)
        m.add_node(sp)
        
        return m
    
    def get_distance(self,x,y,z):
        """
        distance function
        """
        dx = x-self.loc.x
        dy = y-self.loc.y
        dz = abs(z-self.loc.z)
        
        # 2d circle distance
        dxy = math.sqrt(dx**2 + dy**2) - self.r
        # cut with cap plances
        d = max(dxy, dz-self.h/2.0)
        return d


class Dodecahedron(object):
    """
    this is the dodecahedron class.
    a polyhedron made of 12 equilateral pentagons.
    """
    def __init__(self, cx=0, cy=0, cz=0, rad=1):
        self.loc = Vector(cx,cy,cz)
        self.rad = rad
        
    def get_mesh(self):
        m = Mesh()
        
        phi = (1+sqrt(5.0))/2.0
        nodes = []
        nodes.append(Node( 1, 1, 1))
        nodes.append(Node( 1, 1,-1))
        nodes.append(Node( 1,-1, 1))
        nodes.append(Node( 1,-1,-1))
        nodes.append(Node(-1, 1, 1))
        nodes.append(Node(-1, 1,-1))
        nodes.append(Node(-1,-1, 1))
        nodes.append(Node(-1,-1,-1))
        
        nodes.append(Node(0,-phi,-1/phi))
        nodes.append(Node(0,-phi, 1/phi))
        nodes.append(Node(0, phi,-1/phi))
        nodes.append(Node(0, phi, 1/phi))
    
        nodes.append(Node(-phi,-1/phi,0))
        nodes.append(Node(-phi, 1/phi,0))
        nodes.append(Node( phi,-1/phi,0))
        nodes.append(Node( phi, 1/phi,0))
        
        nodes.append(Node(-1/phi,0,-phi))
        nodes.append(Node( 1/phi,0,-phi))
        nodes.append(Node(-1/phi,0, phi))
        nodes.append(Node( 1/phi,0, phi))
        
        for i in range(len(nodes)):
            vadd = nodes[i].addition(self.loc)
            vadd = vadd.normalized()
            vadd = vadd.multiply(self.rad)
            nodes[i] = Node(vadd.x, vadd.y, vadd.z)
        
        m.add_face(Face([nodes[2], nodes[9], nodes[6], nodes[18], nodes[19]]))
        m.add_face(Face([nodes[4], nodes[11], nodes[0], nodes[19], nodes[18]]))
        m.add_face(Face([nodes[18], nodes[6], nodes[12], nodes[13], nodes[4]]))
        m.add_face(Face([nodes[19], nodes[0], nodes[15], nodes[14], nodes[2]]))
        m.add_face(Face([nodes[4], nodes[13], nodes[5], nodes[10], nodes[11]]))
        m.add_face(Face([nodes[14], nodes[15], nodes[1], nodes[17], nodes[3]]))
        m.add_face(Face([nodes[1], nodes[15], nodes[0], nodes[11], nodes[10]]))
        m.add_face(Face([nodes[3], nodes[17], nodes[16], nodes[7], nodes[8]]))
        m.add_face(Face([nodes[2], nodes[14], nodes[3], nodes[8], nodes[9]]))
        m.add_face(Face([nodes[6], nodes[9], nodes[8], nodes[7], nodes[12]]))
        m.add_face(Face([nodes[1], nodes[10], nodes[5], nodes[16], nodes[17]]))
        m.add_face(Face([nodes[12], nodes[7], nodes[16], nodes[5], nodes[13]]))
        
        return m
