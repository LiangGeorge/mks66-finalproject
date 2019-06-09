class Light:

    def __init__(self, position, color):
        self.pos = position
        self.color = color

    def colorAtDist(self, dist):
        #Intensity = color / dist^2
        if dist < 1:
            return self.color
        return self.color * (dist ** -2)
