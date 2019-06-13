#from script import run
import sys, time
import multiprocessing as mp
from script import run
from display import *
from Sphere import *
from Vector import *
from Ray import *
from Light import *
from functools import reduce
from Triangle import *
from draw import *


if len(sys.argv) == 2:
    run(sys.argv[1])
elif len(sys.argv) == 1:
    run(raw_input("please enter the filename of an mdl script file: \n"))
else:
    print "Too many arguments."
