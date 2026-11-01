import numpy as np
import nflreadpy as nfl
import pandas as pd

# Position configuration dictionary defining stats, directions, and sample cutoffs
POSITION_CONFIGS = {
    "QB": {
        "cutoff_col": "attempts",
        "min_cutoff": 200,
        "factors": {
            "passing_yards": (1.0, "Passing Yards"),
            "passing_tds": (1.0, "Passing TDs"),
            "passing_epa": (1.0, "Passing EPA"),
            "passing_interceptions": (-1.0, "Interceptions"),
        },
    },
    "RB": {
        "cutoff_col": "carries",
        "min_cutoff": 75,
        "factors": {
            "rushing_yards": (1.0, "Rushing Yards"),
            "rushing_tds": (1.0, "Rushing TDs"),
            "rushing_epa": (1.0, "Rushing EPA"),
            "rushing_fumbles_lost": (-1.0, "Fumbles Lost"),
            "yards_per_carry": (1.0, "Yards / Carry"),
        },
    },
    "WR": {
        "cutoff_col": "targets",
        "min_cutoff": 40,
        "factors": {
            "receiving_yards": (1.0, "Receiving Yards"),
            "receptions": (1.0, "Receptions"),
            "receiving_tds": (1.0, "Receiving TDs"),
            "receiving_epa": (1.0, "Receiving EPA"),
            "yards_per_reception": (1.0, "Yards / Rec"),
        },
    },
    "TE": {
        "cutoff_col": "targets",
        "min_cutoff": 40,
        "factors": {
            "receiving_yards": (1.0, "Receiving Yards"),
            "receptions": (1.0, "Receptions"),
            "receiving_tds": (1.0, "Receiving TDs"),
            "receiving_epa": (1.0, "Receiving EPA"),
            "yards_per_reception": (1.0, "Yards / Rec"),
        },
    },
}


def load_nfl_data(season=2023):
    """Load regular season data and pre-calculate per-touch efficiency metrics."""
    df_polars = nfl.load_player_stats(seasons=season, summary_level="reg")
    df = df_polars.to_pandas()

    # Calculate derived rate metrics safely
    df["yards_per_carry"] = np.where(
        df["carries"] > 0, df["rushing_yards"] / df["carries"], 0.0
    )
    df["yards_per_reception"] = np.where(
        df["receptions"] > 0, df["receiving_yards"] / df["receptions"], 0.0
    )
    return df


def calculate_zscore_rankings(df, position, weights=None):
    """
    Reusable Phase 3 ranking core: Scores any position dynamically based on factor setup.
    """
    if position not in POSITION_CONFIGS:
        raise ValueError(f"Position '{position}' is not supported.")

    config = POSITION_CONFIGS[position]
    cutoff_col = config["cutoff_col"]
    min_cutoff = config["min_cutoff"]
    factors_info = config["factors"]

    # Filter data for position and attempt/touch threshold
    pos_df = df[
        (df["position"] == position) & (df[cutoff_col] >= min_cutoff)
    ].copy()

    if pos_df.empty:
        print(
            f"No players found for {position} matching cutoff ({cutoff_col} >= {min_cutoff})."
        )
        return pos_df

    # Default to equal weights if none are provided
    if weights is None:
        weights = {factor: 1.0 for factor in factors_info}

    weighted_z_sum = np.zeros(len(pos_df))
    total_weight = sum(weights.values())

    # Reused Phase 3 Z-score normalization loop
    for factor, weight in weights.items():
        direction, _ = factors_info[factor]
        mean = pos_df[factor].mean()
        std = pos_df[factor].std()

        # Prevent division by zero if std is 0
        if std == 0 or np.isnan(std):
            z_score = np.zeros(len(pos_df))
        else:
            z_score = ((pos_df[factor] - mean) / std) * direction

        pos_df[f"{factor}_z"] = z_score
        weighted_z_sum += z_score * weight

    # Calculate composite score & sort
    pos_df["composite_score"] = weighted_z_sum / total_weight
    pos_df = pos_df.sort_values(
        by="composite_score", ascending=False
    ).reset_index(drop=True)
    pos_df["rank"] = pos_df.index + 1

    return pos_df


def display_top_players(ranked_df, position, top_n=3):
    """Display top N players showing ONLY stats relevant to their specific position."""
    config = POSITION_CONFIGS[position]
    display_cols = ["rank", "player_display_name", "composite_score"] + list(
        config["factors"].keys()
    )

    print(f"\n" + "=" * 65)
    print(
        f"        TOP {top_n} {position} RANKINGS (2023 Regular Season)"
    )
    print("=" * 65)
    print(ranked_df[display_cols].head(top_n).to_string(index=False))


if __name__ == "__main__":
    print("Downloading/loading NFL statistics...")
    data = load_nfl_data(season=2023)

    # Calculate top 3 for QB, RB, WR, and TE using the same reusable scoring core
    for pos in ["QB", "RB", "WR", "TE"]:
        ranked_players = calculate_zscore_rankings(data, position=pos)
        display_top_players(ranked_players, position=pos, top_n=3)