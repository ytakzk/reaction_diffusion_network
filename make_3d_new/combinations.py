import math

class Union(object):
    """
    boolean union of two or more objects
    """
    def __init__(self, obja=None, objb=None):
        # self.a = obja
        # self.b = objb
        if type(obja)==type([]):
            self.objs = obja
        else:
            self.objs = [obja,objb]
        
    def get_distance(self,x,y,z):
        # da = self.a.get_distance(x,y,z)
        # db = self.b.get_distance(x,y,z)
        # return min(da,db)
        ds = [o.get_distance(x,y,z) for o in self.objs]
        return min(ds)
    
class Intersection(object):
    """
    boolean intersection of two or more objects
    """
    def __init__(self, obja=None, objb=None):
        # self.a = obja
        # self.b = objb
        if type(obja)==type([]):
            self.objs = obja
        else:
            self.objs = [obja,objb]
        
    def get_distance(self,x,y,z):
        # da = self.a.get_distance(x,y,z)
        # db = self.b.get_distance(x,y,z)
        # return min(da,db)
        ds = [o.get_distance(x,y,z) for o in self.objs]
        return max(ds)
    
class Subtraction(object):
    """
    boolean subtraction of a minus b
    """
    def __init__(self, obja, objb):
        self.a = obja
        self.b = objb
        
    def get_distance(self,x,y,z):
        da = self.a.get_distance(x,y,z)
        db = self.b.get_distance(x,y,z)
        return max(da,-db)
    
class Blend(object):
    """
    smooth blend between a and b
    """
    def __init__(self, obja, objb, r=2):
        self.a = obja
        self.b = objb
        self.r = r
        
    def get_distance(self,x,y,z):
        da = self.a.get_distance(x,y,z)
        db = self.b.get_distance(x,y,z)
        e = max(self.r - abs(da-db), 0)
        return min(da,db) - e*e*0.25/self.r

# original GLSL implementation by MERCURY http://mercury.sexy/hg_sdf
# Java port by W:Blut (Frederik Vanhoutte): https://github.com/wblut/HE_Mesh/blob/master/src/math/wblut/math/WB_SDF.java

class StairUnion(object):
    """
    union with n number of stairs between
    """
    def __init__(self, obja, objb, n=3, ra=40.0):
        self.a = obja
        self.b = objb
        self.n = n
        self.ra = ra
        
    def get_distance(self,x,y,z):
        da = self.a.get_distance(x,y,z)
        db = self.b.get_distance(x,y,z)

        s = self.ra / self.n;
        u = db - self.ra;
        return min(min(da, db), 0.5 * (u + da + abs((u - da + s) % (2 * s) - s)))

class StairIntersection(object):
    """
    intersection with n number of stairs between
    """
    def __init__(self, obja, objb, n=3, ra=40.0):
        self.a = obja
        self.b = objb
        self.n = n
        self.ra = ra
        
    def get_distance(self,x,y,z):
        da = -self.a.get_distance(x,y,z)
        db = -self.b.get_distance(x,y,z)
        
        s = self.ra / self.n;
        u = db - self.ra;
        return -min(min(da, db), 0.5 * (u + da + abs((u - da + s) % (2 * s) - s)))

class StairSubtraction(object):
    """
    subtraction with n number of stairs between
    """
    def __init__(self, obja, objb, n=3, ra=40.0):
        self.a = obja
        self.b = objb
        self.n = n
        self.ra = ra
        
    def get_distance(self,x,y,z):
        da = -self.a.get_distance(x,y,z)
        db =  self.b.get_distance(x,y,z)
        
        s = self.ra / self.n;
        u = db - self.ra;
        return -min(min(da, db), 0.5 * (u + da + abs((u - da + s) % (2 * s) - s)))

class Pipe(object):
    """
    pipe along the intersection curve
    """
    def __init__(self, obja, objb, ra=20.0):
        self.a = obja
        self.b = objb
        self.ra = ra
        
    def get_distance(self,x,y,z):
        da = -self.a.get_distance(x,y,z)
        db =  self.b.get_distance(x,y,z)
        
        d = math.sqrt(da**2 + db**2)
        return d-self.ra

class UGroove(object):
    """
    rectangular groove along the intersection curve
    """
    def __init__(self, obja, objb, ra=20.0, rb=10.0, pos=False):
        self.a = obja
        self.b = objb
        self.ra = ra
        self.rb = rb
        self.ps = pos
        
    def get_distance(self,x,y,z):
        da = -self.a.get_distance(x,y,z)
        db = self.b.get_distance(x,y,z)
        if self.ps:
            da *=-1
        return min(da, max(da-self.ra, abs(db) - self.rb))

class VGroove(object):
    """
    rectangular groove along the intersection curve
    """
    def __init__(self, obja, objb, ra=20.0, rb=10.0, pos=False):
        self.a = obja
        self.b = objb
        self.ra = ra
        self.rb = rb
        self.ps = pos
        
    def get_distance(self,x,y,z):
        da = self.a.get_distance(x,y,z)
        db = self.b.get_distance(x,y,z)
        if self.ps:
            da *=-1
        return max(da, (da + self.ra - abs(db)) * math.sqrt(0.5))

class ChamferUnion(object):
    """
    union with a chamfer
    """
    def __init__(self, obja, objb, ra=20.0):
        self.a = obja
        self.b = objb
        self.ra = ra
        self.sqh = math.sqrt(0.5)
        
    def get_distance(self,x,y,z):
        da = self.a.get_distance(x,y,z)
        db = self.b.get_distance(x,y,z)
        return min(min(da,db), (da - self.ra + db) * self.sqh)

class ChamferIntersection(object):
    """
    intersection with a chamfer
    """
    def __init__(self, obja, objb, ra=20.0):
        self.a = obja
        self.b = objb
        self.ra = ra
        self.sqh = math.sqrt(0.5)
        
    def get_distance(self,x,y,z):
        da = self.a.get_distance(x,y,z)
        db = self.b.get_distance(x,y,z)
        return max(max(da,db), (da + self.ra + db) * self.sqh)

class ChamferSubtraction(object):
    """
    intersection with a chamfer
    """
    def __init__(self, obja, objb, ra=20.0):
        self.a = obja
        self.b = objb
        self.ra = ra
        self.sqh = math.sqrt(0.5)
        
    def get_distance(self,x,y,z):
        da = self.a.get_distance(x,y,z)
        db = -self.b.get_distance(x,y,z)
        return max(max(da,db), (da + self.ra + db) * self.sqh)
