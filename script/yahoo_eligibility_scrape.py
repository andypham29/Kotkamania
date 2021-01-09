import urllib.request

import bs4 as bs

from server.internaldata.service.fantasy_nhl_player_service import FantasyNhlPlayerService


class YahooEligibilityScrape:

    def get_url(self, page):
        count = 50 * page
        return f'https://hockey.fantasysports.yahoo.com/hockey/draftanalysis?tab=SD&pos=ALL&sort=DA_AP&count={count}'

    def get_data_from_yahoo(self, url):
        source = urllib.request.urlopen(url).read()
        soup = bs.BeautifulSoup(source, 'lxml')

        data = []
        table = soup.find('table', attrs={'class': 'Table Ta-start Fz-xxs Table-interactive ysf-scrollloader-table'})
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [item.text.strip() for item in cols]
            if not cols:
                continue

            first_col = cols[0].split(' - ')

            name_col = first_col[0].split('\n')[1].split(' ')
            name = f"{name_col[0]} {name_col[1]}"

            position = first_col[1].replace(' ', '').split('\n')[0]
            position = position.replace('LW', 'L')
            position = position.replace('RW', 'R')

            cols = cols[1:]
            cols.insert(0, position)
            cols.insert(0, name)

            data.append([item for item in cols if item])
        return data

    def update_fantasy_db_with_yahoo_info(self, data):
        fantasy = FantasyNhlPlayerService(uri='../server/internaldata/db/fantasy.db')
        for d in data:
            print(d)
            fantasy.updateFantasyYahooInfoForFantasySkater(d)

    def main(self):
        data = []
        for i in range(6):
            url = self.get_url(i)
            data += self.get_data_from_yahoo(url)
        # url = self.get_url(1)
        # data += self.get_data_from_yahoo(url)
        for d in data:
            print(d)
        self.update_fantasy_db_with_yahoo_info(data)
        return None


if __name__ == '__main__':
    YahooEligibilityScrape().main()
