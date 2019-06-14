import requests  # import requests module
import time #import time module
import json
import urllib.request

def actualMatchday():
    ''' 
    Method needs an Internet access
    Data based on 'https://www.openligadb.de/api/getmatchdata/bl1'
        
    Returns: 
        actualMatchday() returns an int which correspodend with the actual matchday of the Bundesliga
    '''
    
    url = 'https://www.openligadb.de/api/getmatchdata/bl1'
    opener = urllib.request.urlopen(url)
    data = json.load(opener)

# todo Match 1-9 vergleichen
    match1 = data[0]
    group1 = match1['Group']
#    mtchdte = group['MatchDateTime']  
    
    mtchdy = group1['GroupOrderID']
      
    print(mtchdy)