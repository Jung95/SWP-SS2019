import requests  # import requests module
import time #import time module
import json
import urllib.request

def actualMatchday():
    ''' 
    Method needs an Internet access
    Data based on 'https://www.openligadb.de/api/getmatchdata/bl1'
        
    Returns: 
        - actualMatchday() returns an int which correspodend with the actual matchday of the Bundesliga
        - or an Error Message when the Matchdays of the matches differs
    '''
    
    url = 'https://www.openligadb.de/api/getmatchdata/bl1'
    opener = urllib.request.urlopen(url)
    data = json.load(opener)

    match1 = data[0]['Group']
    groupID = match1['GroupOrderID']
    
    for x in range(1, 9):
        match1 = data[x]['Group']
        if match1['GroupOrderID'] != groupID:
            break
            print ('unexpected Matchday diffrence')
        else: 
            continue
    print(groupID)