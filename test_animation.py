from utils import lerp
from easings_functions import *

# a + (b - a) * easing(t)

def test_lerp_linear():
    assert lerp(0, 100, 0.5, linear) == 50

def test_lerp_easeIn():
    assert lerp(0,100,0.5, easeIn) == 12.5

def test_lerp_easeOut():
    assert lerp(0,100,0.5, easeOut) == 75

