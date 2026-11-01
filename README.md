<<<<<<< HEAD
# nfl-player-compare
A tool for comparing NFL player statistics and performance.
# NFL Player Comparison & Custom Ranking Engine

A statistical NFL player comparison and ranking tool built with Python, Pandas, and `nflreadpy`. This engine evaluates players across multiple positions (QB, RB, WR, TE) using standardized Z-scores, custom user weighting, fuzzy search matching, and Matplotlib visual analytics.

---

## Features
- **Multi-Position Rankings:** Evaluates QBs, RBs, WRs, and TEs using position-specific performance metrics.
- **Z-Score Normalization:** Translates distinct stats (e.g., Passing Yards vs. EPA/play) onto a unified scale so volume does not dwarf rate efficiency.
- **Custom Weighting & Presets:** Interactively adjust weights (1–5) or choose preset configurations (Volume vs. Efficiency).
- **Fuzzy Player Search:** Clean string handling and `difflib` matching to handle typos and punctuation (e.g., `tj watt` $\rightarrow$ `T.J. Watt`).
- **Visual Analytics:** Generates side-by-side grouped bar chart comparisons using `matplotlib`.

---

## Installation & Setup

### Prerequisites
- Python 3.10+
- macOS / Linux / Windows terminal access

### Installation
1. Clone your repository (if not already local):
   ```bash
   git clone [https://github.com/YOUR-USERNAME/nfl-player-compare.git](https://github.com/YOUR-USERNAME/nfl-player-compare.git)
   cd nfl-player-compare
=======
# NFL-player-compare
A web application for comparing NFL players using statistics and performance data.
## Visual Player Comparison

Below is a sample output comparing **Patrick Mahomes** and **Brock Purdy** using normalized Z-scores across core QB factors:

![Player Comparison Chart](player_comparison.png)


[nfl_player_comparison_ranking_tool.md](https://github.com/user-attachments/files/34249619/nfl_player_comparison_ranking_tool.md)
# NFL Player Comparison & Ranking Tool

An interactive, multi-position NFL player evaluation tool built with Python, `pandas`, `nflreadpy`, and `matplotlib`. This application enables user-defined metric weighting, standardized Z-score performance indexing, dynamic position filtering, fuzzy player searching, and side-by-side visual analytics.

---

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Statistical Formula & Methodology](#statistical-formula--methodology)
- [Installation & Requirements](#installation--requirements)
- [Usage Guide](#usage-guide)
- [Visualizations](#visualizations)
- [Development Iterations & Changelog](#development-iterations--changelog)

---

## Overview

Traditional NFL statistics often evaluate players using single raw volume metrics (e.g., total passing yards) or raw averages that fail to account for context, sample size, or turnover penalties. This tool normalizes metrics across positions using **Z-scores** derived from 2023 regular-season data loaded via `nflreadpy`. It allows users to rank Quarterbacks (QB), Running Backs (RB), Wide Receivers (WR), and Tight Ends (TE) using balanced default formulas or custom-weighted criteria.

---

## Key Features

* **Multi-Position Normalization:** Evaluates QBs, RBs, WRs, and TEs using position-tailored factor dictionaries and minimum play thresholds.
* **Fuzzy & Robust Name Search:** Handles input typos (e.g., `"jaylen hurts"` $\rightarrow$ `"Jalen Hurts"`) and punctuation variations (e.g., `"tj watt"` $\rightarrow$ `"T.J. Watt"`) using string cleaning and `difflib`.
* **Interactive Preset & Custom Weighting:** Switch between Volume-heavy, Efficiency-heavy, Balanced, or fully customized metric weights (1–5 scale) with built-in overlap warnings.
* **Turnover Penalty Directionality:** Automatically flips negative indicators (Interceptions, Fumbles Lost) so higher raw totals reduce composite rankings.
* **Comparative Matplotlib Visualizations:** Generates grouped bar charts comparing player Z-scores directly against peers or position baselines.

---

## Statistical Formula & Methodology

### 1. Z-Score Standardization
To compare disparate metrics (such as Passing EPA/play vs. Total Passing Yards) on an identical scale, raw stats ($X$) are transformed into standard deviation units ($Z$):

$$Z = \left(\frac{X - \mu}{\sigma}\right) \times D$$

Where:
* $X$ = Player's raw stat
* $\mu$ = Qualified position mean
* $\sigma$ = Qualified position standard deviation
* $D$ = Direction multiplier ($+1.0$ for positive metrics, $-1.0$ for negative metrics like INTs or Fumbles)

### 2. Weighted Composite Index
Player rankings are generated using the weighted mean of individual metric Z-scores:

$$\text{Composite Score} = \frac{\sum (Z_i \times w_i)}{\sum w_i}$$

Where $Z_i$ is the standardized metric score and $w_i$ is the assigned weight ($1 \le w_i \le 5$).

### 3. Position Cutoffs & Factor Mappings

| Position | Minimum Threshold | Included Metrics | Metric Direction |
| :--- | :--- | :--- | :--- |
| **QB** | $\ge 200$ Attempts | Passing Yards, Passing TDs, Passing EPA, Interceptions | INTs: Negative ($-1.0$) |
| **RB** | $\ge 75$ Carries | Rushing Yards, Rushing TDs, Rushing EPA, Yards/Carry, Fumbles Lost | Fumbles: Negative ($-1.0$) |
| **WR** | $\ge 40$ Targets | Receiving Yards, Receptions, Receiving TDs, Receiving EPA, Yards/Rec | All Positive ($+1.0$) |
| **TE** | $\ge 40$ Targets | Receiving Yards, Receptions, Receiving TDs, Receiving EPA, Yards/Rec | All Positive ($+1.0$) |

---

## Installation & Requirements

### Prerequisites
* Python 3.9 or higher

### Required Dependencies
Install the necessary libraries via `pip`:

```bash
pip install pandas numpy nflreadpy matplotlib
```

---

## Usage Guide

### 1. Interactive Search
Run the robust player search interface:

```bash
python3 search.py
```

### 2. Custom QB Weighting Engine
Run the custom weighting menu:

```bash
python3 rankings_v4.py
```

### 3. Multi-Position Rankings
Generate rankings across QB, RB, WR, and TE:

```bash
python3 multi_position_rankings.py
```

### 4. Comparison Chart Generator
Create Z-score comparison charts:

```bash
python3 charts.py
```

---

## Visualizations

### Visual Player Comparison Chart
The tool generates standardized Z-score visual charts comparing player stats without scale distortion:

![Player Comparison Chart](player_comparison.png)

*Figure 1: Standardized Z-Score Comparison between Patrick Mahomes and Brock Purdy (2023 Season).*

---

## Development Iterations & Changelog

### Phase 1–2: Data Pipeline & Search Mechanics
* Integrated `nflreadpy` to ingest 2023 regular season stats.
* Implemented fuzzy matching via `difflib`. 
* **Bug Fix:** Fixed `TypeError: object of type 'float' has no len()` caused by `NaN` values in `nflreadpy` string columns by applying `.dropna()` and explicit type filtering.
* **Regex Enhancement:** Built `clean_str()` regex pipeline to resolve punctuation matching issues (e.g., matching `"tj watt"` to `"T.J. Watt"`).

### Phase 3: Z-Score Core & Model Validation
* Built initial 4-factor QB ranking model (Yards, TDs, EPA, INTs).
* Defended C.J. Stroud's QB3 placement based on low turnover rate (5 INTs on 499 attempts).

### Phase 4: Interactive Weighting Engine
* Added interactive CLI menu with Volume, Efficiency, and Balanced presets.
* Implemented input validation and double-counting warnings when high weights are assigned to both aggregate volume and composite EPA.

### Phase 5: Multi-Position Expansion
* Refactored Z-score scoring pipeline into a reusable modular function (`calculate_zscore_rankings`).
* Configured tailored factor dicts and touch thresholds for RB ($\ge 75$ carries), WR ($\ge 40$ targets), and TE ($\ge 40$ targets).
* Validated RB efficiency outliers (De'Von Achane's 7.8 YPC) vs. full-season volume leaders (Christian McCaffrey, Raheem Mostert).

### Phase 6: Matplotlib Analytics Visualization
* Developed `charts.py` to plot grouped Z-score bar graphs for visual comparison.
>>>>>>> 6e7809151161059ad00b6425cce15c644f1d0041
