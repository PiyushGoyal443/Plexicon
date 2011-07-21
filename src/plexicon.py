'''
@author: dibyendu das

The main module. Everything else
has been called from here.
'''

from path import HOME_PATH
import os
if not os.path.exists(HOME_PATH + '/.plexicon/'):
    os.makedirs(HOME_PATH + '/.plexicon/')

import random
THEME_INDEX = random.randint(0, 3)
from interface import run
run(THEME_INDEX)

for dataFile in os.listdir(HOME_PATH + '/.plexicon/'):
    os.remove(HOME_PATH + '/.plexicon/' + dataFile)