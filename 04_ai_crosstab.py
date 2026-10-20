"""04_ai_crosstab.py

AI use for diagnostic tasks against the CDSS item (Supplement S3), overall and
by age group, with chi-square test and age-adjusted odds ratio for
"unclear what this is".

Reads analytical_sample.csv (written by 01_prepare_sample.py).
Writes data/aggregated/s3_ai_use_by_cdss.csv.

Run from the repository root:  python code/04_ai_crosstab.py
"""
import importlib.util
import warnings
from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("prep", ROOT / "code" / "01_prepare_sample.py")
prep = importlib.util.module_from_spec(spec); spec.loader.exec_module(prep)
CDSS_ITEM = prep.CDSS_ITEM

COLLAPSED = {"daily": "daily_weekly", "weekly": "daily_weekly",
             "monthly": "monthly_less", "less_often": "monthly_less",
             "would_like": "would_like", "unclear": "unclear"}
CATS = ["daily_weekly", "monthly_less", "would_like", "unclear"]


def block(s: pd.DataFrame, subgroup: str) -> list[dict]:
    rows = []
    for flag in (1, 0):
        ss = s[s["ai_use_diagnostics"] == flag]
        n = len(ss)
        vc = ss["cat"].value_counts()
        row = {"subgroup": subgroup, "ai_use_diagnostics": flag, "n": n}
        for c in CATS:
            row[c] = int(vc.get(c, 0))
            row[f"{c}_pct"] = round(row[c] / n * 100, 1) if n else np.nan
        rows.append(row)
    return rows


def or_ci(a: int, b: int, c: int, d: int) -> tuple[float, float, float]:
    """Odds ratio for a 2x2 table [[a, b], [c, d]] with Woolf 95% CI."""
    orr = (a * d) / (b * c)
    se = np.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
    return orr, float(np.exp(np.log(orr) - 1.96 * se)), float(np.exp(np.log(orr) + 1.96 * se))


def main() -> None:
    d = pd.read_csv(ROOT / "analytical_sample.csv")
    cdss_col = f"tool_{CDSS_ITEM:02d}"
    dc = d[d[cdss_col].notna()].copy()
    dc["cat"] = dc[cdss_col].map(COLLAPSED)
    dc["unclear"] = (dc["cat"] == "unclear").astype(float)

    rows = block(dc, "all")
    for g in ["<40", "40-59", ">=60"]:
        rows += block(dc[dc["age_group3"] == g], f"age {g}")
    S3 = pd.DataFrame(rows)
    S3.to_csv(ROOT / "data" / "aggregated" / "s3_ai_use_by_cdss.csv", index=False)

    # 2x2: AI use for diagnostics x unclear
    t = pd.crosstab(dc["ai_use_diagnostics"], dc["unclear"])
    a, b = int(t.loc[1, 1.0]), int(t.loc[1, 0.0])      # AI users: unclear / not
    c, dd = int(t.loc[0, 1.0]), int(t.loc[0, 0.0])     # non-users
    orr, lo, hi = or_ci(a, b, c, dd)
    chi2, p_chi, _, _ = stats.chi2_contingency(t, correction=False)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        m = smf.logit("unclear ~ ai_use_diagnostics + age_ord", dc).fit(disp=0)
    or_adj = float(np.exp(m.params["ai_use_diagnostics"]))
    ci_adj = np.exp(m.conf_int().loc["ai_use_diagnostics"])

    assert a + b == 81 and a == 27
    assert round(a / (a + b) * 100) == 33 and round(c / (c + dd) * 100) == 44
    assert round(orr, 2) == 0.65
    print(f"AI use for diagnostic tasks: n = {a + b}; 'unclear' among users {a}/{a + b} ({a / (a + b) * 100:.0f}%) "
          f"vs non-users {c}/{c + dd} ({c / (c + dd) * 100:.0f}%)")
    print(f"OR {orr:.2f} (95% CI {lo:.2f}-{hi:.2f}), chi-square p = {p_chi:.3f}; "
          f"adjusted for age: OR {or_adj:.2f} ({ci_adj[0]:.2f}-{ci_adj[1]:.2f})")
    for g in ["<40", "40-59", ">=60"]:
        s = dc[dc["age_group3"] == g]
        u1 = s[s["ai_use_diagnostics"] == 1]["unclear"]; u0 = s[s["ai_use_diagnostics"] == 0]["unclear"]
        print(f"  age {g:6s}: unclear among AI users {int(u1.sum())}/{len(u1)} ({u1.mean() * 100:.0f}%), "
              f"non-users {int(u0.sum())}/{len(u0)} ({u0.mean() * 100:.0f}%)")
    print("S3 written: data/aggregated/s3_ai_use_by_cdss.csv")


if __name__ == "__main__":
    main()
