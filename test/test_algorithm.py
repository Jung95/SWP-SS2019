import getBundes
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
    minialgo.setDate(2019,5,2018,5,2019)
    assert minialgo.setHisto(), "Dates are the wrong way arround"
    minialgo.setDate(2018,5,2018,6,2019)
    minialgo.setHisto()
    assert os.path.isfile("5_2018_6_2018.csv"), "there is no CSV file"
    assert minialgo.maxGoal==2, "maxGoal not detected correctly"
    assert minialgo.histo == [{'1. FC Köln': [0, 0, 0],
                               '1. FC Union Berlin': [0, 0, 0],
                               '1. FSV Mainz 05': [1, 0, 0],
                               'Bayer Leverkusen': [0, 0, 1],
                               'Borussia Dortmund': [0, 0, 0],
                               'Borussia Mönchengladbach': [1, 0, 0],
                               'Eintracht Frankfurt': [0, 0, 0],
                               'FC Augsburg': [0, 0, 1],
                               'FC Bayern': [1, 0, 0],
                               'FC Schalke 04': [0, 1, 0],
                               'Fortuna Düsseldorf': [1, 0, 0],
                               'Hertha BSC': [0, 0, 1],
                               'RB Leipzig': [0, 0, 0],
                               'SC Freiburg': [1, 0, 0],
                               'SC Paderborn 07': [0, 0, 0],
                               'TSG 1899 Hoffenheim': [1, 0, 0],
                               'VfL Wolfsburg': [0, 1, 0],
                               'Werder Bremen': [0, 0, 1]},
                              {'1. FC Köln': [0, 0, 0],
                               '1. FC Union Berlin': [0, 0, 0],
                               '1. FSV Mainz 05': [1, 0, 0],
                               'Bayer Leverkusen': [1, 0, 0],
                               'Borussia Dortmund': [1, 0, 0],
                               'Borussia Mönchengladbach': [0, 1, 0],
                               'Eintracht Frankfurt': [1, 0, 0],
                               'FC Augsburg': [1, 0, 0],
                               'FC Bayern': [1, 0, 0],
                               'FC Schalke 04': [1, 0, 0],
                               'Fortuna Düsseldorf': [0, 0, 0],
                               'Hertha BSC': [1, 0, 0],
                               'RB Leipzig': [1, 0, 0],
                               'SC Freiburg': [1, 0, 0],
                               'SC Paderborn 07': [0, 0, 0],
                               'TSG 1899 Hoffenheim': [0, 0, 0],
                               'VfL Wolfsburg': [1, 0, 0],
                               'Werder Bremen': [0, 0, 0]}], "Histogram not filled correctly"

      
