import mdl
from display import *
from matrix import *
from draw import *

"""======== first_pass( commands ) ==========

  Checks the commands array for any animation commands
  (frames, basename, vary)

  Should set num_frames and basename if the frames
  or basename commands are present

  If vary is found, but frames is not, the entire
  program should exit.

  If frames is found, but basename is not, set name
  to some default value, and print out a message
  with the name being used.
  ==================== """
def first_pass( commands ):

    collection = {}
    name = ''
    num_frames = 1
    i = 0
    while i < len(commands):
        if (commands[i]['op'] == 'frames') or (commands[i]['op'] == 'basename') or (commands[i]['op'] == 'vary'):
            collection[commands[i]['op']] = commands[i]['args']
            #print("Statement Reached")
        i+= 1
    #print(collection)
    if ('frames' in collection) and ('basename' in collection):
        num_frames = int(collection['frames'][0])
        #print num_frames
        name = collection['basename'][0]
        #print name
    elif ('vary' in collection) and not(('frames' in collection) and ('basename' in collection)):
        print("Error: Frames not found")
        exit()
    elif ('frames' in collection):
        name = 'animation'
        print("The name being used is: animation")
        num_frames = int(collection['frames'][0])
    return(name, num_frames)

"""======== second_pass( commands ) ==========

  In order to set the knobs for animation, we need to keep
  a seaprate value for each knob for each frame. We can do
  this by using an array of dictionaries. Each array index
  will correspond to a frame (eg. knobs[0] would be the first
  frame, knobs[2] would be the 3rd frame and so on).

  Each index should contain a dictionary of knob values, each
  key will be a knob name, and each value will be the knob's
  value for that frame.

  Go through the command array, and when you find vary, go
  from knobs[0] to knobs[frames-1] and add (or modify) the
  dictionary corresponding to the given knob with the
  appropirate value.
  ===================="""
def second_pass( commands, num_frames ):
    frames = [ {} for i in range(num_frames) ]

    for command in commands:
        if command['op'] == 'vary':
            # print(command)
            args = command['args']
            knobName = command['knob']
            startFrame = int(args[0])
            endFrame = int(args[1])
            startVal = args[2]
            endVal = args[3]
            frames[startFrame][knobName] = startVal
            frames[endFrame][knobName] = endVal
            delta = (endVal - startVal) / (endFrame - startFrame)
            for frame in range(startFrame + 1, endFrame):
                frames[frame][knobName] = startVal + delta * (frame - startFrame)

    return frames


def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    (name, num_frames) = first_pass(commands)
    frames = second_pass(commands, num_frames)

    #for i in frames:
        #print i

    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    doDisplay = False
    lightlst = [Light(Vector([-500, 250, 0]), Vector([1770000, 1560000, 2170000])),
                Light(Vector([250, 190, 100]), Vector([1190, 1580, 2030])),
                Light(Vector([400, 400, 100]), Vector([25500, 10500, 9700])),
                Light(Vector([750, -250, 100]), Vector([2550000, 2550000, 2550000]))]

    maxDigits = "%0" + str(int(math.log(num_frames)) + 1) + "d"

    for frame in range(num_frames):
        for command in commands:
            print command
            c = command['op']
            args = command['args']
            knob_value = 1
            if 'knob' in command and command['knob'] != None and command['knob'] in frames[frame]:
                knob_value = frames[frame][command['knob']]

            if c == 'box':
                if command['constants']:
                    reflect = command['constants']
                add_box(tmp,
                        args[0], args[1], args[2],
                        args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                #draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'

            elif c == 'sphere':
                if command['constants']:
                    reflect = command['constants']
                add_sphere(tmp,
                           args[0], args[1], args[2], args[3], step_3d)
                tmp[-1].applyMatrix(stack[-1])
                #print(type(tmp[len(tmp)-1].o))
                #print(tmp[len(tmp)-1].o)
                #matrix_mult( stack[-1], tmp[len(tmp)-1].o.direction)
                #draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                #tmp = []
                reflect = '.white'

            elif c == 'torus':
                if command['constants']:
                    reflect = command['constants']
                add_torus(tmp,
                          args[0], args[1], args[2], args[3], args[4], step_3d)
                matrix_mult( stack[-1], tmp )
                #draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'line':
                add_edge(tmp,
                         args[0], args[1], args[2], args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                draw_lines(tmp, screen, zbuffer, color)
                tmp = []
            elif c == 'move':
                tmp = make_translate(args[0] * knob_value, args[1] * knob_value, args[2] * knob_value)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'scale':
                tmp = make_scale(args[0] * knob_value, args[1] * knob_value, args[2] * knob_value)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'rotate':
                theta = args[1] * (math.pi/180) * knob_value
                if args[0] == 'x':
                    tmp = make_rotX(theta)
                elif args[0] == 'y':
                    tmp = make_rotY(theta)
                else:
                    tmp = make_rotZ(theta)
                matrix_mult( stack[-1], tmp )
                stack[-1] = [ x[:] for x in tmp]
                tmp = []
            elif c == 'push':
                stack.append([x[:] for x in stack[-1]] )
            elif c == 'pop':
                stack.pop()
            elif c == 'display':
                doDisplay = True
            elif c == 'save':
                save_extension(screen, args[0])

            #Comes at the end so that we can do ray tracing stuff
        print("Printing contents of tmp array in script: ")
        # retrieve_polygons(tmp)
        # print(tmp)
        # draw_polygons(tmp,screen,zbuffer,view,ambient,light,symbols,reflect)
        drawNoPerspective(screen,zbuffer, tmp, lightlst)
        scaleColors(screen,0)
        if doDisplay:
            display(screen)
        doDisplay = False


        if num_frames != 1:
            save_extension(screen, 'anim/' + name + maxDigits%frame)
            tmp = new_matrix()
            ident( tmp )
            stack = [ [x[:] for x in tmp] ]
            screen = new_screen()
            zbuffer = new_zbuffer()
            tmp = []
        # end operation loop
    if num_frames != 1:
        make_animation(name)
