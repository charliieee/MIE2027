"""03_age_models.py

CDSS item by age band, and logistic regressions of "unclear what this is" on
age (one unit = one decade), unadjusted and adjusted, for the CDSS item and
for each of the 18 other tools.

Reads analytical_sample.csv (written by 01_prepare_sample.py).
Writes data/aggregated/cdss_by_age.csv and data/aggregated/regression_age.csv.

Run from the repository root:  python code/03_age_models.py
"""
import importlib.util
import warnings
from pathlib import Path
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("prep", ROOT / "code" / "01_prepare_sample.py")
prep = importlib.util.module_from_spec(spec); spec.loader.exec_module(prep)
TOOL_LABELS, CDSS_ITEM = prep.TOOL_LABELS, prep.CDSS_ITEM

COLLAPSED = {"daily": "daily_weekly", "weekly": "daily_weekly",
             "monthly": "monthly_less", "less_often": "monthly_less",
             "would_like": "would_like", "unclear": "unclear"}
CATS = ["daily_weekly", "monthly_less", "would_like", "unclear"]
# adjustment set of the model reported in the manuscript
COVARIATES = "C(setting) + C(specialty_group)"


def fit_or(df: pd.DataFrame, formula: str) -> tuple[float, float, float, float, int]:
    """Odds ratio per decade with 95% CI and p value for the age term."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        m = smf.logit(formula, df).fit(disp=0)
    ci = np.exp(m.conf_int().loc["age_ord"])
    return float(np.exp(m.params["age_ord"])), float(ci[0]), float(ci[1]), float(m.pvalues["age_ord"]), int(m.nobs)


def main() -> None:
    d = pd.read_csv(ROOT / "analytical_sample.csv")
    cdss_col = f"tool_{CDSS_ITEM:02d}"
    dc = d[d[cdss_col].notna()].copy()
    dc["cat"] = dc[cdss_col].map(COLLAPSED)

    # ---- CDSS item by age band and by three age groups
    rows = []
    for level, grouper in [("band", "age_band"), ("group", "age_group3")]:
        for g, s in dc.groupby(grouper, sort=False):
            n = len(s)
            vc = s["cat"].value_counts()
            row = {"level": level, "age": g, "n": n}
            for c in CATS:
                row[c] = int(vc.get(c, 0))
                row[f"{c}_pct"] = round(row[c] / n * 100, 1)
            rows.append(row)
    A = pd.DataFrame(rows)
    order_band = list(prep.AGE_ORD); order_group = ["<40", "40-59", ">=60"]
    A["sort"] = A.apply(lambda r: (0, order_band.index(r["age"])) if r["level"] == "band" else (1, order_group.index(r["age"])), axis=1)
    A = A.sort_values("sort").drop(columns="sort")
    A.to_csv(ROOT / "data" / "aggregated" / "cdss_by_age.csv", index=False)

    g = A[A["level"] == "group"].set_index("age")
    assert round(g.loc["<40", "unclear_pct"]) == 51 and round(g.loc[">=60", "unclear_pct"]) == 27
    assert round(g.loc["<40", "would_like_pct"]) == 16 and round(g.loc[">=60", "would_like_pct"]) == 29
    print("CDSS item by age group:")
    print(g[["n", "unclear_pct", "would_like_pct", "daily_weekly_pct", "monthly_less_pct"]].round(1).to_string())

    # ---- logistic regressions, CDSS and all other tools
    out = []
    for k in range(1, 20):
        col = f"tool_{k:02d}"
        s = d[d[col].notna()].copy()
        s["unclear"] = (s[col] == "unclear").astype(float)
        if s["unclear"].sum() < 5:          # too few events for a stable estimate
            out.append({"item": k, "tool": TOOL_LABELS[k], "n": len(s), "n_unclear": int(s["unclear"].sum())})
            continue
        u = fit_or(s, "unclear ~ age_ord")
        a = fit_or(s, f"unclear ~ age_ord + {COVARIATES}")
        out.append({"item": k, "tool": TOOL_LABELS[k], "n": len(s), "n_unclear": int(s["unclear"].sum()),
                    "or_unadj": round(u[0], 3), "ci_lo_unadj": round(u[1], 3), "ci_hi_unadj": round(u[2], 3), "p_unadj": round(u[3], 4),
                    "or_adj": round(a[0], 3), "ci_lo_adj": round(a[1], 3), "ci_hi_adj": round(a[2], 3), "p_adj": round(a[3], 4)})
    R = pd.DataFrame(out)
    R.attrs["adjustment"] = COVARIATES
    R.to_csv(ROOT / "data" / "aggregated" / "regression_age.csv", index=False)

    c = R[R["item"] == CDSS_ITEM].iloc[0]
    assert round(c["or_adj"], 2) == 0.72, f"adjusted OR per decade for CDSS is {c['or_adj']}, manuscript reports 0.72"
    print(f"\nCDSS, 'unclear' on age per decade: unadjusted OR {c['or_unadj']:.2f} ({c['ci_lo_unadj']:.2f}-{c['ci_hi_unadj']:.2f}); "
          f"adjusted for {COVARIATES}: OR {c['or_adj']:.2f} ({c['ci_lo_adj']:.2f}-{c['ci_hi_adj']:.2f})")
    others = R[(R["item"] != CDSS_ITEM) & R["or_adj"].notna()]
    dec = others[(others["ci_hi_adj"] < 1)]
    inc = others[(others["ci_lo_adj"] > 1)]
    print(f"other tools, adjusted: {len(dec)} with a significant decreasing gradient, {len(inc)} with an increasing one"
          + (": " + ", ".join(f"{r['tool']} OR {r['or_adj']:.2f}" for _, r in inc.iterrows()) if len(inc) else ""))
    print("written: data/aggregated/cdss_by_age.csv, data/aggregated/regression_age.csv")


if __name__ == "__main__":
    main()
