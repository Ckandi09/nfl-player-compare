import difflib
import re
import nflreadpy as nfl
import pandas as pd


def clean_str(text):
    """Strip out punctuation like dots, dashes, and extra spaces for clean matching."""
    if not isinstance(text, str):
        return ""
    return re.sub(r"[^\w\s]", "", text).lower().strip()


def load_player_data():
    """Load player stats and clean player roster data."""
    df_polars = nfl.load_player_stats(seasons=2023, summary_level="reg")
    df = df_polars.to_pandas()

    # Drop missing names or positions
    df = df.dropna(subset=["player_display_name", "position"]).copy()

    # Keep only valid non-empty string rows
    df = df[
        df["player_display_name"].apply(
            lambda x: isinstance(x, str) and len(x.strip()) > 0
        )
    ]

    # Return unique player-position pairs
    players_df = df[["player_display_name", "position"]].drop_duplicates()
    return players_df


def search_player(raw_input_name, players_df):
    raw_clean = clean_str(raw_input_name)

    if not raw_clean:
        print("Please enter a valid player name.")
        return None, None

    players_df = players_df.copy()
    players_df["normalized_name"] = players_df["player_display_name"].apply(
        clean_str
    )

    # 1. Check for exact match (e.g., "tj watt" -> "T.J. Watt", "jalen hurts" -> "Jalen Hurts")
    exact_matches = players_df[players_df["normalized_name"] == raw_clean]

    # 2. Check for last-name match
    if exact_matches.empty:
        exact_matches = players_df[
            players_df["normalized_name"].str.contains(
                rf"\b{raw_clean}", regex=True
            )
        ]

    # If exactly 1 player found (exact full name or unique last name)
    if len(exact_matches) == 1:
        selected = exact_matches.iloc[0]
        return selected["player_display_name"], selected["position"]

    # If multiple players found (e.g. searching "Allen")
    if len(exact_matches) > 1:
        print(f"\nMultiple players found for '{raw_input_name}':")
        matches_list = exact_matches.reset_index(drop=True)
        for idx, row in matches_list.iterrows():
            print(
                f"  [{idx + 1}] {row['player_display_name']} ({row['position']})"
            )

        choice = input("\nEnter the number of the player you meant: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(matches_list):
            selected = matches_list.iloc[int(choice) - 1]
            return selected["player_display_name"], selected["position"]
        else:
            print("Invalid selection.")
            return None, None

    # 3. Fuzzy matching for typos ("Jaylen Hurts", "TJ Watta")
    all_names = [
        str(name)
        for name in players_df["player_display_name"].tolist()
        if isinstance(name, str) and name.strip()
    ]

    close_matches = difflib.get_close_matches(
        raw_input_name.strip(), all_names, n=3, cutoff=0.5
    )

    if close_matches:
        # If the top fuzzy match is extremely close (e.g. Jaylen Hurts -> Jalen Hurts), auto-select it!
        top_match_clean = clean_str(close_matches[0])
        first_name_input = raw_clean.split()[0] if " " in raw_clean else ""

        # Auto select if it's a obvious single candidate typo fix
        if len(close_matches) == 1 or (
            first_name_input and first_name_input in top_match_clean
        ):
            suggested_name = close_matches[0]
            selected = players_df[
                players_df["player_display_name"] == suggested_name
            ].iloc[0]
            print(
                f"--> Auto-corrected '{raw_input_name}' to '{selected['player_display_name']}'"
            )
            return selected["player_display_name"], selected["position"]

        # If there are genuinely multiple different candidates, prompt user
        print(f"\nNo exact match for '{raw_input_name}'. Did you mean:")
        for idx, name in enumerate(close_matches, 1):
            print(f"  [{idx}] {name}")

        choice = input(
            "\nEnter the number of the correct player (or press Enter to cancel): "
        ).strip()
        if choice.isdigit() and 1 <= int(choice) <= len(close_matches):
            suggested_name = close_matches[int(choice) - 1]
            selected = players_df[
                players_df["player_display_name"] == suggested_name
            ].iloc[0]
            return selected["player_display_name"], selected["position"]

    # 4. Fallback for invalid names (e.g., "xyz123")
    print(f"\nNo player found matching '{raw_input_name}'.")
    return None, None


if __name__ == "__main__":
    print("Loading NFL data...")
    df_players = load_player_data()
    print("Data loaded successfully!\n")

    while True:
        user_query = input(
            "Enter an NFL player's name (or type 'quit' to exit): "
        )

        if user_query.strip().lower() == "quit":
            print("Exiting search.")
            break

        name, pos = search_player(user_query, df_players)

        if name and pos:
            print(f"--> Result: Found {name} | Position: {pos}\n")
        print("-" * 50)