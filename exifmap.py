__author__ = 'khanta'
__author__ = 'tschlein'
# https://code.google.com/p/pygmaps/
#TODO Add code to skip HashMark ---> complete
#Import pygmaps
#TODO Add command line arguments --> complete
import sys
import datetime
import string
import pygmaps
import argparse

debug = 0

#Skip hash marks at beginning of file
def skipHash(f):
    if (debug >= 1):
        print('Entering skipHash:')
    if (debug >= 2):
        print('File passed in:' + str(f))
    lineIn = f.readline()

    while (1):
        if (lineIn[0] == '#'):
            lineIn = f.readline()
        else:
            return (lineIn)


#Parse out latitude and longitude coordinates from line
def latLong(lineIn):
    lineOut = lineIn.split(',')
    c2 = float(lineOut[1:2].pop())
    c1 = float(lineOut[2:3].pop())

    return (c1, c2)


#Add coordinates to a map
#https://maps.google.com/maps?q=51.5235,-0.0715
def getMap(file, path, zoom):
    if (debug >= 1):
        print('Entering getMap:')
    if (debug >= 2):
        print('File passed in:' + str(file))
        print('Path passed in:' + str(path))
        print('Zoom Level passed in::' + str(zoom))
    f = open(file, 'r')

    lineIn = skipHash(f)

    c1, c2 = latLong(lineIn)
    if (debug >= 2):
        print('\tCoordinates: ' + str(c1) + ' - ' + str(c2))
    mymap = pygmaps.maps(c1, c2, zoom)

    lineIn = f.readline()
    while lineIn:
        c1, c2 = latLong(lineIn)
        #print(c1, c2)
        mymap.addpoint(c1, c2, "#0000FF")

        lineIn = f.readline()
    mymap.draw(path + '\mymap.html')


def main(argv):
    try:
        zoom = 16  #default value for zoom if not specified as arg

        global debug
        parser = argparse.ArgumentParser(description="A utility to take GPS coordinates and plot them on a map.",
                                         add_help=True)
        parser.add_argument('-f', '--file', help='The file that contains the GPS coordinates.', required=True)
        parser.add_argument('-p', '--path', help='The path to write the output map to.', required=True)
        parser.add_argument('-z', '--zoom', help='The zoom level, must be in range of 0-15.', required=False)
        parser.add_argument('-d', '--debug', help='The level of debugging.', required=False)
        parser.add_argument('--version', action='version', version='%(prog)s 1.5')

        args = parser.parse_args()
        if (args.file):
            file = args.file
            with open(file):
                check = True
        if (args.path):
            path = args.path
        if (args.zoom):
            value = int(args.zoom)
            if (value >= 0 and value <= 20):
                zoom = value
            else:
                zoom = 16
        if (args.debug):
            debug = args.debug
        if (debug >= 1):
            print('Entering Main:')
        getMap(file, path, zoom)
    except IOError:
        sys.exit('Error: File ' + str(file) + ' does not exist.')


main(sys.argv[1:])