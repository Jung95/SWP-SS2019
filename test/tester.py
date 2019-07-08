import csv

def crawlTest(startYear, startDay, endYear, endDay):
    '''
    This methods tests if the current csv data has the expected length.
    The length correspodens with the number of matches in this time period.
    
        Args: 
            startYear (int): Start Year to test. 
            startDay (int): Start Matchday to test. 
            endYear (int): End Year to test. 
            endDay (int): End Matchday to test. 
        
        return: 
            bool: True if successful, false otherwise
    
    '''
    expectedLines = ((34-startDay+1) + (endYear-startYear-1)*34 + endDay)*9
    
    filename = str(startDay) + '_' + str(startYear) + '_' + str(endDay) + '_' + str(endYear) + '.csv'
    f = open(filename, 'r', encoding='utf-8', newline='')
    rdr = csv.reader(f)
    value = len(list(rdr))
    if value == expectedLines:
        print ('Found all Matches')
        return True
    else:
        print('Found '+ str(value) + ' of ' + str(expectedLines) + ' Matches')
        return False
