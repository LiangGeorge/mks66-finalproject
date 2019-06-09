#from script import run
import sys
from display import *
from Sphere import *
from Vector import *
from Ray import *

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

for x in range(501):
    for y in range(501):
        #print(test.isIntersect(z,[250,250,0]))
        firedRay = Ray(Vector([x,y,0]),Vector([0,0,1]))
        colorVector = getColor(firedRay, objlst, 5)
        plot(screen,zbuff,colorVector.direction,x,y,1)
display(screen)
