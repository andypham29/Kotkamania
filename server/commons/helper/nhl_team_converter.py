class NhlTeamConverter:
    options = {1: "NJD",
               2: "NYI",
               3: "NYR",
               4: "PHI",
               5: "PIT",
               6: "BOS",
               7: "BUF",
               8: "MTL",
               9: "OTT",
               10: "TOR",
               12: "CAR",
               13: "FLA",
               14: "TBL",
               15: "WSH",
               16: "CHI",
               17: "DET",
               18: "NSH",
               19: "STL",
               20: "CGY",
               21: "COL",
               22: "EDM",
               23: "VAN",
               24: "ANA",
               25: "DAL",
               26: "LAK",
               28: "SJS",
               29: "CBJ",
               30: "MIN",
               52: "WPG",
               53: "ARI",
               54: "VGK",
               55: "SEA",
               56: "UTA",
               }

    @staticmethod
    def get_abbreviation_by_teamId(teamId):
        try:
            return NhlTeamConverter.options[int(teamId)]
        except:
            print(f"Unknown teamId: {teamId}")
            return None

    @staticmethod
    def get_teamId_by_abr(abr):
        try:
            for key, val in NhlTeamConverter.options.items():
                if val == abr:
                    return key
        except:
            print(f"Unknown abbreviation: {None}")
            return None

    @staticmethod
    def get_all_teamIds():
        return NhlTeamConverter.options.keys()

    @staticmethod
    def get_all_team_abr():
        return NhlTeamConverter.options.values()
