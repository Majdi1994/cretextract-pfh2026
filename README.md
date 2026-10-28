# CreteXtract control layer: companion repository for the Prototypes for Humanity 2026 short paper

Companion artefacts for:

> Flah, M. and Nehdi, M. L. (2026). *CreteXtract: From Literature to Auditable Chloride-Diffusion Evidence for Low-Carbon Concrete.* Short Papers Platform, Prototypes for Humanity 2026, Dubai, 17-20 November 2026.

Archived at Zenodo: concept DOI [10.5281/zenodo.23749157](https://doi.org/10.5281/zenodo.23749157) (resolves to the latest version); first release v1.0.0, DOI [10.5281/zenodo.23749158](https://doi.org/10.5281/zenodo.23749158). Source: https://github.com/Majdi1994/cretextract-pfh2026

## What CreteXtract is

CreteXtract is a web application (https://cretextract.com) that runs commercially available large language models inside a controlled extraction workflow. The user uploads a set of papers and a column schema, selects a model, and receives a validated dataset, a flag register and a source locator for every populated field.

The application supplies the **control layer** and calls the selected model through its programming interface. The control layer is what makes the output auditable, and it is what this repository publishes, as the exact files used in the evaluated run:

| Control | What it fixes | File |
|---|---|---|
| Method scope | Eligible target: an apparent or effective chloride diffusion coefficient fitted directly to a measured chloride profile (NT BUILD 443, ASTM C1556 or an equivalent bulk-diffusion fit); migration, RCPT, resistivity and model-only coefficients excluded | `prompts/CreteXtract_NT443_12Study_Extraction_Prompt_v1.4.txt` |
| Schema lock | Sixteen columns in a fixed order, with units and missing-value rules | `schema/CreteXtract_Chloride_Da_16_Column_Schema_v1.0.xlsx`, `schema/schema_v1.0.csv` |
| Row-cardinality control | One row per study, mixture, test method, exposure condition, duration, temperature and chloride-profile basis; an observation manifest per source reconciled against the rows returned | extraction prompt, section ROW IDENTITY AND CARDINALITY |
| Source grounding | A locator for every populated field, verified against the PDF text | application; outcome summarised in `validation/rules_v1.md` |
| Read-only validation | Nine executable rules that flag or quarantine a row and never rewrite a value, plus an independent validation agent that matches rows one-to-one against the benchmark | `validation/validation_config.json`, `validation/rules_v1.md`, `prompts/CreteXtract_NT443_12Study_Validation_Prompt_v1.4.txt` |

The model is exchangeable; the controls stay fixed. The short paper evaluates **one configuration** of this workflow, described below.

## Evaluated configuration

| Item | Value |
|---|---|
| Application run | `NT Build 443 - Data - 3rd`, started 2026-08-30 16:35 UTC, status `completed_with_review` |
| Model endpoint | `gemini-3.1-pro-preview` (Google AI for Developers) |
| Schema | `CreteXtract_Chloride_Da_16_Column_Schema_v1.0.xlsx` (16 columns) |
| Extraction prompt | `CreteXtract_NT443_12Study_Extraction_Prompt_v1.4.txt` |
| Validation prompt | `CreteXtract_NT443_12Study_Validation_Prompt_v1.4.txt` |
| Validation rules | `validation_config.json` (9 rules, all enabled) |
| Corpus | 12 PDF studies (`schema/corpus_manifest.csv`) |
| Output | 146 rows; locators resolved for 132 (the 14 rows from the scanned HETEK report have none) |
| Rule outcomes | R_01 flagged 3 rows (Da > 30 x 10^-12 m2/s); R_03 flagged 8 rows (no unique exposure duration in the source); all other rules passed on all rows |
| Benchmark | 120 human-compiled observations at the same observation unit |
| Result, all 12 studies | 118 of 120 benchmark observations found (98.3% recall); 107 of 120 returned within 10% of reference (89.2% end-to-end recovery) |
| Result, 8 studies free of prompt exposure and parsing failure | 91 of 93 found; all within 10% of reference; MAPE 0.058% |

## Disclosures that travel with these files

- **Prompt exposure.** The extraction prompt names expected values or row counts for three corpus studies (Maes: four target coefficients; the temperature study: nine rows, 42 exposure days, Da = 55.3 retained; Elahi: ten Figure 10 observations). The paper's leakage-controlled estimand withholds those three studies and the parsing-failure study. The prompt is published unedited so the run is reproducible as it was made.
- **Validation-prompt controls.** The validation prompt also fixes field conventions for two further groups (Persian Gulf study: 90 chloride-exposure days; Al-Sodani and Dousti: reported exposure temperatures). These controls govern row matching and benchmark adjudication for exposure duration and temperature; they do not name any Da value.
- **Chart reading.** The extraction prompt instructs two-tick axis calibration for figure digitisation. In the evaluated run the ten chart-read rows performed as uncalibrated visual estimates (2 of 10 within 10% of reference), which is why calibrated chart reading outside the model is listed as the next phase.
- **Single run.** All reported numbers come from one run of one model version. Run-to-run variance is not estimated.
- **Excluded study.** A thirteenth study (Szweda et al.) is excluded from the primary corpus by both prompts and from every metric in the paper.

## What is not here

- Application source code (the web application is a separate codebase).
- The twelve study PDFs (publisher copyright). `schema/corpus_manifest.csv` identifies each study and its file name in the run.
- The benchmark and the 146-row run output. They are not part of this release.

## Repository layout

```
schema/
  CreteXtract_Chloride_Da_16_Column_Schema_v1.0.xlsx   the schema file uploaded to the application
  schema_v1.0.csv                                      the same 16 columns with units, matching-key and required flags, and the prompt's field definitions
  corpus_manifest.csv                                  the 12 studies: run file name, identity, rows produced, partition in the paper
prompts/
  CreteXtract_NT443_12Study_Extraction_Prompt_v1.4.txt exact extraction prompt used in the run
  CreteXtract_NT443_12Study_Validation_Prompt_v1.4.txt exact validation prompt used in the run
validation/
  validation_config.json                               the executable rule set as run
  rules_v1.md                                          the rules in readable form, with their outcome on the run
scripts/
  check_output_against_schema.py                       checks any CSV against the locked schema (read-only)
  apply_validation_rules.py                            applies validation_config.json to any CSV and prints per-rule pass counts (read-only)
```

Both scripts reproduce the application's own validation summary when run on the 146-row output (143/146 on R_01, 138/146 on R_03, 146/146 on the rest).

## Using the control layer with another model

1. Upload the PDFs and `schema/CreteXtract_Chloride_Da_16_Column_Schema_v1.0.xlsx` to the application, or supply the schema to your own harness.
2. Use the two prompt files unchanged.
3. Run `scripts/check_output_against_schema.py output.csv` and `scripts/apply_validation_rules.py output.csv` before any value is accepted.

## Citation

See `CITATION.cff`. Please cite the short paper and the archived DOI of this repository.

## Licences

- Prompts, schema files, validation rules and manifests: [CC BY 4.0](LICENSE-DATA)
- Scripts: [MIT](LICENSE)

## Contact

Majdi Flah, Department of Civil Engineering, McMaster University, flahm@mcmaster.ca
Moncef L. Nehdi, College of Engineering, University of Guelph, mnehdi@uoguelph.ca
