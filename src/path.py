'''
@author: dibyendu das

Here all the global file paths are stored
'''

import os, sys

BasePath = os.path.abspath(os.path.join(os.path.realpath(os.path.dirname(sys.argv[0])), '..'))
HomePath = os.getenv("HOME")
LicensePath = os.path.abspath(os.path.join(BasePath, './license/COPYING'))
AboutLogoPath = os.path.abspath(os.path.join(BasePath, './resource/pixmap/about.png'))
OutputIconPath = os.path.abspath(os.path.join(BasePath, './resource/pixmap/output.png'))
InputIconPath = os.path.abspath(os.path.join(BasePath, './resource/pixmap/input.png'))
OutputLogoPath = os.path.abspath(os.path.join(BasePath, './resource/logo.png'))
