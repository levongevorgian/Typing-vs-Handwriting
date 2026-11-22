# Statistical decisions

The primary endpoint is the supplied overall score. All directional differences are typing minus handwriting. The groups are independent; factual and conceptual scores within a participant are paired. The primary test is two-sided Welch at alpha .05, chosen without a preliminary equal-variance test. Its 95% interval uses Welch–Satterthwaite degrees of freedom. Quartiles use linear interpolation. Sample variances use n−1.

The factual, conceptual and difference-of-gaps tests form an exploratory family of three; Holm-adjusted p-values are saved alongside raw p-values. Individual 95% intervals are not simultaneous family intervals. Other supporting tests are exploratory; their unadjusted p-values do not support a search for significant effects. This is a reanalysis with known prior results, not a new preregistered experiment.

Regression uses an intercept, typing indicator and four fixed lecture indicators with algorithms as reference. It estimates a common condition effect within the five lectures. Both classical t-based and HC3 normal-approximation intervals/p-values are saved; the adjusted comparison figure uses HC3 to match earlier Stage 5. This is not a random-lecture generalization. The interaction extension adds four condition-by-lecture terms, compared by a classical nested F-test. Partial condition F equals its classical coefficient t squared. Diagnostics include studentized residuals, leverage, Cook's distance and asymptotic Breusch–Pagan. Diagnostic flags do not delete observations.

Pearson confidence intervals use Fisher's z transform; Spearman uses SciPy's asymptotic p-value. Mann–Whitney uses a two-sided tie-corrected asymptotic calculation and tests ranks, not the same mean parameter as Welch. The >=70 threshold is illustrative; pooled z and uncorrected Pearson chi-square are equivalent, while group intervals use Wilson. These proportions are not the main outcome.

Power uses the common pooled sample SD (16.42) and a normal two-sided alpha-.05 approximation for scenarios of 3, 5, 8 and 10 points. Balanced n planning uses ceil(2 SD² (z.975 + z.80)² / difference²). These are approximate prospective scenarios, not retrospective observed-power evidence or exact Welch guarantees.

Mean and prediction intervals use t; SD intervals use chi-square. Normal tolerance factors are found numerically: integrate over Z=sqrt(n)(sample mean−population mean)/sigma and independent V=(n−1)s²/sigma² to solve Pr[Phi(Z/sqrt(n)+k sqrt(V/(n−1)))−Phi(Z/sqrt(n)−k sqrt(V/(n−1))) >= .90] = .95. Numerical quadrature covers Z from −8 to 8; the omitted normal tail probability is negligible. All are normal-model intervals. Departures and the 0–100 bound limit their literal interpretation; limits are not clipped. No bootstrap or resampling is used.

Hedges g uses the pooled sample SD and the approximate small-sample multiplier 1−3/[4(nT+nH−2)−1]. It is a descriptive standardized estimate, not an equivalence test.

The original public CSV is preserved. We do not infer scoring weights or reconstruct overall from the two component scores. The paper's abstract count discrepancy is resolved using Methods, detailed package documentation and original condition labels.
