Pick up the pieces
==================

Entry in PyWeek #21  <http://www.pyweek.org/21/>
URL: http://pyweek.org/e/pickupthepieces
Team: telecoda_2016
Members: telecoda
License: see LICENSE.txt

Running on OSX
--------------
mkvirtualenv pickupthepieces
pip install hg+http://bitbucket.org/pygame/pygame
pip install pylygon
pip install numpy

python run_game.py


Running the Game
----------------

On Windows or Mac OS X, locate the "run_game.pyw" file and double-click it.

Othewise open a terminal / console and "cd" to the game directory and run:

  python run_game.py


How to Play the Game
--------------------

Put the pictures back together

Move the cursor around the screen with the mouse.

Click mouse to select pieces to move.

When selected pieces can be rotated left or right, but using the 'A' and 'D' keys or 'LEFT' and 'RIGHT' keys.


References
————
Apocalypse Font
http://californiafonts.com/download/font/3332

Siren
http://www.freesound.org/people/fmagrao/sounds/80761/

Music from
https://ourmusicbox.com/category/orchestral/page/4/

Photos from

https://www.google.co.uk/search?q=world+war+2+london+photos&safe=off&biw=2560&bih=1322&tbm=isch&tbo=u&source=univ&sa=X&sqi=2&ved=0ahUKEwi68LC4nKnLAhWiApoKHcjSDOcQsAQIGw#safe=off&tbs=sur:fm&tbm=isch&q=world+war+2+london+the+blitz

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

