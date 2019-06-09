from gmath import *
from Ray import *
from Vector import *

class Sphere:

    def __init__(self,origin,radius):
        self.o = origin
        self.r = radius

    def __str__(self):
        return 'Center: ' + str(self.o) + ' Radius: ' + str(self.r)

    def getReflected(self, ray, point):
        '''Returns the reflected ray of a ray that hits a given point on the sphere
        '''
        # R = 2P - L = 2(N(N dot L))-L
        # L = incoming * -1
        # R = reflected
        # N = normal
        normal = self.getNormal(point)
        incoming = ray.d.normalize() * -1 #Incoming ray direction
        p = normal * normal.dot(incoming)
        reflected = (p * 2) - incoming #Reflected direction vector
        return Ray(point, reflected )


    def getNormal(self, point):
        '''Assumes that the point vector is on the sphere
           Returns t of intersection
        '''
        return (point - self.o).normalize()

    def isIntersect(self, ray):
        origin = ray.o
        direction = ray.d

        #ray = origin + dir * t

        #0 = ax^2 + bx + c
        #a = dot_product(dir, dir)
        #b = 2 * ( dot_product(dir, rayOrg - circleCenter) )
        #c = dot_product(rayOrg - center, rayOrg - center) - radius^2

        a = dot_product(direction, direction)
        b = 2 * ( dot_product(direction, origin - self.o) )
        c = dot_product(origin - self.o, origin - self.o) - (self.r ** 2)

        discriminant = calculate_discriminant(a,b,c)

        if discriminant < 0:
            return None

        threshold = 1e-5 #Considered on the sphere

        roots = quad_form(a,b,c)
        if roots[0] <= threshold and roots[1] <= threshold:
            return None
        root = roots[0] if roots[0] < roots[1] and roots[0] > threshold else roots[1]

        return root

    '''
        print(avectoro.direction)
        diffo = avectoro - self.o
        #print diffo

        a = dot_product(avector.direction,avector.direction)
        #print(a)
        #print(avector.direction)
        b = 2 * dot_product(avector.direction, diffo) + dot_product(diffo,diffo)
        #print(b)
        c = self.r ** 2
        print(c)
        tval = None
        #print(a)
        #print(b)

        if calculate_discriminant(a,b,c) < 0:
            #print(calculate_discriminant(a,b,c))
            return False

        elif calculate_discriminant(a,b,c) == 0:
            tval =  quad_form(a,b,c)[0]
        else:
            print("Reached")
            ret = quad_form(a,b,c)
            if ret[0] < 0:
                tval = ret[1]
            elif ret[1] < 0:
                tval = ret[0]
            else:
                if ret[0] < ret[1]:
                    tval = ret[0]
                else:
                    tval =  ret[1]
        tmuldir = avector * tval
        #This should be the intersection point
        return avectoro + tmuldir
        #print(avectoro.direction)
        diffo = avectoro - self.o
        #print diffo

        a = dot_product(avector.direction,avector.direction)
        #print(a)
        #print(avector.direction)
        b = 2 * dot_product(avector.direction, diffo) + dot_product(diffo,diffo)
        #print(b)
        c = self.r ** 2
        print(c)
        tval = None
        #print(a)
        #print(b)

        if calculate_discriminant(a,b,c) < 0:
            #print(calculate_discriminant(a,b,c))
            return False

        elif calculate_discriminant(a,b,c) == 0:
            tval =  quad_form(a,b,c)[0]
        else:
            print("Reached")
            ret = quad_form(a,b,c)
            if ret[0] < 0:
                tval = ret[1]
            elif ret[1] < 0:
                tval = ret[0]
            else:
                if ret[0] < ret[1]:
                    tval = ret[0]
                else:
                    tval =  ret[1]
        tmuldir = avector * tval
        #This should be the intersection point
        return avectoro + tmuldir
    '''
