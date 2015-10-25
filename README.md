MofDS-GUI


Guide to the GUI:
This GUI is written completely in Python. The following modules are
installed:
-numpy
-matplotlib
(otional pylab, scipy...)

To install them for respected OS, simply google it as it is very ea-
sy to find guides.


Using the GUI is simple. On the left you have buttons for different
built-in functions. To select the function, simply press the button
AND you have to remove the cursor from the button [matplotlib logic].

Bottom of the plot are the controls of the constants that are in a 
map function.

Also it's best to have it in windowed full screen mode, because of the font.


Adding a map:
It is fairly simple all you have to edit is:

#CONSTANTS FOR YOUR FUNCTION
In the Maps class you have to add a key - value to the slider dictionary.
This dictionary contains the names of your constants and additionaly it
provides the number for your map.
Example:

'YourMapName' : [and array containing string either names or letters],


#MODUL#
The same for the modul dictionary. It simply contains the boundary of the
phase space. Cation: Right now it provides the space from [0, <your_boundary>]
Example:
'YourMapName' : value,


#REGISTERING IT IN

in the Maps.__init__ you have to input an entry for the self.maps dictionary. It
is basically linking YourMapName to self.YourMapFunction.

Example:
'YourMapName' : self.YourMapFunction


#INPUTING THE FUNCTION

In the class you have to create your function:

def YourMapFunction(self, data):

The data contains: q, p, your defined constants.
To access them write:

data['q'], data['p'], data['Name_of_a_Constant'],...

Manipulate the data however you like within the boundaries of this program.
The return values of this map must be: q,p



