from domain.fantasyplayer.model.fantasy_nhl_player import FantasyNhlPlayer, DisplayStat, StatValue
from infra.spi.sqlite.fantasyplayer.fantasy_player_repository import FantasyPlayerRepository
from infra.spi.sqlite.playerstat.nhl_player_stat_repository import NhlPlayerStatRepository
from infra.spi.sqlite.playerstatpercentile.nhl_player_stat_repository import NhlPlayerStatPercentileRepository
from server.commons.helper.nhl_season_converter import NhlYearConverter


class FantasyPlayerService:

    def __init__(self):
        self.fantasy_player_repository = FantasyPlayerRepository()
        self.nhl_player_stat_repository = NhlPlayerStatRepository()
        self.nhl_player_stat_percentile_repository = NhlPlayerStatPercentileRepository()

    def getAllFantasySkaters(self):
        """Return list of FantasyNhlPlayer with stats and percentiles populated."""
        players = self.fantasy_player_repository.getAllFantasySkaters()
        season_id = NhlYearConverter.get_previous_season_by_year_removed(0)

        result = []
        for player in players:
            # Fetch raw stats for this player and season
            player_stat = self.nhl_player_stat_repository.find_by_player_id(
                player.id, season_id)

            # Fetch percentile stats for this player and season
            player_percentile = self.nhl_player_stat_percentile_repository.find_by_player_id(
                player.id, season_id)

            # Build domain model FantasyNhlPlayer with DisplayStat
            fantasy_player = self._build_fantasy_nhl_player(player, player_stat, player_percentile)
            result.append(fantasy_player)

        return result

    def getAllFantasySkatersBySearchName(self, name):
        """Return list of FantasyNhlPlayer matching name with stats and percentiles populated."""
        players = self.fantasy_player_repository.getAllFantasySkatersBySearchName(name)
        season_id = NhlYearConverter.get_previous_season_by_year_removed(0)

        result = []
        for player in players:
            # Fetch raw stats for this player and season
            player_stat = self.nhl_player_stat_repository.find_by_player_id(
                player.id, season_id)

            # Fetch percentile stats for this player and season
            player_percentile = self.nhl_player_stat_percentile_repository.find_by_player_id(
                player.id, season_id)

            # Build domain model FantasyNhlPlayer with DisplayStat
            fantasy_player = self._build_fantasy_nhl_player(player, player_stat, player_percentile)
            result.append(fantasy_player)

        return result

    def getAllFantasySkatersWithTeamId(self, team_id):
        """Return list of FantasyNhlPlayer for given team with stats and percentiles populated."""
        players = self.fantasy_player_repository.getAllFantasySkatersByTeamId(team_id)
        season_id = NhlYearConverter.get_previous_season_by_year_removed(0)

        result = []
        for player in players:
            # Fetch raw stats for this player and season
            player_stat = self.nhl_player_stat_repository.find_by_player_id(
                player.id, season_id)

            # Fetch percentile stats for this player and season
            player_percentile = self.nhl_player_stat_percentile_repository.find_by_player_id(
                player.id, season_id)

            # Build domain model FantasyNhlPlayer with DisplayStat
            fantasy_player = self._build_fantasy_nhl_player(player, player_stat, player_percentile)
            result.append(fantasy_player)

        return result

    def getAllFantasySkatersWithCalculatedPercentiles(self):
        """Return list of FantasyNhlPlayer with percentiles calculated based on stat values."""
        players = self.fantasy_player_repository.getAllFantasySkaters()
        season_id = NhlYearConverter.get_previous_season_by_year_removed(0)

        # Build list of players with stats (no percentiles yet)
        players_with_stats = []
        for player in players:
            player_stat = self.nhl_player_stat_repository.find_by_player_id(
                player.id, season_id)

            fantasy_player = self._build_fantasy_nhl_player_without_percentile(player, player_stat)
            players_with_stats.append(fantasy_player)

        # Calculate percentiles based on stat values
        return self._populate_percentiles(players_with_stats)

    def _build_fantasy_nhl_player_without_percentile(self, sqlite_player, player_stat) -> FantasyNhlPlayer:
        """Build a FantasyNhlPlayer from repo data without percentile data."""
        # Extract stat values (raw counts from player_stat)
        stat_value = {
            'assists': player_stat.assists or 0 if player_stat else 0,
            'goals': player_stat.goals or 0 if player_stat else 0,
            'points': player_stat.points or 0 if player_stat else 0,
            'games': player_stat.games or 0 if player_stat else 0,
            'shots': player_stat.shots or 0 if player_stat else 0,
            'hits': player_stat.hits or 0 if player_stat else 0,
            'blocked': player_stat.blocked or 0 if player_stat else 0,
            'plusMinus': player_stat.plusMinus or 0 if player_stat else 0,
            'powerPlayGoals': player_stat.powerPlayGoals or 0 if player_stat else 0,
            'powerPlayPoints': player_stat.powerPlayPoints or 0 if player_stat else 0,
        }

        # Build DisplayStat with StatValue objects (percentile=None initially)
        display_stat = DisplayStat(
            assists=StatValue(stat_value['assists'], None),
            goals=StatValue(stat_value['goals'], None),
            points=StatValue(stat_value['points'], None),
            games=StatValue(stat_value['games'], None),
            shots=StatValue(stat_value['shots'], None),
            hits=StatValue(stat_value['hits'], None),
            blocked=StatValue(stat_value['blocked'], None),
            plusMinus=StatValue(stat_value['plusMinus'], None),
            powerPlayGoals=StatValue(stat_value['powerPlayGoals'], None),
            powerPlayPoints=StatValue(stat_value['powerPlayPoints'], None)
        )

        # Build and return FantasyNhlPlayer
        return FantasyNhlPlayer(
            id=sqlite_player.id,
            skaterFullName=sqlite_player.skaterFullName,
            positionCode=sqlite_player.positionCode,
            teamId=sqlite_player.teamId,
            fantasyGrade=sqlite_player.fantasyGrade,
            yahooEligibility=sqlite_player.yahooEligibility,
            avgPick=sqlite_player.avgPick,
            avgRound=sqlite_player.avgRound,
            percentDrafted=sqlite_player.percentDrafted,
            teamName=sqlite_player.teamName,
            nhlRank=sqlite_player.nhlRank,
            badge=sqlite_player.badge,
            stat=display_stat
        )

    def _populate_percentiles(self, players: list[FantasyNhlPlayer]) -> list[FantasyNhlPlayer]:
        """Calculate percentiles for each stat by comparing against all players."""
        # Extract stat values for each stat name
        stat_names = ['assists', 'goals', 'points', 'games', 'shots', 'hits', 'blocked', 'plusMinus', 'powerPlayGoals', 'powerPlayPoints']

        # Build lists of values for each stat (excluding None/0 values for percentile calculation)
        stat_values = {stat_name: [] for stat_name in stat_names}

        for player in players:
            for stat_name in stat_names:
                stat_obj = getattr(player.stat, stat_name)
                if stat_obj and stat_obj.value is not None and stat_obj.value > 0:
                    stat_values[stat_name].append(stat_obj.value)

        # Sort values for percentile calculation
        for stat_name in stat_names:
            stat_values[stat_name].sort()

        # Calculate percentiles for each player
        for player in players:
            for stat_name in stat_names:
                stat_obj = getattr(player.stat, stat_name)
                if stat_obj and stat_obj.value is not None:
                    # Calculate percentile rank
                    values = stat_values[stat_name]
                    if not values:
                        percentile = 0
                    else:
                        # Count how many values are less than or equal to current value
                        rank = sum(1 for v in values if v <= stat_obj.value)
                        percentile = round((rank / len(values)) * 100)

                    # Update the StatValue with percentile
                    stat_obj.percentile = percentile

        return players

    def _build_fantasy_nhl_player(self, sqlite_player, player_stat, player_percentile) -> FantasyNhlPlayer:
        """Build a FantasyNhlPlayer from repo data, enriching with stat values and percentiles."""
        try:
            player_id = int(sqlite_player.id)
        except (ValueError, AttributeError, TypeError):
            player_id = sqlite_player.id

        # Extract stat values (raw counts from player_stat)
        stat_value = {
            'assists': player_stat.assists or 0 if player_stat else 0,
            'goals': player_stat.goals or 0 if player_stat else 0,
            'points': player_stat.points or 0 if player_stat else 0,
            'games': player_stat.games or 0 if player_stat else 0,
            'shots': player_stat.shots or 0 if player_stat else 0,
            'hits': player_stat.hits or 0 if player_stat else 0,
            'blocked': player_stat.blocked or 0 if player_stat else 0,
            'plusMinus': player_stat.plusMinus or 0 if player_stat else 0,
            'powerPlayGoals': player_stat.powerPlayGoals or 0 if player_stat else 0,
            'powerPlayPoints': player_stat.powerPlayPoints or 0 if player_stat else 0,
        }

        # Extract percentile values
        stat_percentile = {
            'assists': player_percentile.assists if player_percentile else None,
            'goals': player_percentile.goals if player_percentile else None,
            'points': player_percentile.points if player_percentile else None,
            'games': player_percentile.games if player_percentile else None,
            'shots': player_percentile.shots if player_percentile else None,
            'hits': player_percentile.hits if player_percentile else None,
            'blocked': player_percentile.blocked if player_percentile else None,
            'plusMinus': player_percentile.plusMinus if player_percentile else None,
            'powerPlayGoals': player_percentile.powerPlayGoals if player_percentile else None,
            'powerPlayPoints': player_percentile.powerPlayPoints if player_percentile else None,
        }

        # Build DisplayStat with StatValue objects
        display_stat = DisplayStat(
            assists=StatValue(stat_value['assists'], stat_percentile['assists']),
            goals=StatValue(stat_value['goals'], stat_percentile['goals']),
            points=StatValue(stat_value['points'], stat_percentile['points']),
            games=StatValue(stat_value['games'], stat_percentile['games']),
            shots=StatValue(stat_value['shots'], stat_percentile['shots']),
            hits=StatValue(stat_value['hits'], stat_percentile['hits']),
            blocked=StatValue(stat_value['blocked'], stat_percentile['blocked']),
            plusMinus=StatValue(stat_value['plusMinus'], stat_percentile['plusMinus']),
            powerPlayGoals=StatValue(stat_value['powerPlayGoals'], stat_percentile['powerPlayGoals']),
            powerPlayPoints=StatValue(stat_value['powerPlayPoints'], stat_percentile['powerPlayPoints'])
        )

        # Build and return FantasyNhlPlayer
        return FantasyNhlPlayer(
            id=sqlite_player.id,
            skaterFullName=sqlite_player.skaterFullName,
            positionCode=sqlite_player.positionCode,
            teamId=sqlite_player.teamId,
            fantasyGrade=sqlite_player.fantasyGrade,
            yahooEligibility=sqlite_player.yahooEligibility,
            avgPick=sqlite_player.avgPick,
            avgRound=sqlite_player.avgRound,
            percentDrafted=sqlite_player.percentDrafted,
            teamName=sqlite_player.teamName,
            nhlRank=sqlite_player.nhlRank,
            badge=sqlite_player.badge,
            stat=display_stat
        )