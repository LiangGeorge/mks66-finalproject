from gmath import SPECULAR_EXP
from Vector import *

DEFAULT_CONS = ['constants',
                     {'red': [0.2, 0.5, 0.5],
                      'green': [0.2, 0.5, 0.5],
                      'blue': [0.2, 0.5, 0.5]}]

class Light:

    def __init__(self, position, color):
        self.pos = position
        self.color = color

    def __str__(self):
        return 'Light[%s %s]' % (str(self.pos),(str(self.color)))

    def colorAtDist(self, dist):
        #Intensity = color / dist^2
        if dist < 1:
            return self.color
        return self.color * (dist ** -2)

    def applyMatrix(self, matrix):
        self.pos.applyMatrix(matrix)

    def calculateColor(self, dist, rayToLight, normal, viewVector, constants):
        '''Returns the color of a given point
        '''
        # Specular ---------------------
        # R = 2P - L = 2(N(N dot L))-L
        # L = incoming
        # R = reflected
        # N = normal

        red = constants[1]['red']
        green = constants[1]['green']
        blue = constants[1]['blue']

        specCons = Vector([red[2], green[2], blue[2]])
        intensity = self.colorAtDist(dist)
        incoming = rayToLight.d.normalize() #Incoming ray direction
        p = normal * normal.dot(incoming)
        reflected = (p * 2) - incoming #Reflected direction vector
        specular = (intensity * ( (reflected.dot(viewVector)) ** SPECULAR_EXP )).multComponents(specCons)
        # print(incoming)
        # print(reflected)

        # Diffuse ---------------------
        diffCons = Vector([red[1], green[1], blue[1]])
        diffuse = (intensity * normal.dot(incoming)).multComponents(diffCons)

        return specular + diffuse
