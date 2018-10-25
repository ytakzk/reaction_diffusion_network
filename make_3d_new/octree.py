from meshobjs import Vector
import marching_cubes_3d as mc
import math

class OcTree():
    """
    octree class for adaptive subdivision
    """
    def __init__(self, pt, ws):
        self.worldsize = float(ws)
        self.maxlevels = 3
        self.sqrt2 = math.sqrt(2.0)
        self.sqrt3 = math.sqrt(3.0)
        self.pos = pt
        self.rootnode = OctNode(pt.x,pt.y,pt.z, ws, 0)
        self.distobj = None

    def set_level(self, n):
        self.maxlevels = n
        #print self.worldsize/(2**self.maxlevels)

    def divide(self, node, res):
        if node.level < self.maxlevels:
            d = self.distobj.get_distance(node.pos.x, node.pos.y, node.pos.z)
            node.distance = d
            if abs(d) < self.sqrt3 * node.edge/2:
                node.divide_node()
                for b in node.branches:
                    self.divide(b,res)
        else:
            cm = mc.marching_cubes_3d_single_cell(self.distobj.get_distance,
                                                  node.pos.x, node.pos.y, node.pos.z, node.edge)
            res.add_faces(cm.faces)
            for n in cm.nodes:
                res.add_node(n)
            

class OctNode():
    """
    node of octree that is either leaf node
    or has 8 child nodes as branches
    """
    def __init__(self, x,y,z, s, l):
        self.pos = Vector(x,y,z)
        self.edge = s
        self.level = l
        self.branches = None
        self.distance = 0.0 #get_distance(x,y,z)

    def divide_node(self):
        self.branches = []
        qs = self.edge/4.0
        nl = self.level + 1
        self.branches.append(OctNode(self.pos.x-qs, self.pos.y-qs, self.pos.z-qs, qs*2, nl))
        self.branches.append(OctNode(self.pos.x+qs, self.pos.y-qs, self.pos.z-qs, qs*2, nl))
        self.branches.append(OctNode(self.pos.x-qs, self.pos.y+qs, self.pos.z-qs, qs*2, nl))
        self.branches.append(OctNode(self.pos.x+qs, self.pos.y+qs, self.pos.z-qs, qs*2, nl))
        self.branches.append(OctNode(self.pos.x-qs, self.pos.y-qs, self.pos.z+qs, qs*2, nl))
        self.branches.append(OctNode(self.pos.x+qs, self.pos.y-qs, self.pos.z+qs, qs*2, nl))
        self.branches.append(OctNode(self.pos.x-qs, self.pos.y+qs, self.pos.z+qs, qs*2, nl))
        self.branches.append(OctNode(self.pos.x+qs, self.pos.y+qs, self.pos.z+qs, qs*2, nl))
