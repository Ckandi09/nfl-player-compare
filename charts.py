import matplotlib.pyplot as plt
import numpy as np
from multi_position_rankings import POSITION_CONFIGS, calculate_zscore_rankings, load_nfl_data


def plot_player_comparison(
    player1_name, player2_name, position="QB", season=2023
):
    """Generates and saves a Z-score comparison chart between two players of the same position."""
    # 1. Load data and compute rankings/Z-scores
    df = load_nfl_data(season=season)
    ranked_df = calculate_zscore_rankings(df, position=position)

    # 2. Extract Z-score columns for the position
    factors_info = POSITION_CONFIGS[position]["factors"]
    factor_keys = list(factors_info.keys())
    factor_labels = [factors_info[k][1] for k in factor_keys]
    z_cols = [f"{k}_z" for k in factor_keys]

    # 3. Locate players in dataset
    p1_data = ranked_df[
        ranked_df["player_display_name"].str.lower() == player1_name.lower()
    ]
    p2_data = ranked_df[
        ranked_df["player_display_name"].str.lower() == player2_name.lower()
    ]

    if p1_data.empty:
        print(f"❌ Player '{player1_name}' not found among qualified {position}s.")
        return
    if p2_data.empty:
        print(f"❌ Player '{player2_name}' not found among qualified {position}s.")
        return

    p1_name_clean = p1_data.iloc[0]["player_display_name"]
    p2_name_clean = p2_data.iloc[0]["player_display_name"]

    p1_zscores = p1_data.iloc[0][z_cols].values.astype(float)
    p2_zscores = p2_data.iloc[0][z_cols].values.astype(float)

    # 4. Matplotlib Grouped Bar Setup
    x = np.arange(len(factor_labels))  # label locations
    width = 0.35  # bar width

    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot bars
    rects1 = ax.bar(
        x - width / 2,
        p1_zscores,
        width,
        label=p1_name_clean,
        color="#1f77b4",
    )
    rects2 = ax.bar(
        x + width / 2,
        p2_zscores,
        width,
        label=p2_name_clean,
        color="#ff7f0e",
    )

    # 5. Styling and Formatting
    ax.axhline(
        0, color="black", linewidth=0.8, linestyle="--"
    )  # League average line at Z=0
    ax.set_ylabel("Standardized Score (Z-Score)", fontsize=12)
    ax.set_title(
        f"2023 Statistical Comparison: {p1_name_clean} vs. {p2_name_clean} ({position})",
        fontsize=14,
        fontweight="bold",
        pad=15,
    )
    ax.set_xticks(x)
    ax.set_xticklabels(factor_labels, fontsize=11)
    ax.legend(fontsize=11)
    ax.grid(axis="y", linestyle=":", alpha=0.6)

    # Add numeric labels above/below bars
    ax.bar_label(rects1, fmt="%.2f", padding=3)
    ax.bar_label(rects2, fmt="%.2f", padding=3)

    fig.tight_layout()

    # 6. Save image for portfolio & display
    filename = "player_comparison.png"
    plt.savefig(filename, dpi=300)
    print(f"--> Saved chart to '{filename}' successfully!")
    plt.show()


if __name__ == "__main__":
    # Example: Compare Patrick Mahomes vs. Brock Purdy
    plot_player_comparison("Patrick Mahomes", "Brock Purdy", position="QB")