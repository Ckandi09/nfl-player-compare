# NFL Player Comparison & Ranking Tool

A modular terminal application that processes season-long NFL data to rank and compare offensive skill players (QBs, RBs, WRs, TEs) using a custom Z-score statistical methodology.

---

## Installation

Ensure you have Python 3.8+ installed, then install the required dependencies:

```bash
pip install pandas numpy nflreadpy matplotlib

```

---

## Features

* **Memory-Cached Data Loading:** Downloads and parses 2023 NFL data using `nflreadpy` once at startup to optimize performance across all operations.
* **Robust Player Search:** Supports exact full-name matches, unique last-name searches, and fuzzy string matching (with auto-correction for common typos).
* **Position-Specific Z-Score Engine:** Ranks players within their position using weighted statistical factors (e.g., passing yards, passing TDs, passing EPA, and interceptions for QBs).
* **Sample-Size Thresholds:** Filters out backup players using position-specific volume cutoffs (e.g., minimum 200 pass attempts for QBs).
* **Side-by-Side Visual Comparisons:** Generates matplotlib bar charts comparing two qualified players across their position's core metrics.
* **Interactive Terminal Workflow:** An intuitive CLI menu that unifies data processing, searching, ranking, and charting.

---

## Positional Cutoffs & Metric Factors

| Position | Minimum Cutoff | Evaluated Metric Factors & Directions |
| --- | --- | --- |
| **QB** | 200 pass attempts | Passing Yards (1.0), Passing TDs (1.0), Passing EPA (1.0), Interceptions (-1.0) |
| **RB** | 75 rush attempts | Rushing Yards (1.0), Rushing TDs (1.0), Rushing EPA (1.0), Yards/Carry (1.0), Fumbles Lost (-1.0) |
| **WR** | 40 targets | Receiving Yards (1.0), Receptions (1.0), Receiving TDs (1.0), Receiving EPA (1.0), Yards/Reception (1.0) |
| **TE** | 40 targets | Receiving Yards (1.0), Receptions (1.0), Receiving TDs (1.0), Receiving EPA (1.0), Yards/Reception (1.0) |

---

## Statistical Methodology

Players are evaluated using **Z-scores** to measure how many standard deviations their performance is above or below the positional mean:

$$Z = D \times \frac{x - \mu}{\sigma}$$

* **$x$**: Player's individual stat value
* **$\mu$**: Positional average (mean)
* **$\sigma$**: Positional standard deviation
* **$D$**: Direction multiplier ($D = -1$ for negative metrics like interceptions and fumbles lost; $D = 1$ for all other stats)

### Composite Score Formula

Positional Z-scores are multiplied by their directional factors and averaged to determine a composite score:

$$\text{Composite Score} = \frac{\sum (Z_{\text{stat}} \times D_{\text{stat}})}{\sum \vert{}D_{\text{stat}}\vert{}}$$

*Note: All EPA (Expected Points Added) metrics in this tool utilize cumulative **Total EPA** for the 2023 regular season, rather than per-play averages.*

---

## Usage Guide

To launch the interactive CLI application:

```bash
python3 main.py

```

### Individual Scripts & Standalone Tools

*(Earlier versions and specialized modules)*

* `multi_position_rankings.py`: Runs the core Z-score calculation engine and prints positional leaderboards across skill positions.
* `search.py`: Handles player name normalization, fuzzy matching, and disambiguation.
* `charts.py`: Generates individual matplotlib comparison charts.
* `rankings.py` & `rankings_v4.py`: Earlier iterations of the ranking script. `rankings_v4.py` includes a standalone interactive menu allowing users to input custom weights specifically for QBs (note: custom weighting is currently exclusive to `rankings_v4.py` and not part of the main `main.py` CLI workflow).

---

## Visualizations

### Example Comparison: Amon-Ra St. Brown vs. Justin Jefferson (2023 WRs)

> **Analytical Note:** Season-long cumulative totals heavily favor players who appeared in all 17 games. Justin Jefferson missed 7 games in 2023 due to a hamstring injury; while his efficiency (*Yards Per Reception*) remained elite, his cumulative Z-scores reflect missed volume compared to Amon-Ra St. Brown's full-season workload.
> ![Amon-Ra St. Brown vs. Justin Jefferson](player_comparison.png)

---

## Technical Changelog

* **Phase 1 (Data Foundation & Basic Ranking):**
* Loaded raw 2023 season-long player stats using `nflreadpy` (`load_player_stats` with `summary_level="reg"`).
* Calculated basic Z-scores for QBs and handled NaN values caused by missing stats.


* **Phase 2 (Position Expansion & Weighting):**
* Defined `POSITION_CONFIGS` for QBs, RBs, WRs, and TEs with position-specific metrics and minimum volume thresholds.
* Implemented directional multipliers ($D = -1$) for negative metrics (interceptions, fumbles).


* **Phase 3 (Fuzzy Search & Punctuation Handling):**
* Built `search.py` using `difflib` to auto-correct typos (e.g., auto-correcting `Amon Ra St brown` to `Amon-Ra St. Brown`).
* Added multi-player selection menus when input searches match multiple players.


* **Phase 4 (Validation & Verification):**
* Verified sample-size filtering against real-world edge cases (e.g., C.J. Stroud's rookie season qualifications and De'Von Achane's high-efficiency, limited-volume RB campaign).


* **Phase 5 (Visualizations):**
* Created `charts.py` using `matplotlib` to plot side-by-side Z-score profiles for two players sharing the same position.


* **Phase 6 (Refactoring & Decoupling):**
* Modularized codebase to prevent redundant dataset re-downloads across functions.


* **Phase 7 (Application Orchestration & Polish):**
* Built `main.py` entry point to connect memory-cached data loading, player search, ranking outputs, and side-by-side charting in a single CLI loop.
* **Bug Fix:** Fixed volume qualification logic in `get_player_qualification_info()`. The initial fix attempted to parse `min_` keys dynamically and defaulted to checking 0, but the function was successfully updated to read `cutoff_col` and `min_cutoff` directly from `POSITION_CONFIGS` (verified with backup QB Blaine Gabbert's 35 pass attempts).
* **Analytical Insight:** Documented the impact of missed games on cumulative season totals using the Amon-Ra St. Brown vs. Justin Jefferson comparison.
