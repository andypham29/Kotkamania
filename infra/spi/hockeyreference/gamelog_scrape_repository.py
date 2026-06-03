import requests
from bs4 import BeautifulSoup

class GameLogScrapeRepository:

    def __init__(self):
        pass

    def get_hockey_reference_gamelog(self, player_code, season):
        url = f"https://www.hockey-reference.com/players/{player_code[0]}/{player_code}/gamelog/{season}"
        r = requests.get(url)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find("table", id="gamelog")

        if not table:
            raise ValueError("Gamelog table not found — check player code or season")

        rows = table.find("tbody").find_all("tr")
        gamelog = []

        for row in rows:
            # Skip header rows inside tbody
            if row.get("class") == ["thead"]:
                continue

            # Skip rows without data
            if not row.find("td"):
                continue

            def get_td(stat):
                cell = row.find("td", {"data-stat": stat})
                if not cell:
                    return None
                text = cell.text.strip()
                return text if text != "" else None

            def get_th(stat):
                cell = row.find("th", {"data-stat": stat})
                if not cell:
                    return None
                text = cell.text.strip()
                return text if text != "" else None

            # Rk and Gcar are in <th>
            rk = get_th("ranker")  # Rk
            gcar = get_th("game_season")  # game number in season

            # Some seasons use "blk" instead of "blocked_shots"
            blocks = get_td("blocked_shots") or get_td("blk")

            row_data = [
                rk,  # Rk
                gcar,  # Gcar
                get_td("game_location"),  # Gtm (@ or blank)
                get_td("date_game"),  # Date
                get_td("team_id"),  # Team
                None,  # empty column
                get_td("opp_name_abbr") or get_td("opp_id"),  # Opp
                get_td("game_streak"),  # ▲ (often missing in 2026 -> None)
                get_td("game_result"),  # Result

                get_td("goals"),  # G
                get_td("assists"),  # A
                get_td("points"),  # PTS
                get_td("plus_minus"),  # +/-
                get_td("pen_min"),  # PIM

                get_td("goals_ev"),  # EVG
                get_td("goals_pp"),  # PPG
                get_td("goals_sh"),  # SHG
                get_td("goals_gw"),  # GWG

                None,  # EV  (not present on 2026 page)
                None,  # PP  (not present)
                None,  # SH  (not present)

                get_td("shots"),  # SOG
                get_td("shot_pct"),  # SPCT
                None,  # TSA (not present)

                get_td("shifts"),  # SHFT
                get_td("time_on_ice"),  # TOI

                None,  # FOW (not present)
                None,  # FOL (not present)

                blocks,  # BLK
                get_td("hits"),  # HIT
                get_td("takeaways"),  # TAKE
                get_td("giveaways"),  # GIVE
            ]

            gamelog.append(row_data)

        return gamelog


if __name__ == "__main__":
    player = "makarca01"  # Cale Makar
    season = 2026  # 2023–24 season

    data = GameLogScrapeRepository().get_hockey_reference_gamelog(player, season)

    for g in data[:5]:
        print(g)
