from gmath import *
import math
from Vector import *
from Ray import *
from Light import DEFAULT_CONS

class Triangle:
    def __init__(self, p0, p1, p2, constants = DEFAULT_CONS):

        #Hand these vectors in order to use overloaded operators
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.cons = constants
        self.normal = None

    def __str__(self):
        return 'Triangle[%s %s %s]' % (str(self.p0), str(self.p1), str(self.p2))

    def applyMatrix(self, matrix):
        self.p0.applyMatrix(matrix)
        self.p1.applyMatrix(matrix)
        self.p2.applyMatrix(matrix)

    def getNormal(self, blank = 1):
        if self.normal == None:
            temp = []
            edge1 = self.p1 - self.p0
            edge2 = self.p2 - self.p0
            n = edge1.cross(edge2)
            self.normal = n.normalize()
        return self.normal

    def getReflected(self, ray, point):
        '''Returns the reflected ray of a ray that hits the plane that this triangle lies on
        '''
        # R = 2P - L = 2(N(N dot L))-L
        # L = incoming * -1
        # R = reflected
        # N = normal
        normal = self.getNormal()
        incoming = ray.d.normalize() * -1 #Incoming ray direction
        p = normal * normal.dot(incoming)
        reflected = (p * 2) - incoming #Reflected direction vector
        return Ray(point, reflected )


    #Dot product of any point with the normal is the same as the dot product of any other point
    #P0 + P1 * T dotted = A dotted normal
    #p0 is ray origin p1 is ray direction

    def isIntersect(self,ray):
        epsilon = 1e-5
        edge1 = self.p1 - self.p0
        edge2 = self.p2 - self.p0
        h = ray.d.cross(edge2)
        a = edge1.dot(h)
        if (abs(a) < epsilon): # Parallel ray or backface
            return None
        f = 1./a
        s = ray.o - self.p0
        u = f * (s.dot(h))
        if (u < 0 or u > 1):
            return None
        q = s.cross(edge1)
        v = f * ray.d.dot(q)
        if (v < 0 or u + v > 1):
            return None
        # Compute t
        t = f * edge2.dot(q)
        if t < epsilon:
            return None
        return t

        #Vectors Here
        # origin = ray.o
        # direction = ray.d
        # normal = self.get_normal()
        # if (abs(ray.dot(normal)) == 0):
        #     return None
        # else:
        #     #T = (A point dot product with normal) - (Origin dot product with normal) ALL over Direction dotted normal
        #     t = (self.p1 - origin).dot(normal) / ray.d.dot(normal)
        #     if t < 1e-5:
        #         return None
        #     #self.p1 is used because it is one of the points that exist of the plane
        #     #This is only the point that intersects the plane
        #     point = ray.pointAtT(t)
        #
        #     Area = calculate_cross_area((self.p0 - self.p1).direction,(self.p0 - self.p2).direction)/2
        #     #print(Area)
        #     alpha = calculate_cross_area((point - self.p1).direction,(point - self.p2).direction) / (Area * 2)
        #     #print(alpha)
        #     beta = calculate_cross_area((point - self.p2).direction, (point - self.p0).direction)/ (Area * 2)
        #
        #     gamma = calculate_cross_area((point - self.p0).direction,(point - self.p1).direction)/ (Area * 2)
        #
        #     #print(alpha + beta + gamma)
        #     '''
        #     if (alpha >= 0 and alpha <= 1):
        #         print(alpha)
        #     if (beta >= 0 and beta <= 1):
        #         print(beta)
        #     if (gamma >= 0 and gamma <= 1):
        #         print(gamma)
        #     '''
            #
            #
            # if (alpha >= 0 and alpha <= 1) and (beta >= 0 and beta <= 1) and (gamma >= 0 and gamma <= 1) and (alpha + beta + gamma <= 1) :
            #     #print("reached")
            #     return True
