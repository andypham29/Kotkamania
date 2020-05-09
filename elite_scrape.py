import requests
from enum import Enum
import bs4 as bs
import urllib.request
import json


from model.prospect import ProspectElite
from repository.prospect_elite_dao import ProspectEliteDao

hp_url = ['https://www.eliteprospects.com/draft-center/2020/hockeyprospect.com', 0]
fc_url = ['https://www.eliteprospects.com/draft-center/2020/future-considerations', 1]
iss_url = ['https://www.eliteprospects.com/draft-center/2020/iss-hockey', 2]
mh_url = ['https://www.eliteprospects.com/draft-center/2020/mckeen-s-hockey', 3]
elite_url = ['https://www.eliteprospects.com/draft-center/2020/eliteprospects.com', 4]

def getProspectFromRow(i, data):
    if len(data) == 9:
        p = ProspectElite()

        p.name_position = data[1]

        if(i == 0): p.hp = data[0]
        if(i == 1): p.fc = data[0]
        if(i == 2): p.iss = data[0]
        if(i == 3): p.mh = data[0]
        if(i == 4): p.elite = data[0]

        # print(json.dumps(p.__dict__))
        return p
    return None

def getProspectFromEliteUrl(url):
    source = urllib.request.urlopen(url[0]).read()

    soup = bs.BeautifulSoup(source,'lxml')
    print("python scraping elite ...")
    # print(type(output_row))

    data = []
    table = soup.find('table', attrs={'class':'table table-striped players table-sortable highlight-stats'})

    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        # list comprehension: [item.transformation for item in list] -> item.transformation becomes an element of a list
        cols = [item.text.strip() for item in cols]
        data.append([item for item in cols if item])

    prospectList = []
    for item in data:
        p = getProspectFromRow(url[1], item)
        if p != None:
            prospectList.append(p)
    return prospectList

def insertProspectToDb(prospects):
    for prospect in prospects:
            ProspectEliteDao().insertOrUpdateProspectElite(prospect)

def dataToFile(data):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# prospects = (
#     getProspectFromEliteUrl(hp_url) +
#     getProspectFromEliteUrl(fc_url) +
#     getProspectFromEliteUrl(iss_url) +
#     getProspectFromEliteUrl(mh_url) +
#     getProspectFromEliteUrl(elite_url)
# )
#
# ProspectEliteDao().initProspectEliteTable()
# insertProspectToDb(prospects)


dataToFile(ProspectEliteDao().getAllProspects())
