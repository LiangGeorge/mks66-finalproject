#from script import run
import sys
from display import *
from Sphere import *
from Vector import *
from Ray import *
from functools import reduce

def getColor(ray, objlst, numBounces):
    if numBounces <= 0:
        return Vector([0,0,0])
    closest = None
    closestObj = None
    for i in objlst:
        currT = i.isIntersect(ray)
        if closest == None or (currT != None and currT < closest):
            closest = currT
            closestObj = i
    if closest == None:
        return Vector([0,0,0])
    else:
        reflectedRay = closestObj.getReflected(ray, ray.pointAtT(closest))
        return Vector([10,10,10]) + getColor(reflectedRay, objlst, numBounces - 1)

def scaleColors(screen, newMinComp, newMaxComp = 255):
    maxColorComp = screen[0][0][0] #Max color component ex: [10, 20, 30] -> 30
    minColorComp = maxColorComp
    def getminmax(currminmax, colorComp):
        if colorComp > currminmax[0]:
            currminmax[0] = colorComp
        elif colorComp < currminmax[1]:
            currminmax[1] = colorComp
        return currminmax
    colorCompMinMax = reduce(getminmax, [x for i in screen for j in i for x in j], [maxColorComp, minColorComp])
    if colorCompMinMax[0] == colorCompMinMax[1]: #Solid color screen
        return
    scalar = float(newMaxComp) / (colorCompMinMax[0] - colorCompMinMax[1])
    for y in range(YRES):
        for x in range(XRES):
            if y == x == 10:
                print([c * scalar + newMinComp for c in screen[y][x]])
            screen[y][x] = [int(c * scalar + newMinComp) for c in screen[y][x]]


'''
if len(sys.argv) == 2:
    run(sys.argv[1])
elif len(sys.argv) == 1:
    run(raw_input("please enter the filename of an mdl script file: \n"))
else:
    print "Too many arguments."
'''

zbuff = new_zbuffer(500,500)
screen = new_screen()
color = [ 255, 0, 0 ]
vals = []

#Making the center as a vector allows me to use my overloaded operators
test = Sphere(Vector([250,250,100]),50)
objlst = [test, Sphere(Vector([50, 50, 30]), 20), Sphere(Vector([330, 250, 100]), 30)]
# for i in range(50, 70):
#     startRay = Ray(Vector([i, i, 0]), Vector([0,0,1]))
#     inters = objlst[1].isIntersect(startRay)
#     print( inters )
#     if inters != None:
#         print( startRay.pointAtT(inters) )
#         print( objlst[1].getReflected(startRay, startRay.pointAtT(inters) ) )
#     print('------')

for x in range(XRES):
    for y in range(YRES):
        #print(test.isIntersect(z,[250,250,0]))
        firedRay = Ray(Vector([x,y,0]),Vector([0,0,1]))
        colorVector = getColor(firedRay, objlst, 5)
        plot(screen,zbuff,colorVector.direction,x,y,1)
scaleColors(screen, 10)
display(screen)
