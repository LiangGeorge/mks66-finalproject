class Ray:
    def __init__(self,origin,direction):
        #These should be vectors just for ease
        self.o = origin
        self.d = direction

    def pointAtT(self, t):
        return self.o + (self.d * t)

    def __str__(self):
        return '[ ' + str(self.o) + ' ' + str(self.d) + ' ]'

#Ray and Triangle Intersection involves intersecting the plane of the triangle and then checking if the intersection point is within triangle
