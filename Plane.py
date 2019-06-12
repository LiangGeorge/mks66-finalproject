from gmath import *
import math
from Vector import *

class Plane:
    def __init__(self,p0,p1,p2):
        #Hand these vectors in order to use overloaded operators
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2


    def get_normal(self):
        temp = []
        temp.append(self.p0.direction)
        temp.append(self.p1.direction)
        temp.append(self.p2.direction)
        n = calculate_normal(temp,0)
        return Vector(n).normalize()

    def isIntersect(self,ray):
        origin = ray.o
        direction = ray.d
        normal = self.get_normal()
        if (abs(ray.dot(normal)) == 0):
            return None
        else:
            #T = (A point dot product with normal) - (Origin dot product with normal) ALL over Direction dotted normal
            t = (self.p1 - origin).dot(normal) / ray.d.dot(normal)
            if t < 1e-5:
                return None
            #self.p1 is used because it is one of the points that exist of the plane
            #This is only the point that intersects the plane
            point = ray.pointAtT(t)
