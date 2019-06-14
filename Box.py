from Triangle import *
from Vector import *
from Ray import *
from Light import DEFAULT_CONS
from gmath import *
import math
class Box:
    def __init__(self,p0,width,height,depth,constants = DEFAULT_CONS):
        x = p0[0]
        y = p0[1]
        z = p0[2]
        x1 = x + width
        y1 = y - height
        z1 = z - depth
        self.cons = constants
        self.triList = [Triangle(Vector([x, y, z]),Vector([x1, y1, z]),Vector([x1, y, z]),constants),
                        Triangle(Vector([x, y, z]),Vector([x, y1, z]),Vector([x1, y1, z]),constants),
                        Triangle(Vector([x1, y, z1]),Vector([x, y1, z1]),Vector([x, y, z1]),constants),
                        Triangle(Vector([x1, y, z1]),Vector([x1, y1, z1]),Vector([x, y1, z1]),constants),
                        Triangle(Vector([x, y, z1]),Vector([ x, y1, z]),Vector([x, y, z]),constants),
                        Triangle(Vector([x, y, z1]),Vector([x, y1, z1]),Vector([x, y1, z]),constants),
                        Triangle(Vector([x1, y, z]),Vector([x1, y1, z1]),Vector([x1, y, z1]),constants),
                        Triangle(Vector([x1, y, z]),Vector([x1, y1, z]),Vector([x1, y1, z1]),constants),
                        Triangle(Vector([x, y, z1]),Vector([ x1, y, z]),Vector([x1, y, z1]),constants),
                        Triangle(Vector([x, y, z1]),Vector([x, y, z]),Vector([x1, y, z]),constants),
                        Triangle(Vector([x, y1, z]),Vector([x1, y1, z1]),Vector([x1, y1, z]),constants),
                        Triangle(Vector([x, y1, z]),Vector([x, y1, z1]),Vector([x1, y1, z1]),constants)
                        ]

    def applyMatrix(self,matrix):
        for tri in self.triList:
            tri.applyMatrix(matrix)

    def isIntersect(self,ray):
        for tri in self.triList:
            res = tri.isIntersect(ray)
            if res != None:
                return res

    def getReflected(self,ray,point):
        for tri in self.triList:
            res = tri.isIntersect(ray)
            if res != None:
                return tri.getReflected(ray,point)
