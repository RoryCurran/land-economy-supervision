# Sources

## Dataset 1: Business Register and Employment Survey (BRES), open access

- **Provider and URL:** Office for National Statistics, published via Nomis, https://www.nomisweb.co.uk (Query data → Business Register and Employment Survey → open access).
- **Version / dates:** [fill in: year used, e.g. 2024 revised. A revised year is preferable to a provisional one.] Downloaded [fill in date].
- **Download steps:** [Confirm the menu labels as you go, since Nomis wording may differ slightly.]
  1. On Nomis, open *Query data* and choose *Business Register and Employment Survey : open access*.
  2. **Geography:** Travel to Work Areas (2011), select all.
  3. **Date:** one year only.
  4. **Industry:** SIC 2007 *class (4-digit)*, select all.
  5. **Employment status:** *Employment* (employees plus working owners). Measure: *Count*.
  6. Download as CSV. Copy the **API link** that Nomis offers for the query and paste it here, so the download can be repeated exactly:
     `[paste API URL]`
  7. Save the file as `data/raw/bres_ttwa_4digit.csv`. This folder is git-ignored, so the file is not committed.
- **Coverage and unit of observation:** Great Britain (BRES excludes Northern Ireland, which has its own survey run by NISRA). The unit is a TTWA × 4-digit SIC class; the table counts jobs located in each TTWA.
- **Variables and units:** `OBS_VALUE` is the number of jobs. Also used: `GEOGRAPHY_CODE`, `GEOGRAPHY_NAME`, `INDUSTRY_NAME` (format "6910 : Legal activities").
- **Known issues:**
  - Open-access figures are **rounded**, so small cells are noisy. Industries under 2,000 jobs nationally are dropped for this reason.
  - BRES is a sample survey, so every figure carries sampling error.
  - Jobs are recorded at the *workplace*.
- **Access / reuse terms:** Open Government Licence v3.0.

## Dataset 2 (robustness): resident population by TTWA

- [To add: ONS mid-year population estimates or Census 2021 usual residents. If Nomis does not offer TTWA geography directly, aggregate LSOA figures to TTWAs using the ONS LSOA→TTWA lookup from the Open Geography Portal. Record the lookup file and its version here.]

## Literature (from lectures)

- Krugman, P. (1980). Scale economies, product differentiation, and the pattern of trade. *American Economic Review*, 70(5), 950–959.
- Brakman, S., Garretsen, H. & van Marrewijk, C. (2019). *An Introduction to Geographical and Urban Economics: A Spiky World*, 3rd edn, ch. 7.
- Dingel, J., Gottlieb, J., Lozinski, M. & Mourot, P. (June 2026 draft). Market size and trade in medical services. Earlier version: NBER Working Paper 31030.
- Martin, R. (1999). The new 'geographical turn' in economics: some critical reflections. *Cambridge Journal of Economics*, 23(1), 65–91.
- Santos Silva, J. M. C. & Tenreyro, S. (2006). The log of gravity. *Review of Economics and Statistics*, 88(4), 641–658. This is the case for PPML over log-log OLS.
