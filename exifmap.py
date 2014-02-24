__author__ = 'khanta'
__author__ = 'tschlein'
# https://code.google.com/p/pygmaps/
#TODO Add code to skip HashMark ---> complete
#Import pygmaps
#TODO Add command line arguments --> complete
#TODO Add check if long or lat is missing
#TODO Add check if columns are incomplete
#TODO Kick out total plotted items --> Complete
#TODO
import sys
import datetime
import string
import pygmaps
import argparse
import codecs


debug = 0
coordinates = []
hashes = []


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
    try:
        global hashes
        lineOut = lineIn.split(',')
        if str(lineOut[1:2]) != ' ':
            if str(lineOut[2:3]) != '':
                temp = str(lineOut[0:1])
                temp1 = temp.split('\\t')
                hashes.append(temp1[1:2])
                if str((temp1[1:2])) not in hashes:
                    #Ref: http://stackoverflow.com/questions/10009753/python-dealing-with-mixed-encoding-files
                    #Ref: http://stackoverflow.com/questions/7555335/how-to-convert-a-string-from-cp1251-to-utf8
                    c2 = lineOut[1:2].pop().encode('utf-8')
                    if (c2) != b'-':
                        c2 = float(c2)
                        c1 = lineOut[2:3].pop().encode('utf-8')
                        #print(c2, c1)
                        if (c1) != b'-':
                            c1 = float(c1)
                        else:
                            c1 = 0
                    else:
                        c1 = 0
                        c2 = 0
    except:
        #print('Error converting value')
        c1 = 0
        c2 = 0
    finally:
        return (c1, c2)


def getMap(file, path, zoom):
    if (debug >= 1):
        print('Entering getMap:')
    if (debug >= 2):
        print('File passed in:' + str(file))
        print('Path passed in:' + str(path))
        print('Zoom Level passed in::' + str(zoom))

    # with open(file, 'r') as f:
    #     while (True):
    #         lineIn =

    f = open(file, 'r')

    lineIn = skipHash(f)

    c1, c2 = latLong(lineIn)
    if (debug >= 2):
        print('\tCoordinates: ' + str(c1) + ' - ' + str(c2))
    mymap = pygmaps.maps(c1, c2, zoom)

    lineIn = f.readline()
    counter = 1
    while lineIn:
        c1, c2 = latLong(lineIn)
        if not (c1 == 0) and not (c2 == 0):
            mymap.addpoint(c1, c2, "#0000FF")
            counter += 1

        lineIn = f.readline()
    mymap.draw(path + '\mymap.html')
    print(counter)


def main(argv):
    try:
        zoom = 16  #default value for zoom if not specified as arg

        global debug
        parser = argparse.ArgumentParser(description="A utility to take GPS coordinates and plot them on a map.",
                                         add_help=True)
        parser.add_argument('-f', '--file', help='The file that contains the GPS coordinates.', required=True)
        parser.add_argument('-p', '--path', help='The path to write the output map to.', required=True)
        parser.add_argument('-z', '--zoom', help='The zoom level, must be in range of 0-15.', required=False)
        parser.add_argument('-d', '--debug', help='The level of debugging.', type=int, required=False)
        parser.add_argument('--version', action='version', version='%(prog)s 1.5')

        args = parser.parse_args()
        if (args.file):
            file = args.file
            with codecs.open(file, 'r', 'ascii'):
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