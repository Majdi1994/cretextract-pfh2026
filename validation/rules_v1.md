# Executable validation rules, as run (CreteXtract Chloride Da Validation)

Source file: `validation_config.json` (verbatim copy of the rule set applied by the application on 30 August 2026). The application evaluates each rule as a pandas expression over the extracted table. Validation is read-only: a failing rule records a flag against the row; no value is edited, deleted or imputed.

| Rule | Name | Column | Condition (pandas) | Severity | Outcome on the 146-row run |
|---|---|---|---|---|---|
| R_01 | Da valid range warning | Da | `Da <= 30` | warning | 143 / 146 passed; **3 rows flagged** (Da = 55.3, 38.3, 32.7). Rows retained, `Analysis_Eligible = No`. |
| R_02 | Da positivity | Da | `Da > 0` | error | 146 / 146 |
| R_03 | Exposure duration requirement | Exposure_Duration | `Exposure_Duration > 0` | error | 138 / 146 passed; **8 rows flagged**, all from one study where the source did not establish a unique chloride-contact duration. Retained as missing. |
| R_04 | Valid w/b ratio | w_b_ratio | `0.1 <= w_b_ratio <= 1.0` | warning | 146 / 146 |
| R_05 | Optional compressive strength | CS | `CS is null or CS > 0` | error | 146 / 146 |
| R_06 | Test method presence | Test_Method | non-empty | error | 146 / 146 |
| R_07 | Cement quantity required | Cement | `Cement > 0` | error | 146 / 146 |
| R_08 | Exposure temperature validity | Exposure_Temperature | `null or -30 <= T <= 100` | error | 146 / 146 |
| R_09 | Reference presence | Reference | non-empty | error | 146 / 146 |

The two flagged groups are the "three out-of-range values" and the "eight duration fields retained as missing" reported in the short paper.

## Controls applied upstream of these rules

Three further controls act before the rule set and are specified in the prompts rather than in `validation_config.json`:

- **Method scope and coefficient selection hierarchy** (extraction prompt, sections ELIGIBLE TARGET and COEFFICIENT SELECTION HIERARCHY).
- **Row identity and cardinality** (extraction prompt, section ROW IDENTITY AND CARDINALITY): the application builds an observation manifest per source and compares it with the rows returned. On this run the manifest held 170 raw observations across the 12 sources; one source (the scanned HETEK report) was flagged `cardinality_incomplete` and the run closed with status `completed_with_review`.
- **Source grounding**: each populated field is linked to an evidence locator that is verified against the PDF text. On this run, locators resolved for 132 of the 146 rows; the 14 rows from the scanned report have no resolvable locator.

## Reproducing the rule outcomes

`scripts/apply_validation_rules.py <output.csv>` applies `validation_config.json` to any CSV with the locked columns and prints the per-rule pass counts in the same form as the application's `validation_summary.txt`.
