import math

class Vector:
    def __init__(self, direction):
        self.direction = direction

    def get_direction(self):
        return self.direction

    def __add__(self,o):
        return

    #Scaling our vector
    def scaleup(self,scalar):
        self.direction[0] *= scalar[0]
        self.direction[1] *= scalar[1]
        self.direction[2] *= scalar[2]

    def scaledown(self,scalar):
        self.direction[0] /= scalar[0]
        self.direction[1] /= scalar[1]
        self.direction[2] /= scalar[2]

    def __iadd__(self,scalar):
        self.direction[0] += scalar[0]
        self.direction[1] += scalar[1]
        self.direction[2] += scalar[2]


    def __mul__(self,o):
        return [self.direction[0] * o,self.direction[1] * o,self.direction[2] * o]
    #dividing two vectors
    def __truediv__(self,o):
        return [self.direction[0] / o.direction[0],self.direction[1] / o.direction[1],self.direction[2] / o.direction[2]]

    def __add__(self,o):
        return [self.direction[0] + o[0],self.direction[1] + o[1],self.direction[2] + o[2]]

    def __sub__(self,o):
        return [self.direction[0] - o.direction[0],self.direction[1] - o.direction[1],self.direction[2] - o.direction[2]]

    def get_mag(self):
        return math.sqrt( self.direction[0] * self.direction[0] +
                               self.direction[1] *self.direction[1] +
                               self.direction[2] * self.direction[2])

    def normal(self):
        inv = 1/get_mag()
        self.direction[0] *= inv
        self.direction[1] *= inv
        self.direction[2] *= inv
        return self.direction
