import json
import urllib.request

import bs4 as bs

from server.mockdraft.model.prospect import ProspectElite
from server.mockdraft.repository.prospect_elite_dao import ProspectEliteDao

year = "2022"

hp_url = [f'https://www.eliteprospects.com/draft-center/{year}/sportsnet', 0]  # hp -> tsn
fc_url = [f'https://www.eliteprospects.com/draft-center/{year}/fchockey', 1]
iss_url = [f'https://www.eliteprospects.com/draft-center/{year}/neutral-zone', 2]
mh_url = [f'https://www.eliteprospects.com/draft-center/{year}/mckeen-s-hockey', 3]
elite_url = [f'https://www.eliteprospects.com/draft-center/{year}/eliteprospects.com', 4]


def getProspectFromRow(i, data):
    if len(data) == 9:
        p = ProspectElite()

        name_position = getNamePositionTupple(data[1])
        p.name = name_position[0]
        p.position = name_position[1]

        if(i == 0): p.hp = data[0]
        if(i == 1): p.fc = data[0]
        if(i == 2): p.iss = data[0]
        if(i == 3): p.mh = data[0]
        if(i == 4): p.elite = data[0]

        p.league = data[3]
        p.team = data[2]
        p.gp = data[4]
        p.g = data[5]
        p.a = data[6]
        p.p = data[7]
        p.pim = data[8]

        return p
    return None


def getNamePositionTupple(name_position):
    new_name_position = name_position.split(" (")
    return new_name_position[0], new_name_position[1].replace(')', '')


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
            ProspectEliteDao(year).insertOrUpdateProspectElite(prospect)

def dataToFile(data):
    with open('../data2021.json', 'w', encoding='utf-8') as f:
        json.dump([item.__dict__ for item in data], f, ensure_ascii=False, indent=4)

prospects = (
    getProspectFromEliteUrl(hp_url) +
    getProspectFromEliteUrl(fc_url) +
    getProspectFromEliteUrl(iss_url) +
    getProspectFromEliteUrl(mh_url) +
    getProspectFromEliteUrl(elite_url)
)

if __name__ == '__main__':

    ProspectEliteDao(year).initProspectEliteTable()
    insertProspectToDb(prospects)

    allProspects = ProspectEliteDao(year).getAllProspects()

    for prospect in allProspects:
        ProspectEliteDao(year).updateProspectEliteAvgRank(prospect)

    dataToFile(allProspects)
