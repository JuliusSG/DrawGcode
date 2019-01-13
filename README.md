# DrawGcode
A simple program that allows the graphical preview of .gcode files by utilising pythons Pyplot library.
Mainly written for internal use in teaching the workings of G-code.

Since it is written for use with a plotter only 2D G-codes are supported. The z axis instead controls the pen.
A z-coordinate of 0 is interpreted as the pen being in the up position and a z-coordinate greater then 40 is interpreted as the pen being in the down position.

This tool is command line only. 
To use it call the script with the filename of your .gcode as the first parameter e.g. -> python DrawGcode.py example.gcode.



