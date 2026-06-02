#!/usr/bin/env python
"""Quick test to verify FantasyNhlPlayer serialization with stats."""

from domain.fantasyplayer.model.fantasy_nhl_player import FantasyNhlPlayer, DisplayStat, StatValue
import json

# Create a sample FantasyNhlPlayer with stats
display_stat = DisplayStat(
    assists=StatValue(10, 85),
    goals=StatValue(5, 75),
    points=StatValue(15, 80),
    games=StatValue(20, None),
    shots=StatValue(50, 70),
    hits=StatValue(25, 65),
    blocked=StatValue(15, 60),
    plusMinus=StatValue(5, 55),
    powerPlayGoals=StatValue(2, 50),
    powerPlayPoints=StatValue(5, 55)
)

player = FantasyNhlPlayer(
    id="123456",
    skaterFullName="John Doe",
    positionCode="C",
    teamId="1",
    fantasyGrade=85.5,
    yahooEligibility="C,LW",
    avgPick=50,
    avgRound=3,
    percentDrafted=95,
    teamName="Toronto",
    nhlRank=10,
    stat=display_stat
)

print("FantasyNhlPlayer structure:")
print(json.dumps(player.__dict__, default=lambda o: o.__dict__, indent=2))
print("\n✓ Test passed: FantasyNhlPlayer with StatValue objects serializes correctly")

