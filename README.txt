Pick up the pieces
==================

Entry in PyWeek #21  <http://www.pyweek.org/21/>
URL: http://pyweek.org/e/pickupthepieces
Team: telecoda_2016
Members: telecoda
License: see LICENSE.txt

Dependencies
--------------------
pip install pygame
pip install pylygon
pip install numpy


Running the Game
----------------

On Windows or Mac OS X, locate the "run_game.pyw" file and double-click it.

Othewise open a terminal / console and "cd" to the game directory and run:

  python run_game.py


How to Play the Game
--------------------

Put the pictures back together

Move the cursor around the screen with the mouse.

Press the left mouse button to fire the ducks.


Development notes 
-----------------

Creating a source distribution with::

   python setup.py sdist

You may also generate Windows executables and OS X applications::

   python setup.py py2exe
   python setup.py py2app

Upload files to PyWeek with::

   python pyweek_upload.py

Upload to the Python Package Index with::

   python setup.py register
   python setup.py sdist upload

