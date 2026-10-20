# MIE2027 - Used but Not Recognised: Digital Support for Differential Diagnosis in Germany

AUTHORS\
    Sophie-Charlotte Perret, University of Cambridge (0009-0009-0044-4633)\
    Jonah Siebert, University of Applied Sciences Offenburg (0009-0001-7136-1175)\
    Jan Baumann, Hartmannbund, Association of Doctors in Germany (0000-0003-3679-7341)\
    Markus Schinle, University of Applied Sciences Offenburg (0000-0002-3132-0280)

VERSION\
    1.1\
    Last updated: 20 October 2026 (before 20 October 2026 11:59pm UTC+2)

STATUS\
    This repository belongs to the submitted version of the short communication for the 
    the Medical Informatics Europe (MIE) 2027. 
    
--------------------------------------------------------------------------------
1. OVERVIEW OF THE STUDY
--------------------------------------------------------------------------------

This repository documents the data preparation, measurement, and statistical
analysis reported in the accompanying manuscript, a cross-sectional survey of
320 physicians in the German healthcare system conducted between December 2025
and March 2026. It provides the materials referenced in the manuscript as
"Supplements", the analysis code, and the aggregated tables required to
regenerate every published figure and table.

Individual-level microdata are NOT contained in this repository for privacy
reasons. See Section 6, Data availability.

--------------------------------------------------------------------------------
2. REPOSITORY STRUCTURE
--------------------------------------------------------------------------------

     mie2027/
    |
    |-- README.md                          this file
    |-- LICENSE.txt                        licence for code and materials
    |-- CITATION.cff                       how to cite the paper and this repository
    |
    |-- instrument/
    |     questionnaire_de.pdf             full questionnaire, German original
    |     questionnaire_en.pdf             full questionnaire, English translation
    |
    |-- documentation/
    |     strobe_flow_diagram.pdf          sample derivation, 403 to 320
    |     cleaning_and_aggregation_rules.pdf
    |     codebook.csv                     variable names, coding, value labels
    |     nonresponse_bias_analysis.pdf    early versus late respondents
    |
    |-- data/
    |     README_data.txt                  file descriptions and microdata access conditions
    |     aggregated/
    |        table1_sample_characteristics.csv
    |        table2_governance_index_by_setting.csv
    |        table3_regression_main.csv
    |        federal_state_distribution.csv
    |        application_areas.csv
    |
    |-- code/
    |     requirements.txt                 pinned dependency versions
    |     01_data_cleaning.py
    |     02_sample_descriptives.py
    |     03_governance_index.py
    |     04_regression_main.py
    |
    |-- results/

--------------------------------------------------------------------------------
3. CONTENT DESCRIPTION
--------------------------------------------------------------------------------

**instrument/**
    The complete questionnaire as administered, in German, and the English
    translation prepared by the authors. The questionnaire was newly developed
    for this study and was not psychometrically validated. No back-translation
    was conducted. The core Shadow AI item is question 32.

**documentation/strobe_flow_diagram.pdf**
    Flow of respondents from the raw dataset (n = 403) to the final analytical
    sample (n = 320). Stages: exclusion of non-physicians, retired participants,
    Austrian and Swiss respondents, and records incomplete on key demographic
    variables (yielding n = 363); exclusion of respondents who selected "No
    answer" on the core Shadow AI item (n = 28, yielding n = 335); exclusion of
    heterogeneous low-frequency work settings (n = 15, yielding n = 320). One
    pilot participant who received the live link before the dispatch is
    retained in the sample.

**documentation/cleaning_and_aggregation_rules.pdf**
    The full set of inclusion and exclusion criteria applied at each stage, and
    the rules by which response categories were aggregated (inpatient and
    outpatient hospital settings combined into "Hospital"; single and group
    practices combined into "Practice").

**documentation/codebook.csv**
    Variable definitions and coding for every item used in the analysis, with
    the column position of each item in the export, the German response
    options and their English labels, and frequencies on the analytical
    sample. It records the ordinal coding of the six age bands (20 to 29 years
    coded 0); the reference category for healthcare setting (ambulatory
    practice); the two dependent variables (own unauthorised AI use, the
    primary outcome: 1 = own use, 0 = otherwise; Shadow AI exposure, the
    secondary outcome: 1 = own use or observation of a colleague, 0 = no case
    known); and the governance-index coding rule, under which responses of
    "do not know" or "cannot say" on a component item are coded as the
    measure not being in place. The variable names in the codebook are the
    names used in the scripts.

**documentation/governance_index_construction.pdf**
    Construction of the composite governance index (0 to 3), its adaptation from
    the general governance dimensions of Klotz et al. (2019), and the stated
    omission of the monitoring and identification dimension as non-observable
    through physician self-report.

**documentation/nonresponse_bias_analysis.pdf**
    Comparison of early respondents (within 48 hours of the initial dispatch on
    17 December 2025, n = 126) and late respondents (on or after the reminder on
    27 January 2026, n = 145) on gender, age band, healthcare setting and the
    Shadow AI item, with chi-square tests of independence and Cramér's V.

**data/aggregated/**
    The aggregated tables documenting the published descriptives, governance
    distributions and regression results. table2_governance_index_by_setting.csv
    and table3_regression_main.csv are written by scripts 03 and 04;
    table3_regression_main.csv contains both models of Table 3. The reference
    statistics of the German Medical Association used for the goodness-of-fit
    tests and the age standardisation are published at
    https://www.bundesaerztekammer.de/fileadmin/user_upload/BAEK/Ueber_uns/Statistik/AErztestatistik_2025.pdf
    (last checked 4 September 2026); the shares used are stated in
    02_sample_descriptives.py and in federal_state_distribution.csv.

**code/**
    Python scripts reproducing each analysis stage from the cleaned export
    dataClassified_2.csv (n = 335, semicolon separated, cp1252). Run order
    follows the file numbering; each script asserts its output against the
    figures printed in the manuscript and stops if they differ.

    01_data_cleaning.py         Builds the analytical sample (n = 320) and
                                derives every variable used in the manuscript
                                under the names in documentation/codebook.csv.
                                Writes analytical_sample.csv.
    02_sample_descriptives.py   Table 1; goodness-of-fit tests of Section 4.1
                                (gender, age, federal state); AI use,
                                application areas, Shadow AI item, by-setting
                                rates shown in Figure 1 and the age-standardised
                                rates of Section 4.2; governance components and
                                training mode of Section 4.3.
    03_governance_index.py      Composite governance index (0 to 3) and Table 2
                                including the three component columns. Writes
                                table2_governance_index_by_setting.csv.
    04_regression_main.py       Table 3, both models: own use (primary,
                                Specification S14 of the sensitivity report)
                                and exposure (secondary, S13), with variance
                                inflation factors. Writes
                                table3_regression_main.csv.
    05_regression_sensitivity.py
                                The sixteen specifications of the sensitivity
                                report (age ordinal or categorical, setting
                                bundled or separate, governance as components
                                or index, both outcomes) and two additional
                                specifications in which "do not know" on tool
                                provision and guidelines is treated as missing.
                                Writes sensitivity_specifications.csv.
    06_nonresponse_bias.py      Early versus late respondent comparison,
                                reproducing documentation/nonresponse_bias_analysis.pdf.
    07_sensitivity_report.py    Builds results/sensitivity_analysis_report.pdf
                                from the outputs of scripts 04 and 05.

    Age enters the models as a single ordinal predictor with the youngest band
    coded 0, as recorded in the codebook; the odds ratio refers to a one
    category increase.

**results/**
    The sensitivity analysis report: coding conventions, an overview of all
    eighteen specifications with fit statistics, full coefficient tables
    (coefficients, standard errors, z values, p values, odds ratios and 95 per
    cent confidence intervals), and variance inflation factors for the Table 3
    predictor set (maximum 1.32). Specifications S14 and S13 correspond to
    Table 3 of the paper. The two figures of the paper are provided as PNG.

--------------------------------------------------------------------------------
4. SOFTWARE ENVIRONMENT
--------------------------------------------------------------------------------

    Language:   Python 3.12.13
    Libraries:  pandas, scipy (scipy.stats), statsmodels, matplotlib
    Original execution environment: Google Colab

    Exact versions are pinned in code/requirements.txt. To create a matching
    environment:

        python3.12 -m venv venv
        source venv/bin/activate
        pip install -r code/requirements.txt

--------------------------------------------------------------------------------
5. REPRODUCING THE ANALYSIS
--------------------------------------------------------------------------------
 
    With dataClassified_2.csv placed in the repository root, scripts 01 to
    07 reproduce every table and statistic in the manuscript and the
    sensitivity report when run in order from the repository root:

        python code/01_data_cleaning.py
        python code/02_sample_descriptives.py
        ...
        python code/07_sensitivity_report.py

    Intermediate files (analytical_sample.csv, sensitivity_specifications.csv)
    are written to the repository root and are not deposited.

    The file is not deposited (see Section 6). Without it, the aggregated
    tables in data/aggregated/ document the published values but the scripts
    cannot be executed.

--------------------------------------------------------------------------------
6. DATA AVAILABILITY
--------------------------------------------------------------------------------

    Individual-level microdata are not shared publicly. They are available from
    the corresponding authors on reasonable request, under a data-use agreement
    consistent with the ethics approvals governing the study.

    This repository contains aggregated data sufficient to reproduce every
    published figure and table. It does not contain data sufficient to re-run
    the participant-level regressions; those require the microdata above.

--------------------------------------------------------------------------------
7. ETHICS
--------------------------------------------------------------------------------

    The study received favourable ethics opinions from the University of
    Cambridge (Ref. 736, 15 May 2025) and Offenburg University of Applied
    Sciences (Ref. 04-25, 27 June 2025). Data collection was conducted in
    compliance with the General Data Protection Regulation (GDPR). A privacy
    notice and participant information sheet preceded the questionnaire;
    participation was conditional on informed consent.

--------------------------------------------------------------------------------
8. LICENCE
--------------------------------------------------------------------------------

    Code (code/) is released under the MIT License. Documentation, the
    questionnaire, aggregated data and results are released under the Creative
    Commons Attribution 4.0 International licence (CC BY 4.0). See LICENSE.txt.

--------------------------------------------------------------------------------
9. CITATION
--------------------------------------------------------------------------------

    See CITATION.cff. Paper:
    to be updated
--------------------------------------------------------------------------------
10. CONTACT
--------------------------------------------------------------------------------

    Corresponding Authors:
    Sophie Perret, University of Cambridge, scp64@cam.ac.uk 
    Jonah Siebert, University of Applied Sciences Offenburg, jonah.siebert@hs-offenburg.de 

    Co-Authors: 
    Jan Baumann, Hartmannbund, jan.baumann@purposehealth.de 
    Markus Schinle, University of Applied Sciences Offenburg, markus.schinle@hs-offenburg.de 
================================================================================

