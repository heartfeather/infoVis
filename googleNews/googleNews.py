# Heartfeather Intelligence, LLC 2019

import requests
import pprint
import json
import datetime

#request one page of results
def requestOnce(keyword, page, pageSize, fromParam):
    
    url = ('https://newsapi.org/v2/everything?'
       'q=' + keyword + '&'
       'from=' + fromParam + '&'
       'sortBy=popularity&'
       'pageSize=' + str(pageSize) + '&'
       'page=' + str(page) + '&'
       'language=en&'
       'apiKey=your_own_Goole_News_API_key')

    response = requests.get(url)
    data = json.loads(response.text)
    
    if data['status'] == 'ok':
        print(data['status'], data['totalResults'], page)
        return data['status'], data['articles'], data['totalResults']
    else:
        return data['status'], [], 0
#end of requestOnce

#-------start of main program body-----------#

#prepare parameters
keyword = 'Apple'
page = 1
pageSize = 100
numDays = 1
d = datetime.datetime.today()
d = d - datetime.timedelta(days = numDays)
fromParam = d.strftime('%Y-%m-%d')

print('Keyword:', keyword, 'From:', fromParam)

#request page no.1
status, results, total = requestOnce(keyword, page, pageSize, fromParam)

#get total number of pages
pages = int(total / pageSize)
if pages * pageSize < total:
    pages += 1

#request each pages starting from page No.2
while page < pages:
    page += 1
    status, tempResults, total = requestOnce(keyword, page, pageSize, fromParam)
    if (status == 'ok'):
        results = [*results, *tempResults]

#developer plan limits results to be 1000
print('total results', len(results))

#display results
for item in results:
    print(item['title'], item['publishedAt'])
    
#save json data to file
outFile = keyword + "_" + fromParam + "_" + str(numDays) + '.json'
with open(outFile, 'w') as output:
    json.dump(results, output)
    
print('done.')
