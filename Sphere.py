from gmath import *
class Sphere:

    def __init__(self,origin,radius):
        self.o = origin
        self.r = radius

    def isIntersect(self,avector,avectoro):
        pass
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
