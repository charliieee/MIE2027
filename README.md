**Used but Not Recognised - Digital Support for Differential Diagnosis in Germany**

AUTHORS\
    Sophie-Charlotte Perret, University of Cambridge (0009-0009-0044-4633)\
    Jonah Siebert, University of Applied Sciences Offenburg (0009-0001-7136-1175)\
    Jan Baumann, Hartmannbund, Association of Doctors in Germany (0000-0003-3679-7341)\
    Markus Schinle, University of Applied Sciences Offenburg (0000-0002-3132-0280)

VERSION\
    1.1\
    Last updated: 20 October 2026

STATUS\
    This repository belongs to the submitted version of the short communication for the 
    the Medical Informatics Europe (MIE) 2027. 
    
--------------------------------------------------------------------------------
1. OVERVIEW OF THE STUDY
--------------------------------------------------------------------------------

This repository documents the data preparation and analysis reported in the accompanying short communication, a secondary analysis of one item of a cross-sectional survey of 363 physicians in Germany conducted between December 2025 and March 2026. Respondents rated 19 digital tools on a six-point frequency scale (daily, weekly, monthly, less often, "would like to, but not available", "unclear what this is"). The paper reports the item "Differentialdiagnostik bzw. Clinical-Decision-Support (CDSS)" against the 18 other tools, its association with age, and its relation to self-reported AI use for diagnostic tasks.

The repository provides the materials referenced in the manuscript as "Supplements", the analysis code, and the aggregated tables behind Figure 1 and Supplements S2 and S3.

Individual-level microdata are NOT contained in this repository for privacy reasons. See Section 6, Data availability.

--------------------------------------------------------------------------------
2. REPOSITORY STRUCTURE
--------------------------------------------------------------------------------

    mie2027/
|
|-- README.md                          this file
|-- LICENSE.txt                        licence for code and materials
|-- CITATION.cff                       how to cite the paper and this repository
|
|-- supplement/
|     supplement.pdf                   S1 ethics approvals, S2 all 19 tools,
|                                      S3 AI use for diagnostics by CDSS item
|
|-- instrument/
|     questionnaire_de.pdf             full questionnaire, German original
|     questionnaire_en.pdf             full questionnaire, English translation
|
|-- documentation/
|     sample_derivation.pdf            raw export (n = 403) to analytical sample (n = 363)
|     codebook.csv                     variables used in this paper: names, coding, labels
|
|-- data/
|     aggregated/
|        s2_tool_frequencies.csv       19 tools x 6 response categories, counts
|        cdss_by_age.csv               CDSS item by age band
|        s3_ai_use_by_cdss.csv         AI use for diagnostics x CDSS item, overall and by age group
|        regression_age.csv            OR per decade for "unclear", CDSS and the 18 other tools
|
|-- code/
|     requirements.txt                 pinned dependency versions
|     01_prepare_sample.py
|     02_tool_frequencies.py
|     03_age_models.py
|     04_ai_crosstab.py
|
|-- results/
      figure1.pdf
      figure1.png

--------------------------------------------------------------------------------
3. CONTENT DESCRIPTION
--------------------------------------------------------------------------------
    **supplement/supplement.pdf**
    The supplementary material referenced in the manuscript. S1: ethics
    approvals. S2: distribution of all six response categories for all 19
    digital tools. S3: cross-tabulation of AI use for diagnostic tasks against
    the four collapsed categories of the CDSS item, overall and by age group,
    with odds ratios for "unclear what this is".

**instrument/**
    The complete questionnaire as administered, in German, and the English
    translation prepared by the authors. The questionnaire was newly developed
    for this study and was not psychometrically validated. No back-translation
    was conducted. The item analysed is the seventh of the 19-item digital-tool
    battery; AI use for diagnostic tasks is taken from the multiple-response
    item on areas of AI use ("Diagnostik und Befund").

**documentation/sample_derivation.pdf**
    Flow of respondents from the raw export (n = 403) to the analytical sample
    (n = 363): exclusion of non-physicians, retired participants, Austrian and
    Swiss respondents, and records incomplete on key demographic variables.
    Two respondents left the CDSS item blank, giving n = 361 for that item.

**documentation/codebook.csv**
    Variable definitions and coding for every item used in this paper: the 19
    tool items with their German response options and English labels, the
    collapsing rule (daily and weekly; monthly and less often; "would like to,
    but not available"; "unclear what this is"), the six age bands and their
    coding per decade, sex, healthcare setting, specialty, and the AI-use
    indicator. The variable names in the codebook are the names used in the
    scripts.

**data/aggregated/**
    The aggregated tables documenting the published values. s2_tool_frequencies.csv
    underlies Figure 1 and Supplement S2; cdss_by_age.csv the age percentages in
    the Results; s3_ai_use_by_cdss.csv Supplement S3; regression_age.csv the
    odds ratio per decade reported in the Results and the corresponding
    estimates for the 18 other tools. Files are written by the scripts of the
    same number.

**code/**
    Python scripts reproducing the analysis from the cleaned export
    dataAfterCleaning.xlsx (n = 363). Run order follows the file numbering;
    each script asserts its output against the figures printed in the
    manuscript and stops if they differ.

    01_prepare_sample.py        Reads the cleaned export, derives every
                                variable used in the paper under the names in
                                documentation/codebook.csv, and writes
                                analytical_sample.csv.
    02_tool_frequencies.py      Response distribution for all 19 tools,
                                the median share of "unclear what this is"
                                across the 18 comparison tools, Figure 1.
                                Writes s2_tool_frequencies.csv and
                                results/figure1.*.
    03_age_models.py            CDSS item by age band; logistic regression of
                                "unclear what this is" on age per decade,
                                unadjusted and adjusted; the same model for each
                                of the 18 other tools. Writes cdss_by_age.csv
                                and regression_age.csv.
    04_ai_crosstab.py           AI use for diagnostic tasks against the CDSS
                                item, overall and by age group, with chi-square
                                test and age-adjusted odds ratio. Writes
                                s3_ai_use_by_cdss.csv.

**results/**
    Figure 1 of the paper as PDF and PNG.

--------------------------------------------------------------------------------
4. SOFTWARE ENVIRONMENT
--------------------------------------------------------------------------------

    Language:   Python 3.12
    Libraries:  pandas, scipy (scipy.stats), statsmodels, matplotlib, openpyxl

    Exact versions are pinned in code/requirements.txt. To create a matching
    environment:

        python3.12 -m venv venv
        source venv/bin/activate
        pip install -r code/requirements.txt

--------------------------------------------------------------------------------
5. REPRODUCING THE ANALYSIS
--------------------------------------------------------------------------------

    With dataAfterCleaning.xlsx placed in the repository root, scripts 01 to 04
    reproduce every figure, table and statistic in the manuscript and the
    supplement when run in order from the repository root:

        python code/01_prepare_sample.py
        python code/02_tool_frequencies.py
        python code/03_age_models.py
        python code/04_ai_crosstab.py

    The intermediate file analytical_sample.csv is written to the repository
    root and is not deposited.

    dataAfterCleaning.xlsx is not deposited (see Section 6). Without it, the
    aggregated tables in data/aggregated/ document the published values, but
    the scripts cannot be executed.

--------------------------------------------------------------------------------
6. DATA AVAILABILITY
--------------------------------------------------------------------------------

    Individual-level microdata are not shared publicly. They are available from
    the corresponding authors on reasonable request, under a data-use agreement
    consistent with the ethics approvals governing the study.

    This repository contains aggregated data sufficient to reproduce Figure 1
    and Supplements S2 and S3. It does not contain data sufficient to re-run the
    participant-level regressions; those require the microdata above.

--------------------------------------------------------------------------------
7. ETHICS
--------------------------------------------------------------------------------

    The study received favourable ethics opinions from the University of
    Cambridge (Ref. 736, 15 May 2025) and Offenburg University of Applied
    Sciences (Ref. 04-25, 27 June 2025). Data collection was conducted in
    compliance with the General Data Protection Regulation (GDPR). A privacy
    notice and participant information sheet preceded the questionnaire;
    participation was conditional on informed consent. The approvals are
    reproduced in Supplement S1.

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

