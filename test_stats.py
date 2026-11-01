import nflreadpy as nfl

# 1. Load regular season player stats for 2023
df_polars = nfl.load_player_stats(seasons=2023, summary_level="reg")
df = df_polars.to_pandas()

# 2. Filter for Quarterbacks (QB) with at least 50 passing attempts (removes backup noise)
qbs = df[(df["position"] == "QB") & (df["attempts"] >= 50)]

# 3. Select columns: Name, Passing Yards, TDs, Interceptions, and EPA
qb_table = qbs[
    [
        "player_display_name",
        "passing_yards",
        "passing_tds",
        "passing_interceptions",
        "passing_epa",
    ]
]

# 4. Sort by Passing Yards descending
qb_table = qb_table.sort_values(by="passing_yards", ascending=False)

# 5. Print the top 15 quarterbacks
print(qb_table.head(15).to_string(index=False))