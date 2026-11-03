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

## Tools / AI assistance

- **Tool and request:** Claude (Anthropic), 2026-11-03. Asked it to suggest Paper 7 questions based on my lecture slides, then to draft the repo templates and an analysis script for the question I chose.
- **Contribution:**
  - Four candidate questions; I chose this one.
  - First drafts of `question.md`, `sources.md`, `analysis.md`, `outputs.md` and this file.
  - The script `code/hme_elasticities.py`, which was tested on synthetic data only.
- **Checks or changes:** [fill in: what you checked, edited or rejected, e.g. confirming the Nomis menu labels and API link, the spotlight SIC codes, the results on real data, and your own interpretation in report.md.]
