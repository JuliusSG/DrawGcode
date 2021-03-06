# requires  Python 3.6.7
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
import math
import sys

warnings.filterwarnings("ignore")  # remove deprecation warnings
plt.rcParams['toolbar'] = 'None'  # remove stock matplotlib toolbar


# Author and information
def print_startup_message():
    print("DrawGcode v0.1b by Marcus Voß\nhttps://git.io/fhTYj\n")
    print("--------------------------------------------")


# print a syntax error if something cant be interpreted
def syntax_error():
    print("Error: invalid syntax!\n\n");


# return the right color based on the pen variable
def linecolor(pen):
    if pen:
        c = "blue"
    else:
        c = "grey"
    return c


# return the target angle (in degrees) to a point on a circle seen from the center of the circle. dx,dy: relative coordinates of the point from the center. r: Radius of the circle.
def point_angle(dx, dy, r):
    if dy > 0 and dx > 0:
        angle = math.asin(dy / r)
    elif dy > 0 and dx <= 0:
        angle = math.pi / 2 + math.asin(math.fabs(dx) / r)
    elif dy <= 0 and dx < 0:
        angle = math.pi + math.asin(math.fabs(dy) / r)
    else:
        angle = math.pi * 1.5 + math.asin(math.fabs(dx) / r)
    return angle * (180 / math.pi)


# return the key (value) from the given command f.e.  readKey("G1 X10",'X') returns 10
def readKey(command, key):
    if key in command:
        value = ""
        temp = command[command.find(key) + 1:]
        for c in temp:
            if not c.isdigit() and c not in {'.', '-'}:
                break
            else:
                value += c;
        if value == "":
            syntax_error()
            return -1
        return float(value)
    else:
        print("ERROR: key:  "+key +" This should not happen?\n\n")
        return -1


# read a file filename and plot its content
def file_reader(filename):
    x = 0
    y = 0
    pen = False
    print("opening: " + filename + " ...")
    try:
        file = open(filename, "r")
    except IOError:
        print("ERROR: FAILED TO OPEN THE FILE\n\n")
        return -1
    for line in file:
        if ";" in line:
            line = line.split(";")[0]
        if not line :
            continue
        print(repr(line))  # print line content including "\n"
        if line[0] not in ['G','M']:
            print("WARNING: THE PREVIOUS LINE APPEARS TO BE WRONG OR CONTAINS UNSUPPORTED COMMANDS\n\n")
        if "G28" in line:
            plt.plot([x, 0], [y, 0], color=linecolor(pen))
            x = 0
            y = 0
        elif "M280" in line:
            if "P0" in line and "S" in line:
                s = readKey(line, "S")
                if s >= 40:
                    pen = True;
                elif s == 0:
                    pen = False;
                else:
                    syntax_error()
        elif "G1" in line:
            tx = x
            ty = y
            if "X" in line:
                tx = readKey(line, "X")
            if "Y" in line:
                ty = readKey(line, "Y")

            if x != None and y != None:
                plt.plot([x, tx], [y, ty], color=linecolor(pen))
                x = tx
                y = ty
        elif "G2" in line or "G3" in line:
            tx = x
            ty = y
            i = 0
            j = 0
            if "X" in line:
                tx = readKey(line, "X")
            if "Y" in line:
                ty = readKey(line, "Y")
            if "I" in line:
                i = readKey(line, "I")
            if "J" in line:
                j = readKey(line, "J")
            if "Z" in line:
                z = readKey(line, "Z")
                if z >= 40:
                    pen = True;
                elif z == 0:
                    pen = False;
                else:
                    syntax_error()
            centerX = x + i
            centerY = y + j
            radius = math.sqrt((centerX - x) ** 2 + (centerY - y) ** 2) #distance between start point and center point
            radius2 = math.sqrt((centerX - tx) ** 2 + (centerY - ty) ** 2) #distance beteen end point and center point
            if radius != radius2: #to reach the end point from the starting point both radii have to be equal
                syntax_error()
                return -1
            s1 = point_angle(x - centerX, y - centerY, radius) #angle from the center point  to the start point
            s2 = point_angle(tx - centerX, ty - centerY, radius) #angle from the center point  to the end point
            if "G2" in line:
                pac = mpatches.Arc([centerX, centerY], 2 * radius, 2 * radius, angle=0, theta1=s2, theta2=s1,
                                   color=linecolor(pen))
            else:
                pac = mpatches.Arc([centerX, centerY], 2 * radius, 2 * radius, angle=0, theta1=s1, theta2=s2,
                                   color=linecolor(pen))
            ax = plt.gca()
            ax.add_patch(pac)
            x = tx
            y = ty
    plt.xlim(0, 390)    #the maximum x-dimensions 
    plt.ylim(0, 310)    #the maximum y-dimensions 
    plt.axes().set_aspect("equal")
    plt.show()


def main():
    print_startup_message()
    if len(sys.argv) >1:
        filename = sys.argv[1]
        file_reader(filename)
    else:
        print("ERROR: Please specify a filename as an argument when running DrawGcode f.e DrawGcode.exe \"filename.gcode\"")


if __name__ == "__main__":
    main()
