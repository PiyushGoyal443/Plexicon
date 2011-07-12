#!/usr/bin/env python
'''
@author: dibyendu das

The main module. Everything else 
is called from here
'''

from path import HomePath
import os
if not os.path.exists(HomePath + '/.plexicon/'):
    os.makedirs(HomePath + '/.plexicon/')

import random
themeIndex = random.randint(0, 3)
from interface import run
run(themeIndex)

for file in os.listdir(HomePath + '/.plexicon/'):
    os.remove(HomePath + '/.plexicon/' + file)
