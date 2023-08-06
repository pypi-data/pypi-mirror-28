from __future__ import (absolute_import)

from matplotlib import rc, rcParams
rc('text', usetex=True)
rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]

from . import catalog
from . import decorators
from . import grid
from . import integrals
from . import lensing
from . import multiproc
from . import sourcemapping
from . import spt
from . import tools

__version__ = "0.1.0"

print("-------------------------------------------------------")
print("       d8888b. db    db .d8888. d8888b. d888888b       ")
print("       88  `8D `8b  d8' 88'  YP 88  `8D `~~88~~'       ")
print("       88oodD'  `8bd8'  `8bo.   88oodD'    88          ")
print("       88~~~      88      `Y8b. 88~~~      88          ")
print("       88         88    db   8D 88         88          ")
print("       88         YP    `8888Y' 88         YP          ")
print("-------------------------------------------------------")
print("        Package dedicated to the SPT analysis          ")
print("-------------------------------------------------------")
print("Please read Wertz & Orthen 2017 (submitted to A&A)     ")
print("for a detailed description of the package.             ")
print("                                                       ")
print("The theoretical support of the package can be          ")
print("found in the following papers:                         ")
print("+ Schneider & Sluse 2013                               ")
print("+ Schneider & Sluse 2014                               ")
print("+ Unruh, Schneider & Sluse 2017                        ")
print("+ Wertz, Orthen & Schneider 2017                       ")
print("                                                       ")
