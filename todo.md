Todo of graphs we should include:
1. Datagrid of all champs
2. Bar chart of winrate by divided into clases
3. Horizontal bar chart of top 10 champions by winrate
4. time series of winrate of a champ through the patches
5. heatmap of Correlation matrix (Score, Win %, Pick %, Ban %, KDA, Trend) Visualize relationships between numerical metrics (Chat idea)
6. scatterplot of pick% vs win% and color them by champion tier
7. winrate of roles over patches shows in a time series graph

1) Top-10 Champions by Pick % (Bar chart)

Type: Horizontal bar chart

Purpose: snapshot of popularity for selected month

Implementation: interactive Plotly/Altair, sort descending, show Pick%, Ban%, Win% on hover

Answers: Who’s most picked this month?

2) Top-10 Champions by Win % (Bar chart)

Type: Horizontal bar chart

Purpose: shows strongest champions by win-rate (may differ from picks)

Answers: Who’s performing best?

3) Distribution of Score (Histogram + KDE)

Type: Histogram (or density plot)

Purpose: distribution of Score across champions in a month

Implementation: facet by Role or Tier optionally

Answers: How variable is the rating?

4) Scatter / Bubble — Win % vs Pick % (bubble sized by Ban %; color by Class)

Type: Scatter/Bubble chart

Purpose: detect over-picked or under-performing champions

Answers: Are popular champions also effective?

5) Boxplot (or Violin) of KDA per Tier

Type: Boxplot/Violin

Purpose: compare performance dispersion across tiers

Answers: Are top tiers consistent?

6) Correlation Heatmap (numerical variables)

Type: Heatmap (correlation matrix)

Purpose: show relationships (Score vs Win%, KDA vs Win%, Pick% vs Ban%)

Answers: Which metrics move together?

7) Time Series — Line chart of Pick % for selected champions (multi-line)

Type: Multi-line time series

Purpose: track a small set (3–10) of champions over 12 months

Implementation: interactive legend to toggle champions

Answers: How have individual champions trended?

8) Stacked Area Chart — Role share of total pick % over time

Type: Stacked area chart

Purpose: show role meta shifts (e.g., support picks rising) across months

Answers: Which roles dominate the meta chronologically?

9) Temporal Heatmap — Champion × Month (color = Pick % or Win %)

Type: Heatmap (matrix)

Purpose: quick view of who was hot/cold each month

Answers: When did champs spike?

10) Animated Rank / Pick% Chart (gganimate) — “Top movers”

Type: Animated bar chart race or animated line for top champions

Purpose: show month-to-month dynamics visually (animation gives intuition on momentum)

Answers: Who rose/fell fastest over the year?

Implementation: gganimate (R) or Plotly animation (Python). Code below.

11) AI-Generated Infographic (image) — executive summary of latest month

Type: AI-generated stylized chart/infographic image (DALL·E or similar)

Purpose: polished infographic for social sharing / executive summary

Answers: “What’s the meta this month?” (top picks, top win% champ, dominant class, role share)

Implementation: compute aggregates, feed numbers into AI prompt, include alt text and an explanation of the pipeline.
