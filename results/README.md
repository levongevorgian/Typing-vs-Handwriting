# Numerical outputs

All CSV values retain calculation precision. The PDF rounds for readability. This folder is rebuilt by `analysis/analyze.py` (except report_content.json, written by the report builder).

| File | Purpose |
|---|---|
| data_audit.json | Counts, missingness, rows removed, SHA-256 |
| descriptive_statistics.csv | n, mean, median, SD, variance, SE, min/max, quartiles, IQR, skew and flags |
| lecture_counts.csv | Group sizes within each recorded talk |
| welch_tests.csv | Main and secondary differences, SE, t, df, raw p, CI; Holm p for 3 secondary tests |
| normal_model_intervals.csv | Per-group mean and SD CIs, prediction and normal tolerance intervals |
| distribution_checks.csv | Shapiro–Wilk, Brown–Forsythe and Mann–Whitney checks |
| simple_regression.csv | Group-only OLS coefficients; classical and HC3 uncertainty |
| lecture_regression.csv | Lecture-adjusted coefficients; classical and HC3 uncertainty |
| model_comparisons.csv | Partial condition F and condition-by-lecture interaction F |
| regression_diagnostics.csv | Fitted values, residuals, leverage, studentized residuals, Cook distances |
| correlations.csv | Overall and group-specific Pearson/Fisher CI and Spearman results |
| illustrative_proportions.csv | >=70 proportions and Wilson CIs |
| categorical_test.csv | Pooled z and equivalent Pearson chi-square (no continuity correction) |
| power_planning.csv | Assumed effects, approximate current-design power and balanced future n |
| analysis.json | Combined results, diagnostics, chart captions and dependency versions |
| report_content.json | Structured explanatory report content |

`lower` and `upper` in regression tables are classical t intervals. `HC3_lower`, `HC3_upper` and `HC3_p_normal` use robust HC3 SEs with an asymptotic normal reference. The adjusted summary uses the latter. SD and tolerance intervals depend strongly on the normal model; see the report before interpreting them.
