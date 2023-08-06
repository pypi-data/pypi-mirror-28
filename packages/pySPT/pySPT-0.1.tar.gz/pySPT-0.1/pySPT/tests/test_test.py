from __future__ import division, print_function

import numpy as np
import pytest

from pySPT.tools.const import EULEUR_MASCHERONI_CONST as CONST

def test_const():
    assert CONST > 0  
