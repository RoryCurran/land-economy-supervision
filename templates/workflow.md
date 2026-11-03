# Workflow

## 2026-11-03 / Choosing the question

- **Action and reason:** Read Lectures 1–8 and listed candidate questions that test a specific lecture prediction. Chose the home market effect (Lectures 3–4) because it makes a sharp, testable prediction (λ* > θ) with a built-in control group (non-tradable local services), and the data are a single open download.
- **Change made:** Drafted `question.md`.
- **Check and result:** Confirmed that the expected pattern can be written as a number: an elasticity above or equal to 1.
- **Next step:** Download BRES.

## 2026-11-03 / Design decisions

- **Action and reason:**
  - **Region unit:** Travel to Work Areas rather than local authorities. TTWAs are functional regions (Lectures 1–2), while local-authority workplace employment is distorted by commuting.
  - **Estimator:** PPML rather than log-log OLS, because it keeps zero-employment regions (Santos Silva & Tenreyro 2006).
  - **Size measure:** total employment excluding the industry itself.
- **Change made:** Wrote `code/hme_elasticities.py`.
- **Check and result:** Tested the script on synthetic data with known elasticities. It recovered the ordering of the 13 spotlight industries correctly. Levels came out slightly below the true values because the size measure is total employment, not true size. That led to the "measuring size" caveat in `question.md`.
- **Next step:** Run the script on real BRES data, then the population robustness check.

## 2026-11-03 / First run on real data

- **Action and reason:** Downloaded BRES 2024 by TTWA × 4-digit SIC from Nomis. It came as a wide table with Employees and Employment stacked, not the long API format the script expected.
- **Change made:**
  - Added a reader for the wide Nomis table, which uses the Employment block and drops industries with missing cells (only row 0100).
  - Added an option to exclude named regions.
  - Split the rarity correlation into goods and services.
  - Shaded goods and services differently in figure 2.
- **Check and result:**
  - 218 TTWAs and 31.96 million jobs, which is plausible for GB employment. 476 industries pass the 2,000-job threshold.
  - All six tradable services are significantly above 1; local services sit at or below 1. Excluding London leaves the tradable services above 1, and biotech R&D rises.
  - The overall rarity correlation is *positive* (+0.30), the wrong sign for the Dingel prediction. It is driven by small goods industries tied to natural resources. Within services the correlation is −0.08 and not significant.
- **Next step:** Interpret the results in `report.md`. Robustness check with resident population as the size measure.

## Tools / AI assistance

- **Tool and request:** Claude (Anthropic), 2026-11-03. Asked it to suggest Paper 7 questions based on my lecture slides, then to draft the repo templates and an analysis script for the question I chose.
- **Contribution:**
  - Four candidate questions; I chose this one.
  - First drafts of `question.md`, `sources.md`, `analysis.md`, `outputs.md` and this file.
  - The script `code/hme_elasticities.py`, first tested on synthetic data, then extended to read the Nomis table format and run on the real data.
  - A first run of the results, including the London-excluded check.
- **Checks or changes:** [fill in: what you checked, edited or rejected, e.g. confirming the Nomis menu labels and API link, the spotlight SIC codes, the results on real data, and your own interpretation in report.md.]
