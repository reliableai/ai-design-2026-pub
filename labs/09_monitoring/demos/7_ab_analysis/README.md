# Demo 7 · A/B analysis on monitoring data

Pairs with Slides 37–38 of L10 (Section 05 — analysis → INTERLUDE). The final demo in L10: the shift from
*watching* the system (Stages A+B) to *deciding* about it. The data
is the same flat call-row shape from Demos 2/4 with one extra
column — `arm` ∈ {A, B} — which lets the dashboard split every
metric two ways and report confidence intervals on the differences.

## The hypothesis

The team wants to ship **prompt v3** (the *challenger*) to replace
**prompt v2** (the *champion*). v3 adds three safety-rail lines to
the system prompt:

```
Do not infer PII.
Do not give medical advice.
If the ticket references a specific person's identity, redact names.
```

The change is meant to cut schema fails (more explicit structure
instructions help the model stay in JSON mode). The cost is
~25 extra input tokens on every call. The risk is latency creep and
a possible PII-block regression.

## What's here

```
demos/7_ab_analysis/
  gen_ab_runs.py       ← 3000 synthetic calls, 50/50 A/B split
  ab_calls.ndjson      ← one call per line
  ab_calls.js          ← window.__AB_CALLS__
  ab_dashboard.html    ← KPI tiles + per-day time-series with 95% CIs
  README.md
```

## Seeded effect sizes

True population values baked into the generator (everything else is
noise):

| metric                 | arm A (v2) | arm B (v3) | direction       |
|------------------------|-----------:|-----------:|:----------------|
| schema-fail rate       |  8.0%      |  3.0%      | **B better**    |
| PII-block rate         |  2.2%      |  2.5%      | B slightly worse|
| latency p50 (ms)       |  340       |  360       | B slightly slower |
| extra input tokens     |  +0        |  +25       | B slightly pricier|

The primary story is a real 5-percentage-point drop in schema fails
against slight secondary regressions. The dashboard's job is to help
you decide whether the trade is worth it.

## How to run

```bash
python gen_ab_runs.py
open ab_dashboard.html     # or double-click it
```

You'll see four KPI tiles across the top (schema-fail, latency p50,
cost, PII-block) with arm A / arm B numbers and per-arm 95% CIs
(Wilson / bootstrap) for context. The decision flag under each
tile reads a 95% **bootstrap CI on the difference** B − A: the
arms differ on that metric iff that CI excludes zero. Below the
tiles, a decision-summary box lists which metrics B won, lost, or
tied on. Below that, four per-day line charts — shaded CI bands on
every series.

## Teaching beats (Slide 38)

1. **Put the CI on the quantity you care about.** The decision
   criterion is the 95% CI on the *difference* B − A, not "do the
   two per-arm CIs overlap?" The overlap rule adds the two SEs
   linearly (s_A + s_B); a CI on the difference combines them in
   quadrature (√(s_A² + s_B²)), which is strictly tighter. Two
   overlapping per-arm CIs can coexist with a CI on the difference
   that excludes zero — the overlap rule will miss that effect.
   Pedagogy: always ask "what is the interval I'm making a
   decision on?" and make sure it's on the relevant quantity.
2. **Read the interval, not the point.** Start with the schema-fail
   tile. 8.0% vs 3.0% looks decisive; the CI on the difference
   will come back solidly below zero. Now point at the PII tile.
   Point estimates differ by a few tenths of a pp, but the
   difference CI straddles zero — no evidence of a regression at
   this sample size.
3. **The decision box does not recommend.** It summarises wins,
   losses, ties — but ships no verdict. The call "ship B anyway
   because safety > slight latency" lives in a product-manager's
   notes, not in a dashboard. Emphasise: the analyst makes the
   numbers legible; the team makes the call.
4. **CI bands on per-day charts.** Scroll down. Each line has a
   shaded 95% per-arm band; where the two bands clearly separate
   you're confident even under the (conservative) overlap rule.
   Early days (d0–d2) the bands are fat because n is small; late
   days tighter. This graphically teaches "power scales with n" —
   but still remind students the *decision* for the whole window
   runs on the CI on the difference in the KPI tile above.
5. **Wilson vs bootstrap.** Per-arm proportion CIs use Wilson
   intervals (analytic, fast, known-accurate for small n).
   Continuous per-arm CIs and *every* difference CI use bootstrap
   (1000 resamples, seeded). Call out the engineering discipline:
   *pick one accurate method per question and apply it uniformly.*
6. **What the dashboard doesn't do.** No multiple-comparisons
   correction (4 metrics, 95% CI each → naive false-positive
   rate ~18% on at least one metric). No sequential-testing guard
   (you could peek every hour and "find" significance). No
   segmentation by model or ticket type. All of those live on
   Slide 39 as *next steps*.

## Reading the ndjson

```bash
# Per-arm outcome counts (sanity check vs the table above).
jq -r '[.arm, .outcome] | @tsv' ab_calls.ndjson |
  sort | uniq -c | sort -nr

# Median latency per arm.
jq -r 'select(.arm=="A") | .latency_ms' ab_calls.ndjson |
  sort -n | awk '{ a[NR]=$1 } END { print a[int(NR/2)] }'
```

## Where this lives on a real team

The generator and the dashboard are the *analyst's* tool, not the
*on-call's*. On-call dashboards (Demos 2/3/4) are about "is
something on fire now?" — fast paint, alert-shaped. This dashboard
is about "should we ship this change?" — slower, more statistical
machinery, run on a deliberate schedule (end of each A/B window).
Both draw from the same NDJSON row format; the split between them
is a *question*, not a *pipeline*.

## What's deliberately simple

- **50/50 split.** Some teams use 10/90 for risky changes.
  Dashboard works either way; CIs on the 10% arm are just wider.
- **No segmentation.** A production A/B report usually slices by
  model, tenant tier, ticket type. Easy extension: add a dropdown
  at the top of the page that filters the underlying `DATA`.
- **Bootstrap at n=1000.** Fast in the browser, fine for the
  in-lab window. Real reports run 10k+ resamples and cache the
  output server-side. Out of scope here.
- **No guardrail metric for outcome itself.** A responsible
  challenger rollout includes an auto-rollback trigger if any
  guardrail crosses a threshold. The decision box names that as a
  downstream concern; not implemented in the dashboard.
