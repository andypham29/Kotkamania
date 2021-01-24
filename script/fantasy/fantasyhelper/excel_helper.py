import xlsxwriter


class ExcelHelper:

    def __init__(self, filename='fantasy.xlsx'):
        self.workbook = xlsxwriter.Workbook(filename)

    def write_players_to_excel(self, sheet='forward', players=[]):
        worksheet = self.workbook.add_worksheet(sheet)
        worksheet.write(0, 0, "ID")  # Writes an int
        worksheet.write(0, 1, "RANK")  # Writes an int
        worksheet.write(0, 2, "NAME")  # Writes an int
        worksheet.write(0, 3, "GP")  # Writes an int
        worksheet.write(0, 4, "G")  # Writes an int
        worksheet.write(0, 5, "A")  # Writes an int
        worksheet.write(0, 6, "P")  # Writes an int
        worksheet.write(0, 7, "SCORE")  # Writes an int
        worksheet.write(0, 8, "INDEX")
        worksheet.write(0, 9, "PPTOI")

        format_yellow = self.workbook.add_format()
        format_yellow.set_pattern(1)
        format_yellow.set_bg_color('yellow')
        format_green = self.workbook.add_format()
        format_green.set_pattern(1)
        format_green.set_bg_color('green')
        format_red = self.workbook.add_format()
        format_red.set_pattern(1)
        format_red.set_bg_color('red')

        for a in range(len(players)):
            shotPct = players[a].shotPctIndex
            format_color = None
            if float(shotPct) < 0.85:
                format_color = format_red
            elif 0.85 <= float(shotPct) < 0.9:
                format_color = format_yellow
            elif 0.9 <= float(shotPct) < 0.98:
                format_color = None
            else:
                format_color = format_green

            worksheet.write_url(row=a + 1, col=0,
                                url=f"http://www.nhlmockdraft2020.herokuapp.com/api/nhl/players/{players[a].id}",
                                string=f"{players[a].id}")
            worksheet.write(a + 1, 1, a + 1)
            worksheet.write(a + 1, 2, players[a].name or 0)
            worksheet.write(a + 1, 3, players[a].games or 0)
            worksheet.write(a + 1, 4,
                            f"{players[a].goals or 0}")  # ({round(players[a].goals / players[a].games * 82, 2)})")
            worksheet.write(a + 1, 5,
                            f"{players[a].assists or 0}")  # ({round(players[a].assists / players[a].games * 82, 2)})")
            worksheet.write(a + 1, 6,
                            f"{players[a].points or 0}")  # ({round(players[a].points / players[a].games * 82, 2)})")
            worksheet.write(a + 1, 7, players[a].score or 1)
            worksheet.write(a + 1, 8, players[a].shotPctIndex or 0, format_color)
            worksheet.write(a + 1, 9, players[a].pptoi or 0)
            print(f"{a + 1}: {players[a].__dict__}")

    def close(self):
        self.workbook.close()
