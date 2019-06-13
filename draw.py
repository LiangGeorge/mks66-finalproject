from display import *
from matrix import *
from gmath import *
from Sphere import *
from Box import *
from Vector import *
from Ray import *
from Light import *
from functools import reduce
from Triangle import *
from draw import *
import sys, time
import multiprocessing as mp
from display import *
# lightlst = [Light(Vector([-500, 250, 0]), Vector([1770000, 1560000, 2170000])),
#             Light(Vector([250, 190, 100]), Vector([1190, 1580, 2030])),
#             Light(Vector([400, 400, 100]), Vector([25500, 10500, 9700])),
#             Light(Vector([750, -250, 100]), Vector([2550000, 2550000, 2550000]))]

# def retrieve_polygons(polygons):
#     print("Printing polygon clone")
#     print(polygons)
#     objlst = polygons[:]

def draw_scanline(x0, z0, x1, z1, y, screen, zbuffer, color):
    if x0 > x1:
        tx = x0
        tz = z0
        x0 = x1
        z0 = z1
        x1 = tx
        z1 = tz

    x = x0
    z = z0
    delta_z = (z1 - z0) / (x1 - x0 + 1) if (x1 - x0 + 1) != 0 else 0

    while x <= x1:
        plot(screen, zbuffer, color, x, y, z)
        x+= 1
        z+= delta_z

def scanline_convert(polygons, i, screen, zbuffer, color):
    flip = False
    BOT = 0
    TOP = 2
    MID = 1

    points = [ (polygons[i][0], polygons[i][1], polygons[i][2]),
               (polygons[i+1][0], polygons[i+1][1], polygons[i+1][2]),
               (polygons[i+2][0], polygons[i+2][1], polygons[i+2][2]) ]

    # alas random color, we hardly knew ye
    #color = [0,0,0]
    #color[RED] = (23*(i/3)) %256
    #color[GREEN] = (109*(i/3)) %256
    #color[BLUE] = (227*(i/3)) %256

    points.sort(key = lambda x: x[1])
    x0 = points[BOT][0]
    z0 = points[BOT][2]
    x1 = points[BOT][0]
    z1 = points[BOT][2]
    y = int(points[BOT][1])

    distance0 = int(points[TOP][1]) - y * 1.0 + 1
    distance1 = int(points[MID][1]) - y * 1.0 + 1
    distance2 = int(points[TOP][1]) - int(points[MID][1]) * 1.0 + 1

    dx0 = (points[TOP][0] - points[BOT][0]) / distance0 if distance0 != 0 else 0
    dz0 = (points[TOP][2] - points[BOT][2]) / distance0 if distance0 != 0 else 0
    dx1 = (points[MID][0] - points[BOT][0]) / distance1 if distance1 != 0 else 0
    dz1 = (points[MID][2] - points[BOT][2]) / distance1 if distance1 != 0 else 0

    while y <= int(points[TOP][1]):
        if ( not flip and y >= int(points[MID][1])):
            flip = True

            dx1 = (points[TOP][0] - points[MID][0]) / distance2 if distance2 != 0 else 0
            dz1 = (points[TOP][2] - points[MID][2]) / distance2 if distance2 != 0 else 0
            x1 = points[MID][0]
            z1 = points[MID][2]

        #draw_line(int(x0), y, z0, int(x1), y, z1, screen, zbuffer, color)
        draw_scanline(int(x0), z0, int(x1), z1, y, screen, zbuffer, color)
        x0+= dx0
        z0+= dz0
        x1+= dx1
        z1+= dz1
        y+= 1



def add_polygon( polygons, x0, y0, z0, x1, y1, z1, x2, y2, z2 ):
    add_point(polygons, x0, y0, z0)
    add_point(polygons, x1, y1, z1)
    add_point(polygons, x2, y2, z2)

def draw_polygons( polygons, screen, zbuffer, view, ambient, light, symbols, reflect):

    #Printing handed out polygons
    print("Current Polygon List: ")
    print(polygons)
    zbuff = new_zbuffer(500,500)
    screen = new_screen()
    color = [ 255, 0, 0 ]
    vals = []

    #Making the center as a vector allows me to use my overloaded operators
    test = Sphere(Vector([250,250,100]),50)
    objlst = [test, Sphere(Vector([50, 50, 30]), 20), Sphere(Vector([330, 250, 100]), 30), Sphere(Vector([250, 500, 100]), 70)]
    lightlst = [Light(Vector([-500, 250, 0]), Vector([1770000, 1560000, 2170000])),
                Light(Vector([250, 190, 100]), Vector([1190, 1580, 2030])),
                Light(Vector([400, 400, 100]), Vector([25500, 10500, 9700])),
                Light(Vector([750, -250, 100]), Vector([2550000, 2550000, 2550000]))]
    # lightlst = [Light(Vector([-500, 250, 0]), Vector([1770000, 1560000, 2170000]))]
    # lightlst = [Light(Vector([190, 250, 100]), Vector([119, 158, 203]))]
    test0 = Triangle(Vector([100,300,100]),Vector([200,300,100]),Vector([150,450,100]))
    temp = []
    #add_torus(temp,250,250,100,25,150,50)
    add_box(temp,100,350,100,100,100,100)
    tmp = new_matrix()
    ident(tmp)
    matrix_mult(make_rotX(30),tmp)
    matrix_mult(make_rotY(-20), tmp)
    matrix_mult(tmp,temp)

    triangles = []
    for x in range(0,len(temp) - 2,3):
        triangles.append(Triangle(Vector(temp[x][:3]),Vector(temp[x + 1][:3]),Vector(temp[x + 2][:3])))

    # triangles.append(Triangle( Vector([300, 200, 100]), Vector([250, 300, 100]), Vector([200, 200, 100]) ))

    startTime = time.time()

    # firedRay = Ray(Vector([250,250,0]), Vector([0,0,1]))
    # t = triangles[0].isIntersect(firedRay)
    # print(t)
    # refl = triangles[0].getReflected(firedRay, firedRay.pointAtT(t))
    # print(firedRay)
    # print(refl)

# def setPixelColor(ystart, yend):
#     if yend > YRES:
#         yend = YRES
#     results = []
#     for x in range(XRES):
#         for y in range(ystart, yend):
#             firedRay = Ray( Vector([x, y, 0]), Vector([0, 0, 1]) )
#             colorVector = getColor(firedRay, objlst, lightlst, 5)
#             if colorVector.direction != [0,0,0]:
#                 results.append([x, y, colorVector.direction])
#     return results
#
# def drawNoPerspective():
#     for x in range(XRES):
#         for y in range(YRES):
#             #print(test.isIntersect(z,[250,250,0]))
#             firedRay = Ray(Vector([x,y,0]),Vector([0,0,1]))
#             #print(test0.isIntersect(firedRay))
#             # for obj in objlst:
#             #     if obj.isIntersect(firedRay):
#             #         plot(screen,zbuff,color,x,y,1)
#             # colorVector = getColor(firedRay, objlst, lightlst, 5)
#             # plot(screen,zbuff,colorVector.direction,x,y,1)
#             #Multiprocessing method
#             dy = YRES // mp.cpu_count()
#             numChunks = mp.cpu_count()
#             # numChunks = 4
#             dy = dy + int( (YRES - (dy * mp.cpu_count())) // numChunks ) + 1
#             print([(chunk, chunk + dy) for chunk in range(0, YRES, dy)])
#             pool = mp.Pool(mp.cpu_count())
#             results = [pool.apply(setPixelColor, args = (chunk, chunk + dy)) for chunk in range(0, YRES, dy)]
#             pool.close()
#             # print(results)
#             print('Complete')
#             for i in results:
#                 for j in i:
#                     plot(screen,zbuff,j[2],j[0],j[1],1)
#     #
#     #         ''' Triangle Test
#     #         if test0.isIntersect(firedRay):
#     #             #print("hit")
#     #             plot(screen,zbuff,color,x,y,1)
#     #         '''
#     #
#     #         ''' Testing Some of my stuff IMPORTANT UNCOMMENT THIS PLZ
#     #         colorVector = getColor(firedRay, objlst, lightlst, 5)
#     #         plot(screen,zbuff,colorVector.direction,x,y,1)
#     #         '''


def getColor(ray, objlst, lightlst, numBounces):
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
    hitColor = Vector([0,0,0])
    intersectPoint = ray.pointAtT(closest)
    reflectedRay = closestObj.getReflected(ray, intersectPoint)
    #Make successive bounces less important based on spectral constants
    colorDecay = Vector([closestObj.cons[1]['red'][2], closestObj.cons[1]['green'][2], closestObj.cons[1]['blue'][2]])
    normal = closestObj.getNormal(intersectPoint)
    if normal.dot(reflectedRay.d) < 0:
        normal *= -1
    for light in lightlst:
        rayToLight = Ray(intersectPoint, (light.pos - intersectPoint))
        if normal.dot(rayToLight.d) < 0:
            continue
        distToLight = rayToLight.d.get_mag()
        rayToLight.d.normalize()
        for obj in objlst: #Check for object hit
            dist = obj.isIntersect(rayToLight)
            if dist != None and dist < distToLight:
                break
        else: #Executed if objects are exhausted without break
            #Phong model
            hitColor += light.calculateColor(distToLight, rayToLight, normal, ray.d, closestObj.cons)
        continue
    return (hitColor + getColor(reflectedRay, objlst, lightlst, numBounces - 1).multComponents(colorDecay))

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
            screen[y][x] = [int(c * scalar + newMinComp) for c in screen[y][x]]


    # def setPixelColorPerspective(ystart, yend, midX, midY, distAway):
    #     if yend > YRES:
    #         yend = YRES
    #     results = []
    #     for x in range(XRES):
    #         for y in range(ystart, yend):
    #             firedRay = Ray( Vector([midX, midY, distAway]), ( Vector([x, y, 0]) - Vector([250, 250, distAway]) ).normalize() )
    #             colorVector = getColor(firedRay, objlst, lightlst, 5)
    #             results.append([x, y, colorVector.direction])
    #     return results
    #
    # def drawPerspective(ang, useRad = False): #55 degrees is human
    #     if not(useRad):
    #         if not(ang < 180 and ang > 0):
    #             print("Invalid view angle")
    #             return
    #         ang *= math.pi / 180
    #     else:
    #         if not(ang < math.pi and ang > 0):
    #             print("Invalid view angle")
    #             return
    #     midX = XRES/2.
    #     midY = YRES/2.
    #     dy = YRES // mp.cpu_count()
    #     numChunks = mp.cpu_count()
    #     # numChunks = 4
    #     dy = dy + int( (YRES - (dy * mp.cpu_count())) // numChunks ) + 1
    #     distAway = -1 * (midX / math.tan(ang / 2))
    #     # print([(chunk, chunk + dy, midX, midY, distAway) for chunk in range(0, YRES, dy)])
    #     pool = mp.Pool(mp.cpu_count())
    #     results = [pool.apply(setPixelColorPerspective, args = (chunk, chunk + dy, midX, midY, distAway)) for chunk in range(0, YRES, dy)]
    #     pool.close()
    #     # output = mp.Queue()
    #     # processes = [mp.Process(target=setPixelColorPerspective, args = (chunk, chunk + dy, midX, midY, distAway)) for chunk in range(0, YRES, dy)]
    #     # for p in processes:
    #     #     p.start()
    #     # for p in processes:
    #     #     p.join()
    #     # results = [output.get() for p in processes]
    #     for i in results:
    #         for j in i:
    #             plot(screen,zbuff,j[2],j[0],j[1],1)
    #
def drawNoPerspective(screen,zbuff,objlst, lightlst):
    for x in range(XRES):
        for y in range(YRES):
            #print(test.isIntersect(z,[250,250,0]))
            firedRay = Ray(Vector([x,y,0]),Vector([0,0,1]))
            #print(test0.isIntersect(firedRay))
            # for obj in objlst:
            #     if obj.isIntersect(firedRay):
            #         plot(screen,zbuff,color,x,y,1)
            colorVector = getColor(firedRay, objlst, lightlst, 5)
            plot(screen,zbuff,colorVector.direction,x,y,1)
    # #     #
    # #     #         ''' Triangle Test
    # #     #         if test0.isIntersect(firedRay):
    # #     #             #print("hit")
    # #     #             plot(screen,zbuff,color,x,y,1)
    # #     #         '''
    # #     #
    # #     #         ''' Testing Some of my stuff IMPORTANT UNCOMMENT THIS PLZ
    # #     #         colorVector = getColor(firedRay, objlst, lightlst, 5)
    # #     #         plot(screen,zbuff,colorVector.direction,x,y,1)
    # #     #         '''
    # #
def drawPerspective(screen, zbuff, ang, objlst, lightlst, useRad = False): #55 degrees is human
    if not(useRad):
        if not(ang < 180 and ang > 0):
            print("Invalid view angle")
            return
        ang *= math.pi / 180
    else:
        if not(ang < math.pi and ang > 0):
            print("Invalid view angle")
            return
    midX = XRES/2.
    midY = YRES/2.
    distAway = -1 * (midX / math.tan(ang / 2))
    for x in range(XRES):
        for y in range(YRES):
            # print(test.isIntersect(z,[250,250,0]))
            firedRay = Ray( Vector([midX, midY, distAway]), ( Vector([x, y, 0]) - Vector([250, 250, distAway]) ).normalize() )
            # print(firedRay)
            # print(test0.isIntersect(firedRay))
            # for obj in objlst:
            #     if obj.isIntersect(firedRay):
            #         plot(screen,zbuff,color,x,y,1)
            colorVector = getColor(firedRay, objlst, lightlst, 5)
            plot(screen,zbuff,colorVector.direction,x,y,1)
    #
    # objlst = triangles




def add_box( polygons, x, y, z, width, height, depth,cons):
    polygons.append(Box([x,y,z],width,height,depth,cons))
    # x1 = x + width
    # y1 = y - height
    # z1 = z - depth
    # # print(x)
    # # print(y)
    # # print(z)
    # #Front face
    #
    # add_triangle(polygons, x, y, z, x1, y1, z, x1, y, z,cons)
    # add_triangle(polygons, x, y, z, x, y1, z, x1, y1, z,cons)
    # #Back Face
    # add_triangle(polygons, x1, y, z1, x, y1, z1, x, y, z1,cons)
    # add_triangle(polygons, x1, y, z1, x1, y1, z1, x, y1, z1,cons)
    # #Left
    # add_triangle(polygons, x, y, z1, x, y1, z, x, y, z,cons)
    # add_triangle(polygons, x, y, z1, x, y1, z1, x, y1, z,cons)
    # #Right
    # add_triangle(polygons, x1, y, z, x1, y1, z1, x1, y, z1,cons)
    # add_triangle(polygons, x1, y, z, x1, y1, z, x1, y1, z1,cons)
    # #Top
    # add_triangle(polygons, x, y, z1, x1, y, z, x1, y, z1,cons)
    # add_triangle(polygons, x, y, z1, x, y, z, x1, y, z,cons)
    # #Bottom
    # add_triangle(polygons, x, y1, z, x1, y1, z1, x1, y1, z,cons)
    # add_triangle(polygons, x, y1, z, x, y1, z1, x1, y1, z1,cons)

    # x1 = x + width
    # y1 = y - height
    # z1 = z - depth
    #
    # #front
    # add_polygon(polygons, x, y, z, x1, y1, z, x1, y, z)
    # add_polygon(polygons, x, y, z, x, y1, z, x1, y1, z)
    #
    # #back
    # add_polygon(polygons, x1, y, z1, x, y1, z1, x, y, z1)
    # add_polygon(polygons, x1, y, z1, x1, y1, z1, x, y1, z1)
    #
    # #right side
    # add_polygon(polygons, x1, y, z, x1, y1, z1, x1, y, z1)
    # add_polygon(polygons, x1, y, z, x1, y1, z, x1, y1, z1)
    # #left side
    # add_polygon(polygons, x, y, z1, x, y1, z, x, y, z)
    # add_polygon(polygons, x, y, z1, x, y1, z1, x, y1, z)
    #
    # #top
    # add_polygon(polygons, x, y, z1, x1, y, z, x1, y, z1)
    # add_polygon(polygons, x, y, z1, x, y, z, x1, y, z)
    # #bottom
    # add_polygon(polygons, x, y1, z, x1, y1, z1, x1, y1, z)
    # add_polygon(polygons, x, y1, z, x, y1, z1, x1, y1, z1)

def add_triangle(polygons,p00,p01,p02,p10,p11,p12,p20,p21,p22,cons):
    polygons.append(Triangle(Vector([p00,p01,p02]),Vector([p10,p11,p12]),Vector([p20,p21,p22]),cons))

def add_sphere(polygons, cx, cy, cz, r, cons ):
    polygons.append(Sphere(Vector([cx,cy,cz]),r,cons))
    '''
    points = generate_sphere(cx, cy, cz, r, step)

    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step

    step+= 1
    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):

            p0 = lat * step + longt
            p1 = p0+1
            p2 = (p1+step) % (step * (step-1))
            p3 = (p0+step) % (step * (step-1))

            if longt != step - 2:
                add_polygon( polygons, points[p0][0],
                             points[p0][1],
                             points[p0][2],
                             points[p1][0],
                             points[p1][1],
                             points[p1][2],
                             points[p2][0],
                             points[p2][1],
                             points[p2][2])
            if longt != 0:
                add_polygon( polygons, points[p0][0],
                             points[p0][1],
                             points[p0][2],
                             points[p2][0],
                             points[p2][1],
                             points[p2][2],
                             points[p3][0],
                             points[p3][1],
                             points[p3][2])
                             '''

def generate_sphere( cx, cy, cz, r, step ):
    points = []

    rot_start = 0
    rot_stop = step
    circ_start = 0
    circ_stop = step

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(step)
        for circle in range(circ_start, circ_stop+1):
            circ = circle/float(step)

            x = r * math.cos(math.pi * circ) + cx
            y = r * math.sin(math.pi * circ) * math.cos(2*math.pi * rot) + cy
            z = r * math.sin(math.pi * circ) * math.sin(2*math.pi * rot) + cz

            points.append([x, y, z])
            #print 'rotation: %d\tcircle%d'%(rotation, circle)
    return points

def add_torus(polygons, cx, cy, cz, r0, r1, step ):
    points = generate_torus(cx, cy, cz, r0, r1, step)

    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step

    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):

            p0 = lat * step + longt;
            if (longt == (step - 1)):
                p1 = p0 - longt;
            else:
                p1 = p0 + 1;
            p2 = (p1 + step) % (step * step);
            p3 = (p0 + step) % (step * step);

            add_polygon(polygons,
                        points[p0][0],
                        points[p0][1],
                        points[p0][2],
                        points[p3][0],
                        points[p3][1],
                        points[p3][2],
                        points[p2][0],
                        points[p2][1],
                        points[p2][2] )
            add_polygon(polygons,
                        points[p0][0],
                        points[p0][1],
                        points[p0][2],
                        points[p2][0],
                        points[p2][1],
                        points[p2][2],
                        points[p1][0],
                        points[p1][1],
                        points[p1][2] )


def generate_torus( cx, cy, cz, r0, r1, step ):
    points = []
    rot_start = 0
    rot_stop = step
    circ_start = 0
    circ_stop = step

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(step)
        for circle in range(circ_start, circ_stop):
            circ = circle/float(step)

            x = math.cos(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cx;
            y = r0 * math.sin(2*math.pi * circ) + cy;
            z = -1*math.sin(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cz;

            points.append([x, y, z])
    return points


def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy
    i = 1

    while i <= step:
        t = float(i)/step
        x1 = r * math.cos(2*math.pi * t) + cx;
        y1 = r * math.sin(2*math.pi * t) + cy;

        add_edge(points, x0, y0, cz, x1, y1, cz)
        x0 = x1
        y0 = y1
        i+= 1

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):

    xcoefs = generate_curve_coefs(x0, x1, x2, x3, curve_type)[0]
    ycoefs = generate_curve_coefs(y0, y1, y2, y3, curve_type)[0]

    i = 1
    while i <= step:
        t = float(i)/step
        x = t * (t * (xcoefs[0] * t + xcoefs[1]) + xcoefs[2]) + xcoefs[3]
        y = t * (t * (ycoefs[0] * t + ycoefs[1]) + ycoefs[2]) + ycoefs[3]
        #x = xcoefs[0] * t*t*t + xcoefs[1] * t*t + xcoefs[2] * t + xcoefs[3]
        #y = ycoefs[0] * t*t*t + ycoefs[1] * t*t + ycoefs[2] * t + ycoefs[3]

        add_edge(points, x0, y0, 0, x, y, 0)
        x0 = x
        y0 = y
        i+= 1


def draw_lines( matrix, screen, zbuffer, color ):
    if len(matrix) < 2:
        print 'Need at least 2 points to draw'
        return

    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   matrix[point][2],
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   matrix[point+1][2],
                   screen, zbuffer, color)
        point+= 2

def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)

def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )



def draw_line( x0, y0, z0, x1, y1, z1, screen, zbuffer, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        zt = z0
        x0 = x1
        y0 = y1
        z0 = z1
        x1 = xt
        y1 = yt
        z1 = zt

    x = x0
    y = y0
    z = z0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)
    wide = False
    tall = False

    if ( abs(x1-x0) >= abs(y1 - y0) ): #octants 1/8
        wide = True
        loop_start = x
        loop_end = x1
        dx_east = dx_northeast = 1
        dy_east = 0
        d_east = A
        distance = x1 - x + 1
        if ( A > 0 ): #octant 1
            d = A + B/2
            dy_northeast = 1
            d_northeast = A + B
        else: #octant 8
            d = A - B/2
            dy_northeast = -1
            d_northeast = A - B

    else: #octants 2/7
        tall = True
        dx_east = 0
        dx_northeast = 1
        distance = abs(y1 - y) + 1
        if ( A > 0 ): #octant 2
            d = A/2 + B
            dy_east = dy_northeast = 1
            d_northeast = A + B
            d_east = B
            loop_start = y
            loop_end = y1
        else: #octant 7
            d = A/2 - B
            dy_east = dy_northeast = -1
            d_northeast = A - B
            d_east = -1 * B
            loop_start = y1
            loop_end = y

    dz = (z1 - z0) / distance if distance != 0 else 0

    while ( loop_start < loop_end ):
        plot( screen, zbuffer, color, x, y, z )
        if ( (wide and ((A > 0 and d > 0) or (A < 0 and d < 0))) or
             (tall and ((A > 0 and d < 0) or (A < 0 and d > 0 )))):

            x+= dx_northeast
            y+= dy_northeast
            d+= d_northeast
        else:
            x+= dx_east
            y+= dy_east
            d+= d_east
        z+= dz
        loop_start+= 1
    plot( screen, zbuffer, color, x, y, z )
