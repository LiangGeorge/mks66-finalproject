#from script import run
import sys
from display import *
from Sphere import *
from Vector import *
from Ray import *

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
test = Sphere(Vector([250,250,0]),50)
for x in range(501):
    for y in range(501):
        #print(test.isIntersect(z,[250,250,0]))
        val = test.isIntersect(Ray(Vector([x,y,0]),Vector([0,0,1])))
        if val != None:
            print(val)
            plot(screen,zbuff,color,x,y,1)
display(screen)
