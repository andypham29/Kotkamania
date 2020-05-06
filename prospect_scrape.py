import requests
from enum import Enum
import bs4 as bs
import urllib.request
from model.prospect import Prospect
from repository.prospect_dao import ProspectDao

category = {
    "NA_P":1,
    "EU_P":2,
    "NA_G":3,
    "EU_G":4
}
class category_enum(Enum):
    NA_P = 1
    EU_S = 2
    NA_G = 3
    EU_G = 4

class prospect_enum(Enum):
    final_rank = 0
    mid_rank = 1
    player = 2
    height = 3
    weight = 4
    position = 5
    team = 6
    league = 7

def getProspectFromRow(row):
    if len(row) == 7:
        row.insert(0, "")
        
    return Prospect(
        rank = row[prospect_enum.final_rank.value],
        player_name = row[prospect_enum.player.value],
        height = row[prospect_enum.height.value],
        weight = row[prospect_enum.weight.value],
        position = row[prospect_enum.position.value],
        team = row[prospect_enum.team.value],
        league = row[prospect_enum.league.value]
    )

def getProspectUrl(category, page, year):
    return f"http://www.nhl.com/ice/draftprospectbrowse.htm?cat={category}&sort=finalRank&year={year}&pg={page}"

def getProspectsFromUrl(url):
    source = urllib.request.urlopen(url).read()

    soup = bs.BeautifulSoup(source,'lxml')
    print("python scraping...")
    # print(type(output_row))

    data = []
    table = soup.find('table', attrs={'class':'stat-table'})

    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        # list comprehension: [item.transformation for item in list] -> item.transformation becomes an element of a list
        cols = [item.text.strip() for item in cols]
        data.append([item for item in cols if item])

    return data
def insertProspectToDb(prospects):
    for prospect in prospects:
        if (len(prospect) >= 7):
            # print(getProspectFromRow(prospect))
            ProspectDao().createProspect(getProspectFromRow(prospect))

urlNAP1 = getProspectUrl(category.get("NA_P"), 1, 2020)
urlNAP2 = getProspectUrl(category.get("NA_P"), 2, 2020)
urlNAP3 = getProspectUrl(category.get("NA_P"), 3, 2020)
urlNAG1 = getProspectUrl(category.get("NA_G"), 1, 2020)
urlEUP1 = getProspectUrl(category.get("EU_P"), 1, 2020)
urlEUP2 = getProspectUrl(category.get("EU_P"), 2, 2020)
urlEUP3 = getProspectUrl(category.get("EU_P"), 3, 2020)
urlEUG1 = getProspectUrl(category.get("EU_G"), 1, 2020)

prospects = (
    getProspectsFromUrl(urlNAP1) +
    getProspectsFromUrl(urlNAP2) +
    getProspectsFromUrl(urlNAP3) +
    getProspectsFromUrl(urlEUP1) +
    getProspectsFromUrl(urlEUP2) +
    getProspectsFromUrl(urlEUP3) +
    getProspectsFromUrl(urlNAG1) +
    getProspectsFromUrl(urlEUG1)
)

ProspectDao().initProspectTable()
insertProspectToDb(prospects)
# for prospect in prospects:
#     if (len(prospect) >= 7):
#         print(getProspectFromRow(prospect))
# ProspectDao().initProspectTable()
# for prospect in prospects:
    # ProspectDao().createProspect(getProspectFromRow(prospect))
