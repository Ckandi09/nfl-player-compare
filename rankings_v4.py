import numpy as np
import nflreadpy as nfl
import pandas as pd


def load_qb_data(season=2023, min_attempts=200):
    """Load player stats and compute per-attempt metrics."""
    df_polars = nfl.load_player_stats(seasons=season, summary_level="reg")
    df = df_polars.to_pandas()

    # Filter for regular QBs with at least min_attempts
    qbs = df[(df["position"] == "QB") & (df["attempts"] >= min_attempts)].copy()

    # Derived metric: Yards per attempt
    qbs["yards_per_attempt"] = qbs["passing_yards"] / qbs["attempts"]
    return qbs


def get_weight_input(prompt):
    """Prompts the user for a weight between 1 and 5 with validation."""
    while True:
        val = input(prompt).strip()
        if val.isdigit() and 1 <= int(val) <= 5:
            return float(val)
        print("  ❌ Invalid input! Please enter an integer between 1 and 5.")


def get_user_weights():
    """Interactive prompt menu with presets and custom weight input."""
    print("\n--- CHOOSE A WEIGHTING PRESET OR CUSTOMIZE ---")
    print("  [1] Volume Preset     (Emphasis on Yards & TDs)")
    print("  [2] Efficiency Preset (Emphasis on EPA & Yards/Attempt)")
    print("  [3] Balanced Preset   (Equal weights across all stats)")
    print("  [4] Custom Weights    (Manually assign weights 1–5)")

    choice = input("\nEnter choice (1-4): ").strip()

    if choice == "1":
        print("\n--> Applied Preset: Volume heavy")
        return {
            "passing_yards": 5.0,
            "passing_tds": 5.0,
            "passing_epa": 1.0,
            "yards_per_attempt": 1.0,
            "passing_interceptions": 2.0,
        }
    elif choice == "2":
        print("\n--> Applied Preset: Efficiency heavy")
        return {
            "passing_yards": 1.0,
            "passing_tds": 2.0,
            "passing_epa": 5.0,
            "yards_per_attempt": 5.0,
            "passing_interceptions": 4.0,
        }
    elif choice == "3":
        print("\n--> Applied Preset: Balanced")
        return {
            "passing_yards": 3.0,
            "passing_tds": 3.0,
            "passing_epa": 3.0,
            "yards_per_attempt": 3.0,
            "passing_interceptions": 3.0,
        }
    else:
        print("\n-- Custom Weighting (Enter 1=Lowest Impact to 5=Highest) --")
        w_yards = get_weight_input("Weight for Passing Yards (1-5): ")
        w_tds = get_weight_input("Weight for Passing Touchdowns (1-5): ")
        w_epa = get_weight_input("Weight for Passing EPA (1-5): ")
        w_ypa = get_weight_input("Weight for Yards Per Attempt (1-5): ")
        w_ints = get_weight_input(
            "Weight for Interception Penalty (1-5): "
        )

        # Overlap Warning Check
        if w_epa >= 4 and (w_yards >= 4 or w_tds >= 4):
            print(
                "\n⚠️  NOTE: High weights on both EPA and Volume metrics (Yards/TDs) "
                "will reward high-usage efficiency twice!"
            )

        return {
            "passing_yards": w_yards,
            "passing_tds": w_tds,
            "passing_epa": w_epa,
            "yards_per_attempt": w_ypa,
            "passing_interceptions": w_ints,
        }


def score_and_rank_qbs(qbs, weights):
    """Normalize metrics via Z-Scores and calculate custom weighted score."""
    qbs = qbs.copy()

    # Direction: +1 for positive stats, -1 for negative stats (Interceptions)
    directions = {
        "passing_yards": 1.0,
        "passing_tds": 1.0,
        "passing_epa": 1.0,
        "yards_per_attempt": 1.0,
        "passing_interceptions": -1.0,
    }

    weighted_z_sum = np.zeros(len(qbs))
    total_weight = sum(weights.values())

    for metric, weight in weights.items():
        mean = qbs[metric].mean()
        std = qbs[metric].std()
        # Z-score formula: (X - mean) / std
        z_score = ((qbs[metric] - mean) / std) * directions[metric]
        qbs[f"{metric}_z"] = z_score
        weighted_z_sum += z_score * weight

    qbs["composite_score"] = weighted_z_sum / total_weight
    qbs = qbs.sort_values(by="composite_score", ascending=False).reset_index(
        drop=True
    )
    qbs["rank"] = qbs.index + 1
    return qbs


if __name__ == "__main__":
    print("Loading 2023 QB statistics...")
    qb_data = load_qb_data(season=2023, min_attempts=200)

    weights = get_user_weights()
    ranked_qbs = score_and_rank_qbs(qb_data, weights)

    print("\n" + "=" * 65)
    print("               TOP 5 QUARTERBACKS (CUSTOM FORMULA)")
    print("=" * 65)
    print(
        ranked_qbs[
            [
                "rank",
                "player_display_name",
                "composite_score",
                "passing_yards",
                "passing_tds",
                "passing_epa",
                "yards_per_attempt",
            ]
        ]
        .head(5)
        .to_string(index=False)
    )