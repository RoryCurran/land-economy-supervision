"""
Home market effect in UK employment: industry-by-industry size elasticities.

Question (see question.md): do larger functional regions hold a more-than-
proportional share of jobs in tradable, increasing-returns industries, and only
a proportional share in local services?

For each 4-digit SIC industry k we estimate, across regions i,

    E[emp_ik] = exp(a_k + b_k * ln(size_i))

where size_i is total employment in region i *excluding* industry k (so a big
industry is not mechanically correlated with its own region's size).

    b_k > 1  -> magnification: big regions get a more-than-proportional share
                (the home-market-effect signature, lambda* > theta in L3-4)
    b_k = 1  -> industry simply scales with the region (local services)
    b_k < 1  -> industry over-represented in small regions (e.g. land-based)

Estimated by Poisson pseudo-maximum likelihood (PPML), the standard estimator
in the gravity literature, which keeps regions with zero employment rather
than dropping them as a log-log OLS would. Log-log OLS on non-zero regions is
reported alongside as a check.

Usage (from the repo root):
    python code/hme_elasticities.py data/raw/bres_ttwa_4digit_2024.csv outputs/ttwa
    # robustness: drop named regions (comma-separated), e.g. London
    python code/hme_elasticities.py data/raw/bres_ttwa_4digit_2024.csv outputs/ttwa_exlondon London

Input: either the wide "table" CSV from the Nomis web query tool (the
Employment block is used) or a long-format Nomis API CSV with GEOGRAPHY_CODE,
INDUSTRY_NAME and OBS_VALUE. See sources.md for the exact download.
"""

import re
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import spearmanr

# Industries to spotlight. Grouped by what the theory predicts.
SPOTLIGHT = {
    # Local, non-tradable services: expect b close to 1
    "9602": ("Hairdressing & beauty", "local"),
    "8520": ("Primary education", "local"),
    "8621": ("GP practices", "local"),
    "4711": ("Supermarkets", "local"),
    "5610": ("Restaurants", "local"),
    # Rarer health service, cf. Dingel et al.: expect above GPs
    "8610": ("Hospitals", "health"),
    # Tradable, increasing-returns services: expect b > 1
    "6910": ("Legal activities", "tradable"),
    "6419": ("Banking", "tradable"),
    "6201": ("Computer programming", "tradable"),
    "7022": ("Management consultancy", "tradable"),
    "6612": ("Securities brokerage", "tradable"),
    "7311": ("Advertising agencies", "tradable"),
    "7211": ("Biotech R&D", "tradable"),
}
GROUP_COLOURS = {"local": "#4C78A8", "health": "#B279A2", "tradable": "#E45756"}

MIN_NATIONAL_EMP = 2000  # skip tiny industries: too noisy after Nomis rounding


EMPLOYMENT_STATUS = "Employment"  # employees + working owners; see sources.md


def load_nomis_wide(path: Path):
    """Read the 'table' CSV that the Nomis web query tool downloads.

    That file holds one or more blocks, each headed by metadata lines
    (e.g. "Employment status:","Employment") and then a header row
    "Industry", <region>, "", <region>, "", ... where every value column is
    followed by a flag column. Missing values are "-". We keep the block whose
    employment status matches EMPLOYMENT_STATUS.
    """
    import csv
    with open(path, encoding="utf-8-sig") as fh:
        rows = list(csv.reader(fh))
    status, blocks = None, {}
    i = 0
    while i < len(rows):
        r = rows[i]
        if r and r[0].startswith("Employment status"):
            status = r[1].strip()
        if r and r[0] == "Industry":
            regions = r[1::2]
            records = []
            i += 1
            while i < len(rows) and not rows[i]:  # blank line after header
                i += 1
            while i < len(rows) and rows[i] and re.match(r"^\d{4} :", rows[i][0]):
                records.append([rows[i][0]] + rows[i][1::2])
                i += 1
            blocks[status] = (regions, records)
            continue
        i += 1
    if EMPLOYMENT_STATUS not in blocks:
        sys.exit(f"No '{EMPLOYMENT_STATUS}' table found; tables present: "
                 f"{list(blocks)}")
    regions, records = blocks[EMPLOYMENT_STATUS]
    wide = pd.DataFrame(records, columns=["INDUSTRY_NAME"] + regions)
    df = wide.melt(id_vars="INDUSTRY_NAME", var_name="GEOGRAPHY_CODE",
                   value_name="OBS_VALUE")
    # Industries with any missing ("-") cell are dropped, not zero-filled.
    bad = df.loc[df["OBS_VALUE"].str.strip() == "-", "INDUSTRY_NAME"].unique()
    if len(bad):
        print(f"Dropping {len(bad)} industries with missing values: "
              + "; ".join(bad))
    df = df[~df["INDUSTRY_NAME"].isin(bad)]
    df["GEOGRAPHY_NAME"] = df["GEOGRAPHY_CODE"]
    return df


def load_nomis(path: Path) -> pd.DataFrame:
    """Read a Nomis CSV (long API format or wide web-table format) and return
    a region x industry matrix."""
    with open(path, encoding="utf-8-sig") as fh:
        first = fh.readline()
    if "GEOGRAPHY_CODE" in first.upper():
        df = pd.read_csv(path)
    else:
        df = load_nomis_wide(path)
    df.columns = [c.upper() for c in df.columns]
    needed = {"GEOGRAPHY_CODE", "GEOGRAPHY_NAME", "INDUSTRY_NAME", "OBS_VALUE"}
    missing = needed - set(df.columns)
    if missing:
        sys.exit(
            f"Input is missing columns {missing}. Download the long-format API "
            "CSV described in sources.md, not the wide 'table' layout."
        )
    # Guard against a download that mixes years or measures.
    for col in ("DATE", "MEASURES_NAME", "EMPLOYMENT_STATUS_NAME"):
        if col in df.columns and df[col].nunique() > 1:
            sys.exit(f"Input has several values of {col}: {df[col].unique()}. "
                     "Filter to one before running.")

    df["SIC4"] = df["INDUSTRY_NAME"].astype(str).str.extract(r"^(\d{4})")[0]
    df = df.dropna(subset=["SIC4"])
    df["OBS_VALUE"] = pd.to_numeric(df["OBS_VALUE"], errors="coerce").fillna(0)
    names = (df.drop_duplicates("SIC4").set_index("SIC4")["INDUSTRY_NAME"]
               .str.replace(r"^\d{4}\s*:\s*", "", regex=True))
    emp = df.pivot_table(index="GEOGRAPHY_CODE", columns="SIC4",
                         values="OBS_VALUE", aggfunc="sum").fillna(0)
    return emp, names


def estimate(emp: pd.DataFrame, names: pd.Series) -> pd.DataFrame:
    total = emp.sum(axis=1)
    rows = []
    for k in emp.columns:
        y = emp[k]
        if y.sum() < MIN_NATIONAL_EMP:
            continue
        size = total - y
        keep = size > 0
        X = sm.add_constant(np.log(size[keep]))
        res = sm.GLM(y[keep], X, family=sm.families.Poisson()).fit(cov_type="HC1")
        b, se = res.params.iloc[1], res.bse.iloc[1]

        nz = keep & (y > 0)
        ols_b = np.nan
        if nz.sum() >= 10:
            ols = sm.OLS(np.log(y[nz]), sm.add_constant(np.log(size[nz]))).fit()
            ols_b = ols.params.iloc[1]

        rows.append({
            "sic4": k,
            "industry": names.get(k, k),
            "national_emp": y.sum(),
            "regions_nonzero": int((y > 0).sum()),
            "regions_total": int(keep.sum()),
            "b_ppml": b,
            "se": se,
            "ci_low": b - 1.96 * se,
            "ci_high": b + 1.96 * se,
            "b_ols_nonzero": ols_b,
        })
    out = pd.DataFrame(rows)
    out["sig_above_1"] = out["ci_low"] > 1
    out["sig_below_1"] = out["ci_high"] < 1
    return out.sort_values("b_ppml", ascending=False)


def fig_spotlight(res: pd.DataFrame, path: Path) -> None:
    s = res[res["sic4"].isin(SPOTLIGHT)].copy()
    s["label"] = s["sic4"].map(lambda k: SPOTLIGHT[k][0])
    s["group"] = s["sic4"].map(lambda k: SPOTLIGHT[k][1])
    s = s.sort_values("b_ppml")
    fig, ax = plt.subplots(figsize=(7, 0.42 * len(s) + 1.2))
    yy = np.arange(len(s))
    for i, (_, r) in enumerate(s.iterrows()):
        c = GROUP_COLOURS[r["group"]]
        ax.plot([r["ci_low"], r["ci_high"]], [i, i], color=c, lw=2, alpha=0.6)
        ax.plot(r["b_ppml"], i, "o", color=c, ms=7)
    ax.axvline(1, color="0.3", ls="--", lw=1)
    ax.text(1, len(s) - 0.4, " proportional (b = 1)", va="bottom", fontsize=8,
            color="0.3")
    ax.set_yticks(yy, s["label"])
    ax.set_xlabel("Elasticity of industry employment to region size (PPML, 95% CI)")
    handles = [plt.Line2D([], [], marker="o", ls="", color=c, label=g)
               for g, c in GROUP_COLOURS.items()]
    ax.legend(handles=handles, frameon=False, fontsize=8, loc="lower right")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def fig_all(res: pd.DataFrame, path: Path) -> None:
    """Every industry: elasticity against national size, goods vs services."""
    services = res["sic4"].str[:2].astype(int) >= 45
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for mask, colour, label in [(~services, "0.75", "Goods & primary (SIC 01-43)"),
                                (services, "0.35", "Services (SIC 45-99)")]:
        ax.scatter(np.log10(res.loc[mask, "national_emp"]),
                   res.loc[mask, "b_ppml"], s=10, color=colour, alpha=0.7,
                   lw=0, label=label)
    s = res[res["sic4"].isin(SPOTLIGHT)]
    for _, r in s.iterrows():
        ax.scatter(np.log10(r["national_emp"]), r["b_ppml"], s=30, zorder=3,
                   color=GROUP_COLOURS[SPOTLIGHT[r["sic4"]][1]])
    ax.axhline(1, color="0.3", ls="--", lw=1)
    ax.set_xlabel("National employment in industry (log10)")
    ax.set_ylabel("Elasticity to region size (PPML)")
    ax.legend(frameon=False, fontsize=8, loc="lower left")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def main(infile: str, outprefix: str, exclude: str = "") -> None:
    emp, names = load_nomis(Path(infile))
    if exclude:
        drop = [r.strip() for r in exclude.split(",")]
        unknown = set(drop) - set(emp.index)
        if unknown:
            sys.exit(f"Regions not found: {unknown}")
        emp = emp.drop(index=drop)
        print(f"Excluding regions: {drop}")
    print(f"{emp.shape[0]} regions x {emp.shape[1]} industries, "
          f"{emp.values.sum():,.0f} jobs in total")
    res = estimate(emp, names)
    out = Path(outprefix)
    out.parent.mkdir(parents=True, exist_ok=True)
    res.to_csv(f"{out}_elasticities.csv", index=False)
    fig_spotlight(res, Path(f"{out}_fig1_spotlight.png"))
    fig_all(res, Path(f"{out}_fig2_all_industries.png"))

    rho, p = spearmanr(np.log(res["national_emp"]), res["b_ppml"])
    print(f"Industries estimated: {len(res)}")
    print(f"  significantly above 1: {res['sig_above_1'].sum()}")
    print(f"  significantly below 1: {res['sig_below_1'].sum()}")
    print(f"Spearman(log national employment, b): {rho:.2f} (p = {p:.3g})")
    services = res["sic4"].str[:2].astype(int) >= 45
    for lab, m in [("goods & primary", ~services), ("services", services)]:
        r_, p_ = spearmanr(np.log(res.loc[m, "national_emp"]), res.loc[m, "b_ppml"])
        print(f"  within {lab} ({m.sum()} industries): {r_:.2f} (p = {p_:.3g})")
    cols = ["sic4", "industry", "b_ppml", "ci_low", "ci_high", "b_ols_nonzero"]
    spot = res[res["sic4"].isin(SPOTLIGHT)][cols]
    print("\nSpotlight industries:\n" + spot.to_string(index=False,
                                                       float_format="%.2f"))
    missing = set(SPOTLIGHT) - set(res["sic4"])
    if missing:
        print(f"\nNote: spotlight codes not estimated (absent or too small): "
              f"{sorted(missing)}")


if __name__ == "__main__":
    if len(sys.argv) not in (3, 4):
        sys.exit(__doc__)
    main(*sys.argv[1:])
