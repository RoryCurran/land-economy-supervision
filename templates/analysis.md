# Analysis

- **Software / dependencies:** Python 3.10+, with pandas, numpy, statsmodels, scipy and matplotlib.
  `pip install pandas numpy statsmodels scipy matplotlib`

- **Input files and locations:** `data/raw/bres_ttwa_4digit.csv`. This is the Nomis long-format CSV; see `sources.md` for the download.

- **Steps or commands, in order:**
  1. Download the BRES data as described in `sources.md`.
  2. From the repo root, run:
     `python code/hme_elasticities.py data/raw/bres_ttwa_4digit.csv outputs/ttwa`
  3. The script then does the following:
     - Pivots the data to a region × industry matrix of jobs.
     - For each industry *k* with at least 2,000 jobs nationally, estimates the following by **Poisson pseudo-maximum likelihood**, with heteroskedasticity-robust (HC1) standard errors:

       E[emp_ik] = exp(a_k + b_k · ln size_i)

       Here size_i is total employment in TTWA *i* excluding industry *k*. Excluding *k* stops large industries from being mechanically correlated with their own regions' size.
     - Reports log-log OLS on regions with non-zero employment as a check. If OLS and PPML differ a lot, the zeros matter.
     - Saves the full results table and two figures, and prints a summary. The summary includes the Spearman correlation between *b* and the log of national employment, which tests the "rarer → more concentrated" prediction.

- **Output files:** listed in `outputs.md`.

- **Planned robustness checks:**
  - Replace size with resident population (Dataset 2), which measures demand directly.
  - Rerun at local-authority level. Commuting should distort the results there: the City of London and Westminster should become extreme outliers. That is a direct illustration of why the functional region is the right unit.
  - Change the minimum-size threshold to 1,000 and 5,000 jobs.
