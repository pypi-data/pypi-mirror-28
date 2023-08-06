import pytest

def test_ImportShamrock():
    from PyAndor import ShamRockController
    try:
        controller = ShamRockController()
    except OSError:
        pass

def test_ImportCamera():
    from PyAndor import AndorCamera
    try:
        camera = AndorCamera()
    except OSError:
        pass    