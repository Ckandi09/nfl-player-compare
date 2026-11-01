import numpy as np
import pandas as pd
import nflreadpy as nfl


def load_and_score_qbs(season=2023, min_attempts=200):
    print("Downloading/loading player stats from nflreadpy... (this may take a few seconds)")
    df_polars = nfl.load_player_stats(seasons=season, summary_level="reg")
    df = df_polars.to_pandas()

    print(f"Total raw rows loaded: {len(df)}")

    # Filter for Quarterbacks with minimum attempt threshold
    qbs = df[(df["position"] == "QB") & (df["attempts"] >= min_attempts)].copy()
    print(f"Number of QBs with >= {min_attempts} pass attempts: {len(qbs)}")

    if qbs.empty:
        print("Warning: No quarterbacks matched your filter criteria!")
        return qbs

    # 1. Define stats and their direction (+1 for good, -1 for bad stats)
    factors = {
        "passing_yards": 1.0,
        "passing_tds": 1.0,
        "passing_epa": 1.0,
        "passing_interceptions": -1.0,  # Flipped: more INTs lowers score
    }

    # 2. Calculate Z-Scores for each factor: Z = (X - mean) / std
    for factor, direction in factors.items():
        mean = qbs[factor].mean()
        std = qbs[factor].std()
        # Multiply by direction to flip negative metrics
        qbs[f"{factor}_z"] = ((qbs[factor] - mean) / std) * direction

    # 3. Calculate Composite Weighted Score (Equal weights: 25% each)
    qbs["composite_score"] = (
        qbs["passing_yards_z"]
        + qbs["passing_tds_z"]
        + qbs["passing_epa_z"]
        + qbs["passing_interceptions_z"]
    ) / len(factors)

    # 4. Rank players by composite score descending
    qbs = qbs.sort_values(by="composite_score", ascending=False).reset_index(
        drop=True
    )
    qbs["rank"] = qbs.index + 1

    return qbs


if __name__ == "__main__":
    df_ranked = load_and_score_qbs(season=2023, min_attempts=200)

    if not df_ranked.empty:
        print("\n--- TOP 3 QUARTERBACKS (2023 Season) ---")
        top_3 = df_ranked[
            [
                "rank",
                "player_display_name",
                "composite_score",
                "passing_yards",
                "passing_tds",
                "passing_interceptions",
                "passing_epa",
            ]
        ].head(3)
        print(top_3.to_string(index=False))