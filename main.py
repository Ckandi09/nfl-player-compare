"""NFL Player Comparison & Interactive Ranking Tool (main.py)

Integrates search, Z-score rankings, and Matplotlib visual comparisons into a
single interactive terminal application.
"""

from charts import plot_player_comparison
from multi_position_rankings import (
    POSITION_CONFIGS,
    calculate_zscore_rankings,
    display_top_players,
    load_nfl_data,
)
from search import search_player

# Define supported positions matching multi_position_rankings.py
SUPPORTED_POSITIONS = ["QB", "RB", "WR", "TE"]


def get_player_qualification_info(df, player_name, position):
    """Checks if a player exists in raw data and if they met position sample-size cutoffs."""
    raw_matches = df[
        df["player_display_name"].str.lower() == player_name.lower()
    ]

    if raw_matches.empty:
        return None, "Player not found in 2023 dataset."

    player_row = raw_matches.iloc[0]
    config = POSITION_CONFIGS[position]
    factors = config["factors"]

    # Identify the threshold key name dynamically
    cutoff_key = next((k for k in config if k.startswith("min_")), None)
    cutoff = config.get(cutoff_key, 0) if cutoff_key else 0

    threshold_stat = list(factors.keys())[0]  # e.g., 'attempts', 'carries', 'targets'
    actual_val = player_row.get(threshold_stat, 0)

    if actual_val < cutoff:
        return player_row, (
            f"⚠️  {player_row['player_display_name']} did not meet the sample-size cutoff "
            f"for ranking ({actual_val} {threshold_stat}, needed {cutoff}+)."
        )

    return player_row, "Qualified"


def run_interactive_tool():
    """Main execution loop for the NFL comparison tool."""
    print("\n" + "=" * 60)
    print("🏈 WELCOME TO THE NFL STATISTICAL RANKING & COMPARISON TOOL 🏈")
    print("=" * 60)

    # Load data ONCE at startup to avoid redundant downloads
    print("\n[1/7] Loading 2023 NFL season data into memory...")
    nfl_df = load_nfl_data(season=2023)
    print("✓ Data successfully loaded!\n")

    while True:
        print("-" * 60)
        user_input = input(
            "Enter a player's name (or type 'quit' to exit): "
        ).strip()

        if user_input.lower() in ["quit", "q", "exit"]:
            print("\nThanks for using the NFL Comparison Tool! Goodbye! 👋\n")
            break

        if not user_input:
            continue

        # Search player name and get position
        matched_name, position = search_player(user_input, nfl_df)

        if not matched_name or not position:
            continue

        print(f"\n🔍 Found: {matched_name} ({position})")

        # Edge Case: Unsupported Position
        if position not in SUPPORTED_POSITIONS:
            print(f"ℹ️  Position '{position}' is currently unsupported.")
            print(
                f"   Our Z-score engine only ranks skill positions: {', '.join(SUPPORTED_POSITIONS)}."
            )
            continue

        # Rank position using Z-scores
        ranked_df = calculate_zscore_rankings(nfl_df, position=position)

        # Check sample-size qualification
        player_row, qual_status = get_player_qualification_info(
            nfl_df, matched_name, position
        )

        display_top_players(ranked_df, position=position, top_n=3)

        # Display target player's specific rank
        p_match = ranked_df[
            ranked_df["player_display_name"].str.lower() == matched_name.lower()
        ]

        if not p_match.empty:
            # Determine Rank
            if "Rank" in p_match.columns:
                rank = p_match.iloc[0]["Rank"]
            elif "rank" in p_match.columns:
                rank = p_match.iloc[0]["rank"]
            else:
                rank = ranked_df.index.get_loc(p_match.index[0]) + 1

            # Determine Composite Z-Score Column
            z_col = next(
                (
                    c
                    for c in p_match.columns
                    if "zscore" in c.lower()
                    or "z_score" in c.lower()
                    or "composite" in c.lower()
                ),
                None,
            )
            composite_z = p_match.iloc[0][z_col] if z_col else 0.0

            total_qualified = len(ranked_df)
            print(
                f"\n🎯 {matched_name}: #{rank} out of {total_qualified} qualified {position}s (Composite Z-Score: {composite_z:+.2f})"
            )
        else:
            print(f"\n{qual_status}")

        # Offer side-by-side comparison chart
        chart_choice = (
            input(
                f"\nCompare {matched_name} with another {position} on a Z-Score chart? (y/n): "
            )
            .strip()
            .lower()
        )

        if chart_choice in ["y", "yes"]:
            while True:
                p2_input = input(
                    f"Enter second {position}'s name: "
                ).strip()
                if not p2_input:
                    break

                p2_name, p2_pos = search_player(p2_input, nfl_df)
                if not p2_name or not p2_pos:
                    continue

                # Edge Case: Position mismatch
                if p2_pos != position:
                    print(
                        f"⚠️ Position mismatch! {matched_name} is a {position}, but {p2_name} is a {p2_pos}."
                    )
                    print(
                        "   Charts require both players to share the same position scale."
                    )
                    continue

                print(f"\n📊 Generating chart for {matched_name} vs. {p2_name}...")
                print(
                    "💡 (Note: If the chart window opens, close it to return to the menu.)"
                )

                plot_player_comparison(
                    matched_name, p2_name, position=position, season=2023
                )
                break


if __name__ == "__main__":
    run_interactive_tool()