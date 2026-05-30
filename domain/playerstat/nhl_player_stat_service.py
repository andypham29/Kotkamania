from typing import Optional, List

from domain.playerstat.model.nhl_player_stat import PlayerStat
from infra.spi.nhlapi.nhlskater.nhl_skater_realtime_service import NHLSkaterRealtimeService
from infra.spi.nhlapi.nhlskater.nhl_skater_summary_service import NHLSkaterSummaryService
from infra.spi.nhlapi.nhlskater.nhl_skater_timeonice_service import NHLSkaterTimeOnIceService


class NhlPlayerStatService:
    """
    Facade for building comprehensive NHL player statistics by combining data
    from multiple NHL API services: Realtime, Summary, and TimeOnIce.
    """

    def __init__(self,
                 realtime_service: Optional[NHLSkaterRealtimeService] = None,
                 summary_service: Optional[NHLSkaterSummaryService] = None,
                 timeonice_service: Optional[NHLSkaterTimeOnIceService] = None):
        self.realtime_service = realtime_service or NHLSkaterRealtimeService()
        self.summary_service = summary_service or NHLSkaterSummaryService()
        self.timeonice_service = timeonice_service or NHLSkaterTimeOnIceService()

    def _fetch_paged(self, method, season_id: int, total: int = 500, batch: int = 100):
        """
        Helper to fetch up to `total` items from a service method that supports
        `start` and `limit` (passed as strings).

        `method` should be a bound method like `self.realtime_service.getAllPlayers`.
        """
        results = []
        start = 0
        while len(results) < total:
            try:
                page = method(str(start), str(batch), season_id)
            except Exception:
                # stop on any error (network/rate limit). Caller can retry.
                break

            if not page:
                break

            results.extend(page)

            # If fewer than batch were returned we are at the end
            if len(page) < batch:
                break

            start += batch

        # trim to requested total
        return results[:total]

    def get_player_stat(self, player_id: int, season_id: int) -> Optional[PlayerStat]:
        """
        Get comprehensive player statistics for a specific player and season.

        Args:
            player_id: NHL player ID
            season_id: NHL season ID

        Returns:
            PlayerStat object with combined data from all three APIs, or None if player not found
        """
        # Get data from all three services
        realtime_data = self._get_realtime_data(player_id, season_id)
        summary_data = self._get_summary_data(player_id, season_id)
        timeonice_data = self._get_timeonice_data(player_id, season_id)

        # If no data found from any service, return None
        if not realtime_data and not summary_data and not timeonice_data:
            return None

        # Build comprehensive stat object
        return self._build_player_stat(player_id, season_id, realtime_data, summary_data, timeonice_data)

    def get_all_players_from_franchise(self, franchise_id: int, season_id: int) -> List[PlayerStat]:
        """
        Get comprehensive statistics for all players on a given team for a season.
        A franchise roster fits in a single API page, so no paging is required.
        """
        realtime_players  = self.realtime_service.getPlayersPerTeam(franchise_id,  seasonId=season_id)
        summary_players   = self.summary_service.getPlayersPerTeam(franchise_id,   seasonId=season_id)
        timeonice_players = self.timeonice_service.getPlayersPerTeam(franchise_id, seasonId=season_id)

        return self._combine_player_data(realtime_players, summary_players, timeonice_players, season_id)

    def _get_realtime_data(self, player_id: int, season_id: int):
        """Get realtime data for a specific player using paging"""
        try:
            players = self._fetch_paged(self.realtime_service.getAllPlayers, season_id, total=500, batch=100)
            return next((p for p in players if p.playerId == player_id), None)
        except:
            return None

    def _get_summary_data(self, player_id: int, season_id: int):
        """Get summary data for a specific player using paging"""
        try:
            players = self._fetch_paged(self.summary_service.getAllPlayers, season_id, total=500, batch=100)
            return next((p for p in players if p.playerId == player_id), None)
        except:
            return None

    def _get_timeonice_data(self, player_id: int, season_id: int):
        """Get time on ice data for a specific player using paging"""
        try:
            players = self._fetch_paged(self.timeonice_service.getAllPlayers, season_id, total=500, batch=100)
            return next((p for p in players if p.playerId == player_id), None)
        except:
            return None

    def _combine_player_data(self, realtime_players, summary_players, timeonice_players, season_id):
        """Combine data from three services into player stats"""
        # Create maps
        realtime_map = {p.playerId: p for p in realtime_players if getattr(p, 'playerId', None)}
        summary_map = {p.playerId: p for p in summary_players if getattr(p, 'playerId', None)}
        timeonice_map = {p.playerId: p for p in timeonice_players if getattr(p, 'playerId', None)}

        # Get all unique player IDs
        all_player_ids = set(realtime_map.keys()) | set(summary_map.keys()) | set(timeonice_map.keys())

        # Build stats for each player
        stats = []
        for player_id in sorted(all_player_ids):
            realtime_data = realtime_map.get(player_id)
            summary_data = summary_map.get(player_id)
            timeonice_data = timeonice_map.get(player_id)

            stat = self._build_player_stat(player_id, season_id, realtime_data, summary_data, timeonice_data)
            if stat:
                stats.append(stat)

        return stats

    def _build_player_stat(self, player_id: int, season_id: int,
                          realtime_data, summary_data, timeonice_data) -> Optional[PlayerStat]:
        """
        Build a PlayerStat object from the three data sources.
        """
        # If all data sources are None, return None
        if not realtime_data and not summary_data and not timeonice_data:
            return None

        # Initialize with default values
        stat = PlayerStat()

        # Set identifiers
        stat.playerId = player_id
        stat.seasonId = season_id

        # Add summary stats (primary source for most stats)
        if summary_data:
            stat.goals = summary_data.goals
            stat.assists = summary_data.assists
            stat.points = summary_data.points
            stat.shots = summary_data.shots
            stat.games = summary_data.gamesPlayed
            stat.plusMinus = summary_data.plusMinus
            stat.penaltyMinutes = summary_data.penaltyMinutes
            stat.powerPlayGoals = summary_data.ppGoals
            stat.powerPlayPoints = summary_data.ppPoints
            stat.shotPct = summary_data.shootingPct or 0.0
            stat.gameWinningGoals = summary_data.gameWinningGoals
            stat.overTimeGoals = summary_data.otGoals
            stat.shortHandedGoals = summary_data.shGoals
            stat.shortHandedPoints = summary_data.shPoints
            stat.faceOffPct = summary_data.faceoffWinPct

        # Add time on ice stats
        if timeonice_data:
            # Convert time values to strings as expected by the model
            stat.timeOnIce = str(timeonice_data.timeOnIce) if timeonice_data.timeOnIce else None
            stat.timeOnIcePerGame = str(timeonice_data.timeOnIcePerGame) if timeonice_data.timeOnIcePerGame else None
            stat.shifts = timeonice_data.shifts
            stat.evenTimeOnIce = str(timeonice_data.evTimeOnIce) if timeonice_data.evTimeOnIce else None
            stat.evenTimeOnIcePerGame = str(timeonice_data.evTimeOnIcePerGame) if timeonice_data.evTimeOnIcePerGame else None
            stat.powerPlayTimeOnIce = str(timeonice_data.ppTimeOnIce) if timeonice_data.ppTimeOnIce else None
            stat.powerPlayTimeOnIcePerGame = str(timeonice_data.ppTimeOnIcePerGame) if timeonice_data.ppTimeOnIcePerGame else None
            stat.shortHandedTimeOnIce = str(timeonice_data.shTimeOnIce) if timeonice_data.shTimeOnIce else None
            stat.shortHandedTimeOnIcePerGame = str(timeonice_data.shTimeOnIcePerGame) if timeonice_data.shTimeOnIcePerGame else None

        # Add realtime/advanced stats
        if realtime_data:
            stat.hits = realtime_data.hits
            stat.blocked = realtime_data.blockedShots

        return stat


if __name__ == '__main__':
    from dataclasses import asdict
    import json

    facade = NhlPlayerStatService()
    season_id = 20252026
    franchise_id = 6  # Boston Bruins
    stats = facade.get_all_players_from_franchise(franchise_id, season_id)

    for s in stats:
        print(json.dumps(asdict(s), indent=2))

    print(f"\nTotal players: {len(stats)}")
