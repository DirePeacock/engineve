import os
import sys
import pathlib
basedir = pathlib.Path(__file__).parent.parent
srcdir = basedir / 'src' 
vegamedir = basedir / 'src' / 'vegame'

sys.path.append(str(srcdir))
sys.path.append(str(vegamedir))