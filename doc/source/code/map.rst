.. _map-code:

========
Map code
========

This code describes the classes that contains the maps. There are two variants,
one that does not have an input matrix, which I named standard and the other
that can have an image as input (ie Arnold Cat Map).

The main difference is in the usage of the maps. In the standard maps the user
clicks, using mouse, on the plot area and the phase-space will be drawn using
the selected point as the initial position.

In the image maps, the maps contain images as input and therefore any mappings
are done on the image and the user can only iterate mappings and resize/reset
the image as necessary.

.. automodule:: maps
   :members: