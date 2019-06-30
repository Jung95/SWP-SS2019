import pytest
import miniAlgo

minialgo = miniAlgo.Algorithmus()

def test_init():
    """Test for right initialisation of variables
    """
    assert minialgo.startYear==0, "startYear initialised wrong"
    assert minialgo.startDay==0, "startDay initialised wrong"
    assert minialgo.endYear==0, "endYear initialised wrong"
    assert minialgo.endDay==0, "endDay initialised wrong"
    assert minialgo.nowYear==0, "nowYear initialised wrong"
    assert len(minialgo.histo)==0, "histogram not initialised emtpy"
    assert minialgo.maxGoal==0, "maxGoal initialised wrong"
    
def test_setDate():
    minialgo.setDate(2018,5,2018,6,2019)
    assert minialgo.startYear==2018, "fail"
