"""
LX-7 · A/B analysis with a decision memo.

You're the DRI for the triage agent. Product wants to know: should
we switch from gpt-4o-mini (arm A, current) to gpt-4o (arm B,
candidate)? You have 800 calls across 7 days, 50/50 split, in
`ab_calls.ndjson`. Your job:

  1. Implement `compare_arms(calls)` below. For each of four
     metrics, return both arms' point estimate + 95% CI (for
     context) AND a 95% CI on the *difference* B − A (for the
     decision). Flag each metric as "significant" when the CI on
     the difference excludes zero.
  2. Run `python starter.py`. It prints a table. Eyeball it.
  3. Write `DECISION_MEMO.md` — ≤ 300 words — with your
     recommendation.

The decision runs on the CI of the difference, not on whether the
two per-arm CIs happen to overlap. Two overlapping per-arm CIs can
coexist with a CI on the difference that excludes zero, so the
overlap rule misses real effects. Always put the CI on the quantity
you actually care about — here, B − A.

The helpers for Wilson proportions, per-arm bootstrap means /
medians, and *bootstrap on the difference* are already written for
you. What you have to write is the *comparison* — deciding which
method to use for which metric, gathering results into a consistent
shape, and interpreting what "95% CI on the difference excludes
zero" buys you.

Four metrics to compare, in order of product priority:

  (1) schema_fail rate         (proportion, lower = better)
  (2) pii-block rate           (proportion, lower = better)
  (3) latency p50              (continuous, lower = better)
  (4) mean cost per call       (continuous, lower = better)

Decision-memo rubric (see README):
  * One paragraph per metric — point estimates (both arms),
    95% CI on the difference, whether the CI excludes zero.
  * One paragraph on trade-offs across metrics.
  * A recommendation that names: ship / don't ship / ship on a
    segment. Back it with the numbers, not with vibes.

Run:  python starter.py
"""

from __future__ import annotations

import json
import math
import random
from collections import defaultdict


# ---------------------------------------------------------------------------
# Helpers — provided. You don't need to edit these.
# ---------------------------------------------------------------------------

def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson 95% CI for a single-arm proportion. Returns (lo, hi)."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def bootstrap_ci(values: list[float], stat, n: int = 1000,
                 seed: int = 2026) -> tuple[float, float, float]:
    """Bootstrap 95% CI for `stat(values)` on a single arm.

    Returns (point, lo, hi). Use for per-arm display CIs on
    continuous metrics.
    """
    if not values:
        return (0.0, 0.0, 0.0)
    rng = random.Random(seed)
    resamples = []
    N = len(values)
    for _ in range(n):
        sample = [values[rng.randrange(N)] for _ in range(N)]
        resamples.append(stat(sample))
    resamples.sort()
    lo = resamples[int(n * 0.025)]
    hi = resamples[int(n * 0.975)]
    return (stat(values), lo, hi)


def bootstrap_ci_diff(values_A: list[float], values_B: list[float],
                      stat, n: int = 1000,
                      seed: int = 2026) -> tuple[float, float, float]:
    """Unpaired bootstrap 95% CI for stat(B) - stat(A).

    For A/B traffic where each call belongs to exactly one arm, we
    resample A and B independently and take percentiles of the
    resulting differences. If the returned interval excludes zero,
    we have evidence that the arms differ on `stat`.

    For proportion metrics, pass 0/1 indicator arrays and use
    stat=mean.

    (If you had the *same* examples scored by both arms — e.g. a
    golden-set comparison — you would instead resample example
    indices jointly. See the paired bootstrap worked example in
    the bootstrap lab.)
    """
    if not values_A or not values_B:
        return (0.0, 0.0, 0.0)
    rng = random.Random(seed)
    N_A, N_B = len(values_A), len(values_B)
    diffs = []
    for _ in range(n):
        sa = [values_A[rng.randrange(N_A)] for _ in range(N_A)]
        sb = [values_B[rng.randrange(N_B)] for _ in range(N_B)]
        diffs.append(stat(sb) - stat(sa))
    diffs.sort()
    lo = diffs[int(n * 0.025)]
    hi = diffs[int(n * 0.975)]
    return (stat(values_B) - stat(values_A), lo, hi)


def median(vals: list[float]) -> float:
    if not vals: return 0.0
    s = sorted(vals)
    mid = len(s) // 2
    return s[mid] if len(s) % 2 else (s[mid - 1] + s[mid]) / 2


def mean(vals: list[float]) -> float:
    return sum(vals) / len(vals) if vals else 0.0


# ---------------------------------------------------------------------------
# The function you implement.
# ---------------------------------------------------------------------------

def compare_arms(calls: list[dict]) -> dict:
    """Build a comparison dict of the form:

        {
          "schema_fail": {
            "kind": "proportion",
            "A": {"point": 0.056, "lo": 0.037, "hi": 0.085, "n": 374, "k": 21},
            "B": {"point": 0.035, "lo": 0.021, "hi": 0.057, "n": 426, "k": 15},
            "diff": {"point": -0.021, "lo": -0.052, "hi": 0.010},
            "significant": False,
          },
          "pii_block":   {...},
          "latency_p50": {"kind": "continuous", "A": {...}, "B": {...},
                          "diff": {...}, "significant": ...},
          "cost_mean":   {...},
        }

    Per-arm CIs (display only):
      * Use `wilson` for proportion metrics (schema_fail, pii_block).
      * Use `bootstrap_ci` with `median` for latency, `mean` for cost.

    Difference CI (the decision criterion):
      * Use `bootstrap_ci_diff` for every metric. For proportions,
        pass 0/1 indicator arrays and stat=mean. For latency use
        stat=median; for cost use stat=mean.

    `significant` is True iff the CI on the *difference* excludes
    zero (i.e. lo > 0 or hi < 0). Do not use per-arm CI overlap —
    it is conservative and misses real effects.
    """
    # TODO: implement.
    raise NotImplementedError("implement compare_arms()")


# ---------------------------------------------------------------------------
# Reporting — provided.
# ---------------------------------------------------------------------------

def load_calls(path: str = "ab_calls.ndjson") -> list[dict]:
    with open(path) as f:
        return [json.loads(line) for line in f]


def print_table(cmp: dict) -> None:
    headers = ["metric", "row", "point", "95% CI", "n", "CI excl. 0?"]
    rows = []
    for metric, info in cmp.items():
        for arm in ("A", "B"):
            d = info[arm]
            point = d["point"]
            if info["kind"] == "proportion":
                val = f"{point * 100:.2f}%"
                ci  = f"[{d['lo'] * 100:.2f}%, {d['hi'] * 100:.2f}%]"
                n_s = f"{d['n']} (k={d['k']})"
            elif metric == "cost_mean":
                val = f"${point:.6f}"
                ci  = f"[${d['lo']:.6f}, ${d['hi']:.6f}]"
                n_s = str(d["n"])
            else:
                val = f"{point:.1f} ms"
                ci  = f"[{d['lo']:.1f}, {d['hi']:.1f}]"
                n_s = str(d["n"])
            rows.append([metric if arm == "A" else "", arm, val, ci, n_s, ""])

        d = info["diff"]
        if info["kind"] == "proportion":
            val = f"{d['point'] * 100:+.2f} pp"
            ci  = f"[{d['lo'] * 100:+.2f} pp, {d['hi'] * 100:+.2f} pp]"
        elif metric == "cost_mean":
            val = f"${d['point']:+.6f}"
            ci  = f"[${d['lo']:+.6f}, ${d['hi']:+.6f}]"
        else:
            val = f"{d['point']:+.1f} ms"
            ci  = f"[{d['lo']:+.1f}, {d['hi']:+.1f}]"
        rows.append(["", "B − A", val, ci, "",
                     "yes" if info["significant"] else "no"])

    col_widths = [max(len(str(r[c])) for r in [headers] + rows)
                  for c in range(len(headers))]
    def fmt(row):
        return "  ".join(str(c).ljust(col_widths[i]) for i, c in enumerate(row))
    print(fmt(headers))
    print(fmt(["-" * w for w in col_widths]))
    for r in rows:
        print(fmt(r))


def main() -> None:
    calls = load_calls()
    try:
        cmp = compare_arms(calls)
    except NotImplementedError:
        print("compare_arms() isn't implemented yet — get to it.")
        return
    print_table(cmp)
    print("\nNow write DECISION_MEMO.md (≤ 300 words).")
    print("Rubric is in README.md; table above has the numbers you need.")


if __name__ == "__main__":
    main()
