import os
import sys
import pathlib
basedir = pathlib.Path(__file__).parent.parent
srcdir = basedir / 'src'
enginevedir = srcdir / 'engineve'

sys.path.append(str(srcdir))
sys.path.append(str(enginevedir))