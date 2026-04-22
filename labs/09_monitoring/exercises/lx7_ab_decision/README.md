# LX-7 · A/B test with a decision memo

Pairs with [Demo 7](../../demos/7_ab_analysis/README.md). ~50 minutes.

## Background

You're the DRI (directly-responsible individual) for the triage
agent. Leadership emailed at 9am: "the bigger model is 16x the
price but supposedly much smarter — can we switch?" By EOD they
want a one-pager that either says "yes, ship", "no, don't ship", or
"here's what we'd need to decide".

You have 800 calls of real traffic, collected over a 7-day A/B
window. arm A = gpt-4o-mini (current), arm B = gpt-4o (candidate).
The split is 50/50. Your job is to:

1. Compute 95% CIs per arm (for context) and a 95% CI on the
   *difference* B − A (for the decision) for four metrics.
2. Decide whether each difference is significant — i.e. whether
   its 95% CI excludes zero. That is your evidence criterion.
3. Write a decision memo that weighs the four metrics against each
   other and commits to a recommendation.

This is the exercise that tests whether the rest of L10 stuck.
You'll use Stage-A style flat rows (`ab_calls.ndjson`), you'll
pretend you're reading them off a dashboard like Demo 7's, and you'll
produce a document — not a line of Python — as the real deliverable.

## Task

1. **Implement `compare_arms(calls)`** in `starter.py`. The helpers
   (`wilson`, `bootstrap_ci`, `bootstrap_ci_diff`, `median`,
   `mean`) are already written; you use them to build a per-metric
   comparison dict. See the docstring for the expected shape.
2. **Run `python starter.py`.** You'll get a table with three rows
   per metric (A, B, B − A). The decision row has the CI on the
   difference and a "CI excludes 0?" flag. Which metrics come back
   significant? Which are too close to call?
3. **Copy `DECISION_MEMO_TEMPLATE.md` to `DECISION_MEMO.md`** and
   fill it in. Target: ≤ 300 words total.

## Rules

1. **No external stats libraries.** Use only the helpers in
   `starter.py`. The point of the exercise is that you can run this
   analysis *in a notebook* on a plane; it shouldn't require scipy.
2. **No point estimates without CIs in the memo.** Every number
   you cite has a confidence interval attached. "B is 30% faster"
   without "[CI: X% to Y%]" is not a finding; it's a vibe.
3. **Decide on the CI of the difference, not p-values and not
   per-arm CI overlap.** Put the interval on the quantity you
   actually care about (B − A). Two overlapping per-arm CIs can
   coexist with a CI on the difference that excludes zero, so the
   overlap rule is conservative and misses real effects.
4. **You must commit to a recommendation.** "More data needed" is
   a valid recommendation; "I can't decide" is not.

## Success criteria

Your submission passes when:

1. `python starter.py` runs without raising `NotImplementedError`
   and prints the three-row-per-metric table.
2. `DECISION_MEMO.md` exists, is ≤ 300 words, and has:
   - A paragraph per metric citing both arms' point estimates, the
     95% CI on the difference, and whether the CI excludes zero.
   - A trade-off paragraph.
   - A concrete recommendation (one of the four from the template)
     plus a named flip-condition.
3. The memo is internally consistent: if you say "ship B on urgent
   tickets", the numbers you cited can plausibly justify that
   segmentation; if you say "don't ship", none of the arm-B
   metrics should be winning outright.

## Hints

- **Wilson for per-arm proportions, bootstrap for per-arm
  continuous, bootstrap_ci_diff for the difference on everything.**
  Schema-fail and PII-block rates are proportions; latency and cost
  are continuous. For the difference CI, represent proportion
  metrics as 0/1 indicator arrays and pass `stat=mean`.
- **"Significant" means the CI on the difference excludes zero.**
  If `diff["lo"] > 0` the arms differ and B is larger; if
  `diff["hi"] < 0` they differ and B is smaller; if zero is inside
  the interval, you cannot distinguish them at 95% confidence.
- **Seed the bootstrap.** Use the default seed in `bootstrap_ci`
  and `bootstrap_ci_diff`. Same data → same CI every time.
  Reproducibility is an analytical feature, not a luxury.
- **The 800 calls is small.** Power-wise, this is enough for
  effect sizes of ~5 percentage points on proportions and ~40 ms
  on latency. Smaller effects will wash out. If the CI on the
  difference straddles zero by a point or two, that's not a
  signal — that's the sample size talking.
- **The cost metric is a trap.** Mean cost is ~16x between arms,
  CI on the difference tight and trivially non-zero. Don't let it
  dominate. The product call is whether other wins *justify* the
  cost, not whether a difference exists.

## What to submit

- Your patched `starter.py` (or a separate `solution.py`).
- `DECISION_MEMO.md` filled in per the template.

## Common pitfalls

- **Quoting the raw delta and forgetting the CI on the difference.**
  "B is 43 ms slower" is only half a finding. Without "[CI:
  +30 to +55 ms]" on the difference you can't tell if the effect is
  large-and-certain or small-and-noisy.
- **Deciding by "do the per-arm CIs overlap?"** The overlap rule
  corresponds to a stricter significance test (roughly α ≈ 0.006
  instead of 0.05) because it adds the two SEs linearly rather
  than in quadrature. It will tell you "no effect" on real
  regressions. Decide on the CI of the difference.
- **Ignoring the floor / ceiling.** A 2% PII-block rate with
  difference CI [−1 pp, +2 pp] is a tie. Both arms sit in the same
  range. You're measuring noise.
- **Writing a memo in the present tense.** A/B findings are
  historical claims about the collection window ("B's schema-fail
  rate was 3.5%..."). "B has a lower rate" prescribes forward and
  you haven't measured forward.
- **Overfitting to the biggest delta.** Cost is a 16x difference.
  If your memo only talks about cost, you ignored three-quarters of
  the evidence. Product decisions weight the full picture.

## What this drills

- **Confidence intervals as a decision criterion.** You can make a
  ship-or-don't call from the CI on the difference alone — no
  p-values, no multiple-comparisons correction, no
  minimum-detectable-effect power calculation. For most
  engineering teams, this is the right bar.
- **Writing evidence in prose.** Most organisations don't read
  dashboards as carefully as they read memos. The dashboard is the
  inputs; the memo is the product. Practising this turns an analyst
  into a colleague.
- **Naming flip-conditions.** "I'd reverse this call if the
  latency regression grew to X" is what makes a recommendation
  useful a month from now, after more data arrives. Memos without
  flip-conditions age into fiction.
- **Commitment over hedging.** "Extend the experiment" is a
  commitment. "We don't have enough data" without naming how much
  more you'd want and what threshold you'd use is not.

## What's out of scope

- **Bayesian priors / posteriors.** A Bayesian report would give a
  posterior over the lift with 95% credible bands. Arguably more
  natural; takes more setup. Stick with frequentist Wilson +
  bootstrap-on-difference.
- **Segmentation by ticket urgency.** The data includes
  `ticket.urgency`. If you have spare time, slicing by urgency
  changes the story — B's gains might concentrate on urgency ≥ 7.
  Optional.
- **Deploying the winner.** A real flow gates the ramp behind a
  canary rollout, automated guardrail triggers, and a rollback
  runbook. Out of scope for the memo; mentioned for your plan.
