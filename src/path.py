'''
@author: dibyendu das

Here all the global file paths are stored
'''

import os, sys

BASE_PATH = os.path.abspath(os.path.join(os.path.realpath(
                       os.path.dirname(sys.argv[0])), '..'))
HOME_PATH = os.getenv("HOME")
LICENSE_PATH = os.path.abspath(os.path.join(BASE_PATH, './license/COPYING'))
ABOUT_LOGO_PATH = os.path.abspath(os.path.join(BASE_PATH,
                            './resource/pixmap/about.png'))
OUTPUT_ICON_PATH = os.path.abspath(os.path.join(BASE_PATH,
                           './resource/pixmap/output.png'))
INPUT_ICON_PATH = os.path.abspath(os.path.join(BASE_PATH,
                            './resource/pixmap/input.png'))
OUTPUT_LOGO_PATH = os.path.abspath(os.path.join(BASE_PATH,
                                    './resource/logo.png'))
