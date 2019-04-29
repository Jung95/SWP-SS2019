from urllib.request import urlopen  # import urlopen module
import os #import os module
import time #import time module

print('Start year?')
startyear = int(input()) # set the start year to download
now = time.gmtime(time.time()) # get the current time
nowyear = now.tm_year  # get the current year from  current time

try: # if there isnt the Origin Directory, then make that
    if not(os.path.isdir('origin')): 
        os.makedirs(os.path.join('origin'))
except OSError as e:
    raise

for year in range(startyear, nowyear + 1): # from Startyear to nowyear
    str_year =str(year) # convert year int to str
    try:
        if not(os.path.isdir('origin/'+ str_year)):  # if there isnt the years Directory, then make that
            os.makedirs(os.path.join('origin/'+str_year))
    except OSError as e:
        raise
    
    for gameday in range(34): # total 34 Game
        str_gameday = str(gameday+1)  # day year int to str and plus 
        url = 'https://www.openligadb.de/api/getmatchdata/bl1/' + str_year +'/' + (str_gameday) # set he URL
        target_file = 'origin/' + str_year + '/'+str_gameday+'.xml'

        if (year < nowyear and os.path.exists(target_file)): # if we have data of last years already, then skip
            pass
        else:
            with urlopen(url) as res:  # Open URL
                res_data = res.read()
            with open(target_file, 'wb') as f:
                f.write(res_data)






