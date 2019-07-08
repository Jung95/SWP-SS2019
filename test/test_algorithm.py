import pytest
import os
import miniAlgo

minialgo = miniAlgo.Algorithmus()

def test_init():
    """Test for right initialisation of variables
    """
    minialgo.__init__()
    assert minialgo.startYear==0, "startYear initialised wrong"
    assert minialgo.startDay==0, "startDay initialised wrong"
    assert minialgo.endYear==0, "endYear initialised wrong"
    assert minialgo.endDay==0, "endDay initialised wrong"
    assert minialgo.nowYear==0, "nowYear initialised wrong"
    assert len(minialgo.histo)==0, "histogram not initialised emtpy"
    assert minialgo.maxGoal==0, "maxGoal initialised wrong"
    
def test_setDate():
    """Test for right setting of variables
    """
    minialgo.setDate(2018,5,2018,6,2019)
    assert minialgo.startYear==2018, "startYear set wrong"
    assert minialgo.startDay==5, "startDay set wrong"
    assert minialgo.endYear==2018, "endYear set wrong"
    assert minialgo.endDay==6, "endDay set wrong"
    assert minialgo.nowYear==2019, "nowYear set wrong"

def test_setHisto():
    """Test for right histogram initialisation
    """
    minialgo.setDate(2018,5,2018,6,2019)
    minialgo.setHisto()
    assert os.path.isfile("5_2018_6_2018.csv"), "there is no CSV file"
    assert minialgo.maxGoal==2, "maxGoal not detected correctly"
    # test falls daten falsch herum 
    # test für histogram befüllung
    minialgo.setDate(2018,6,2018,5,2019)
    assert os.path.isfile("6_2018_5_2018.csv"), "dates are invalid"


