# Outputs

| File | Description | Created by |
| --- | --- | --- |
| `outputs/ttwa_elasticities.csv` | One row per industry (476): PPML elasticity *b*, standard error, 95% CI, OLS check, national employment, number of non-zero TTWAs | `code/hme_elasticities.py` |
| `outputs/ttwa_fig1_spotlight.png` | **Headline figure.** Elasticities with 95% CIs for 13 spotlight industries, coloured by predicted group (local / health / tradable), with a reference line at *b* = 1 | `code/hme_elasticities.py` |
| `outputs/ttwa_fig2_all_industries.png` | Every industry's elasticity against national employment (log scale), with goods and services shaded differently. Tests whether rarer industries concentrate more | `code/hme_elasticities.py` |
| `outputs/ttwa_exlondon_*` | The same three outputs re-estimated without the London TTWA (robustness check) | `code/hme_elasticities.py` with `London` as the third argument |
