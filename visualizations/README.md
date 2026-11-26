# Standalone visualizations

Each chart is saved separately in PNG and SVG.

## Score Distributions by Note-Taking Method

[PNG](01_score_distributions.png) · [SVG](01_score_distributions.svg)

Dots: participants; boxes: middle 50%; line: median; diamond: mean. All observations retained.

## Overall Score Distributions

[PNG](02_histograms.png) · [SVG](02_histograms.svg)

Identical bins and axes; the last bin includes 100.

## Normal Probability Plots of Overall Scores

[PNG](03_normal_probability.png) · [SVG](03_normal_probability.svg)

Tail departures and bounded scores matter especially for individual prediction, variance and tolerance intervals.

## Mean Differences and 95% Confidence Intervals

[PNG](04_mean_difference_intervals.png) · [SVG](04_mean_difference_intervals.svg)

Intervals are individual 95% intervals, not simultaneous family intervals. Secondary p-values are Holm-adjusted separately.

## Welch Two-Sample t-Test for Overall Scores

[PNG](05_hypothesis_test.png) · [SVG](05_hypothesis_test.svg)

Shading represents both tails at least as far from zero as the observed statistic. The p-value is not the probability that the null is true.

## Mean Scores by Question Type and Note-Taking Method

[PNG](06_question_type.png) · [SVG](06_question_type.svg)

Lines summarize means, not individual change over time. The formal comparison uses conceptual minus factual within each participant.

## Mean Overall Scores by Lecture and Note-Taking Method

[PNG](07_lecture_means.png) · [SVG](07_lecture_means.svg)

Small subgroups have wide intervals. These are descriptive means with marginal t intervals, not five independent confirmatory tests.

## Unadjusted and Lecture-Adjusted Mean Differences

[PNG](08_adjusted_comparison.png) · [SVG](08_adjusted_comparison.svg)

Adjusted result uses an additive model with lecture indicators and a common typing effect; its approximate 95% interval uses HC3 standard errors and a normal critical value.

## Lecture-Adjusted Regression Diagnostics

[PNG](09_regression_diagnostics.png) · [SVG](09_regression_diagnostics.svg)

Residual shape, unequal spread and influential observations limit model accuracy. Dashed Cook threshold 4/n is a screening rule, not an exclusion rule.

## Association Between Factual and Conceptual Scores

[PNG](10_factual_conceptual.png) · [SVG](10_factual_conceptual.svg)

Each point is one participant. Correlation is exploratory and does not demonstrate causation; overall is not correlated with its own components.

## Proportions of Participants Scoring at Least 70

[PNG](11_illustrative_threshold.png) · [SVG](11_illustrative_threshold.svg)

70 is an exploratory threshold, not an official pass mark. Error bars are Wilson 95% confidence intervals.

## Statistical Power by Assumed Mean Difference

[PNG](12_power_planning.png) · [SVG](12_power_planning.svg)

Normal planning approximation at two-sided alpha .05, with common SD estimated from this sample. This is scenario analysis, not evidence for the null.

## Confidence, Prediction and Tolerance Intervals

[PNG](13_interval_purposes.png) · [SVG](13_interval_purposes.svg)

Mean CIs and prediction intervals are 95%; tolerance intervals have 90% population content and 95% confidence under normality. Values beyond 100 expose the normal model limitation; they are not clipped.