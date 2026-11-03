# Sources

## Dataset 1: Business Register and Employment Survey (BRES), open access

- **Provider and URL:** Office for National Statistics, published via Nomis, https://www.nomisweb.co.uk (Query data → Business Register and Employment Survey → open access).
- **Version / dates:** 2024 estimates, downloaded 3 November 2026 from the Nomis web query tool. [Rory to confirm: whether 2024 is shown as provisional or revised on Nomis.]
- **Download steps (as done):**
  1. On Nomis, open *Query data* and choose *Business Register and Employment Survey : open access*.
  2. **Geography:** all Travel to Work Areas (2011) in Great Britain. That gives 218 areas.
  3. **Date:** 2024.
  4. **Industry:** all SIC 2007 4-digit classes. That gives 616 rows, including the special row 0100 for farm agriculture.
  5. **Employment status:** both *Employees* and *Employment*. Nomis puts these in the same file as two stacked tables. **Measure:** *Count*.
  6. Download in Nomis's table CSV format. Save as `data/raw/bres_ttwa_4digit_2024.csv`. This folder is git-ignored, so the file is not committed.
  - The script reads this wide table directly and uses the *Employment* block (employees plus working owners). [Optional: paste the Nomis API link for the query here so the download can be repeated with one click.]
- **Coverage and unit of observation:** Great Britain, 218 TTWAs (2011 definitions). BRES does not cover Northern Ireland. The unit is TTWA × 4-digit SIC class; the table counts jobs at the *workplace*. Total: 31.96 million jobs.
- **Variables and units:** the number of jobs, one column per TTWA (identified by name), plus a flag column after each value.
- **Known issues:**
  - Open-access figures are **rounded**, by an amount that varies by estimate (Nomis article 1103). Industries under 2,000 jobs nationally are dropped, which leaves 476 of 615.
  - Row 0100 (DEFRA/Scottish Executive agricultural data) is missing ("-") for every area, so the script drops it. Two cells carry the "+" flag, meaning incomplete because farm agriculture is suppressed. They are kept.
  - **ONS quality warning** (from the file footnotes): geographical misreporting affects 2015–2024 estimates for Hillingdon and Hounslow, which is the Heathrow area. That sits inside the London TTWA, and possibly Slough and Heathrow. This is one more reason to run the analysis with London excluded.
  - BRES is a sample survey, so every figure carries sampling error.
- **Access / reuse terms:** Open Government Licence v3.0. ONS Crown Copyright.

## Literature (from lectures)

- Krugman, P. (1980). Scale economies, product differentiation, and the pattern of trade. *American Economic Review*, 70(5), 950–959.
- Brakman, S., Garretsen, H. & van Marrewijk, C. (2019). *An Introduction to Geographical and Urban Economics: A Spiky World*, 3rd edn, ch. 7.
- Dingel, J., Gottlieb, J., Lozinski, M. & Mourot, P. (June 2026 draft). Market size and trade in medical services. Earlier version: NBER Working Paper 31030.
- Martin, R. (1999). The new 'geographical turn' in economics: some critical reflections. *Cambridge Journal of Economics*, 23(1), 65–91.
- Santos Silva, J. M. C. & Tenreyro, S. (2006). The log of gravity. *Review of Economics and Statistics*, 88(4), 641–658. This is the case for PPML over log-log OLS.
