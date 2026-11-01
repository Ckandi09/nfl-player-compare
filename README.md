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