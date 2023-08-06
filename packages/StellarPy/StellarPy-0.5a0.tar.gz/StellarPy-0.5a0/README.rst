=========
StellarPy
=========
*StellarPy is a Python library for calculating and modeling the motion of celestial bodies.*

----

Example
-------

.. image:: https://raw.githubusercontent.com/ezinall/StellarPy/master/examples/exmaple.png

Hello Earth
-----------
Here is how a simple modeling looks like in StellarPy:

.. code:: python

   from stellarpy import Star, Body, Make

   SUN = Star('Sun', m=1.98892e30)
   Make(SUN, color=(1, 1, 0, 1))

   EARTH = Body('Earth', major=SUN, m=5.9726e24, a=149598262, e=0.01671022, i=0.00005, w=114.20783,
                O=348.73936, M=358.617)
   Make(EARTH, color=(0, 0, 1, 1))

   if __name__ == '__main__':
       from pyqtgraph.Qt import QtCore, QtGui
       import sys
       if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
           QtGui.QApplication.instance().exec_()

Installation
------------
``pip install stellarpy``

Contact
-------
- `GitHub <https://github.com/ezinall/StellarPy>`_  - Project directory

License
-------
This software is distributed under `BSD License <https://en.wikipedia.org/wiki/BSD_licenses>`_.
Full text of the license is included in `LICENSE.txt <https://github.com/ezinall/StellarPy/blob/master/LICENSE.txt>`_ file.
