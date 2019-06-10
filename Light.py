from gmath import SPECULAR_EXP

class Light:

    def __init__(self, position, color):
        self.pos = position
        self.color = color

    def colorAtDist(self, dist):
        #Intensity = color / dist^2
        if dist < 1:
            return self.color
        return self.color * (dist ** -2)

    def calculateColor(self, dist, rayToLight, normal, viewVector):
        '''Returns the color of a given point
        '''
        # Specular ---------------------
        # R = 2P - L = 2(N(N dot L))-L
        # L = incoming
        # R = reflected
        # N = normal
        intensity = self.colorAtDist(dist)
        incoming = rayToLight.d.normalize() #Incoming ray direction
        p = normal * normal.dot(incoming)
        reflected = (p * 2) - incoming #Reflected direction vector
        specular = intensity * ( (reflected.dot(viewVector)) ** SPECULAR_EXP )

        # Diffuse ---------------------
        diffuse = intensity * normal.dot(incoming)

        return specular + diffuse
