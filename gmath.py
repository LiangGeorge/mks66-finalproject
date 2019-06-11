import math
from display import *
from Vector import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1 #How much light is absorbed
SPECULAR = 2 # Shinyness
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, symbols, reflect ):

    n = normal[:]
    normalize(n)
    normalize(light[LOCATION])
    normalize(view)
    r = symbols[reflect][1]

    a = calculate_ambient(ambient, r)
    d = calculate_diffuse(light, r, n)
    s = calculate_specular(light, r, view, n)

    i = [0, 0, 0]
    i[RED] = int(a[RED] + d[RED] + s[RED])
    i[GREEN] = int(a[GREEN] + d[GREEN] + s[GREEN])
    i[BLUE] = int(a[BLUE] + d[BLUE] + s[BLUE])
    limit_color(i)

    return i

def calculate_ambient(alight, reflect):
    a = [0, 0, 0]
    a[RED] = alight[RED] * reflect['red'][AMBIENT]
    a[GREEN] = alight[GREEN] * reflect['green'][AMBIENT]
    a[BLUE] = alight[BLUE] * reflect['blue'][AMBIENT]
    return a

def calculate_diffuse(light, reflect, normal):
    d = [0, 0, 0]

    dot = dot_product( light[LOCATION], normal)

    dot = dot if dot > 0 else 0
    d[RED] = light[COLOR][RED] * reflect['red'][DIFFUSE] * dot
    d[GREEN] = light[COLOR][GREEN] * reflect['green'][DIFFUSE] * dot
    d[BLUE] = light[COLOR][BLUE] * reflect['blue'][DIFFUSE] * dot
    return d

def calculate_specular(light, reflect, view, normal):
    s = [0, 0, 0]
    n = [0, 0, 0]

    result = 2 * dot_product(light[LOCATION], normal)
    n[0] = (normal[0] * result) - light[LOCATION][0]
    n[1] = (normal[1] * result) - light[LOCATION][1]
    n[2] = (normal[2] * result) - light[LOCATION][2]

    result = dot_product(n, view)
    result = result if result > 0 else 0
    result = pow( result, SPECULAR_EXP )

    s[RED] = light[COLOR][RED] * reflect['red'][SPECULAR] * result
    s[GREEN] = light[COLOR][GREEN] * reflect['green'][SPECULAR] * result
    s[BLUE] = light[COLOR][BLUE] * reflect['blue'][SPECULAR] * result
    return s

def limit_color(color):
    color[RED] = 255 if color[RED] > 255 else color[RED]
    color[GREEN] = 255 if color[GREEN] > 255 else color[GREEN]
    color[BLUE] = 255 if color[BLUE] > 255 else color[BLUE]

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

def get_magnitude(vector):
    return math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
#Return the dot porduct of a . b
def dot_product(a, b):
# if type(a) == Vector:
    a = a.direction
# if type(b) == Vector:
    b = b.direction
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Returns whether the angle is obtuse, acute, or perpendicular for vectors
def where_pointing(a,b):
    prod = dot_product(a,b)
    if prod == 0:
        return "perpendicular"
    elif prod > 0:
        return "acute"
        #We cannot see this surface so don't render
        #This is also not facing the light vector
    else:
        return "obtuse"
        #We can see this surface
        #This is facing the light vector
        #Now find distance between the light and the object vector to find the lighting

#Use this with light or camera vector and the normal in order to see if a specific face can be seen
def can_see (a,b):
    prod = dot_product(a,b)
    if prod > 0:
        return False
    elif prod < 0:
        return True
    return False

#Return the angle between two vectors
def angle_between(a,b):
    return math.acos(dot_product(normalize(a),normalize(b)))

#Return the length of vector a projected onto vector b
def proj_length(a,b):
    return dot_product(a,normalize(b))

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
#This is generated from using the cross product of vectors of two sides
#Could reference this to check the signs
def calculate_cross_area(A,B):
    N = [0, 0, 0]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]
    magnitude = math.sqrt( N[0] * N[0] +
                           N[1] * N[1] +
                           N[2] * N[2])
    return abs(magnitude)
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N

def calculate_discriminant(a,b,c):
    return (b ** 2) - (4 * a * c)

def distance_formula(a,b):
    d = math.sqrt(((b[0] - a[0]) ** 2) + ((b[1] - a[1]) ** 2) + ((b[2] - a[2])**2))
    return d

def quad_form(a,b,c):
    first = ((-1 * b) - math.sqrt(calculate_discriminant(a,b,c))) / (2 * a)
    second =  ((-1 * b) + math.sqrt(calculate_discriminant(a,b,c))) / (2 * a)
    return (first,second)
