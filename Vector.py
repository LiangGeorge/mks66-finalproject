import math
from matrix import matrix_mult

class Vector:
    def __init__(self, direction):
        self.direction = direction
        if len(direction) == 3:
            direction.append(1)

    def get_direction(self):
        return self.direction

    def __add__(self,o):
        return

    def applyMatrix(self, matrix):
        matrix_mult(matrix, [self.direction])

    #Scaling our vector
    def scaleup(self,scalar):
        self.direction[0] *= scalar[0]
        self.direction[1] *= scalar[1]
        self.direction[2] *= scalar[2]

    def scaledown(self,scalar):
        self.direction[0] /= scalar[0]
        self.direction[1] /= scalar[1]
        self.direction[2] /= scalar[2]

    def __iadd__(self,o):
        self.direction[0] += o.direction[0]
        self.direction[1] += o.direction[1]
        self.direction[2] += o.direction[2]
        return self


    def __mul__(self,o):
        return Vector([self.direction[0] * o,self.direction[1] * o,self.direction[2] * o])
    #dividing two vectors
    def __truediv__(self,o):
        return Vector([self.direction[0] / o.direction[0],self.direction[1] / o.direction[1],self.direction[2] / o.direction[2]])

    def __add__(self,o):
        return Vector([self.direction[0] + o.direction[0],self.direction[1] + o.direction[1],self.direction[2] + o.direction[2]])

    def __sub__(self,o):
        return Vector([self.direction[0] - o.direction[0],self.direction[1] - o.direction[1],self.direction[2] - o.direction[2]])

    def __str__(self):
        return '<' + ','.join(str(x) for x in self.direction) + '>'

    def get_mag(self):
        return math.sqrt( self.direction[0] * self.direction[0] +
                               self.direction[1] *self.direction[1] +
                               self.direction[2] * self.direction[2] )

    def normalize(self):
        inv = 1/self.get_mag()
        self.direction[0] *= inv
        self.direction[1] *= inv
        self.direction[2] *= inv
        return self

    def multComponents(self, other):
        # print(str(self), str(other))
        self.direction[0] *= other.direction[0]
        self.direction[1] *= other.direction[1]
        self.direction[2] *= other.direction[2]
        return self

    def dot(self, other):
        a = self.direction
        b = other.direction
        return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

    def cross(self, other):
        x = (self.direction[1] * other.direction[2]) - (self.direction[2] * other.direction[1])
        y = (self.direction[2] * other.direction[0]) - (self.direction[0] * other.direction[2])
        z = (self.direction[0] * other.direction[1]) - (self.direction[1] * other.direction[0])
        return Vector([x,y,z])
