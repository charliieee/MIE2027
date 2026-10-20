"""01_prepare_sample.py

Reads the cleaned survey export (dataAfterCleaning.xlsx, n = 363 physicians)
and derives every variable used in the short communication under the names
documented in documentation/codebook.csv. Writes analytical_sample.csv to the
repository root.

Run from the repository root:  python code/01_prepare_sample.py
"""
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "dataAfterCleaning.xlsx"
OUT = ROOT / "analytical_sample.csv"

# ---------------------------------------------------------------------------
# Column positions in the export (0-based) and variable names
# ---------------------------------------------------------------------------
COL_AGE, COL_SEX, COL_SETTING, COL_SPECIALTY = 8, 10, 11, 13
COL_TOOLS = list(range(18, 37))            # 19 digital-tool items, in questionnaire order
COL_AI_ANY, COL_AI_AREAS = 42, 43

TOOL_LABELS = {                            # English short labels used in Figure 1 and S2
    1: "Practice/hospital information system",
    2: "Electronic patient record (ePA)",
    3: "Electronic medication list/plan",
    4: "Electronic sick note (eAU)",
    5: "Image viewing (PACS)",
    6: "Laboratory information system",
    7: "Differential diagnosis / CDSS",
    8: "Prescribable digital health apps (DiGA)",
    9: "Health apps in patient care",
    10: "Telephone assistants (scheduling)",
    11: "Video consultation",
    12: "Tele-rounds (ICU, stroke unit, care home)",
    13: "Tele/home monitoring",
    14: "Speech recognition for documentation",
    15: "Digital pre-registration, emergency care",
    16: "Patient-facing triage tools (ada, docyet)",
    17: "Medication safety alerts (AMTS)",
    18: "Automated duty rostering",
    19: "Knowledge resources (Amboss, Thieme)",
}
CDSS_ITEM = 7

RESPONSE_LABELS = {                        # German response option -> English level
    "täglich": "daily",
    "wöchentlich": "weekly",
    "monatlich": "monthly",
    "seltener": "less_often",
    "möchte ich, aber nicht verfügbar": "would_like",
    "unklar, was das ist": "unclear",
}
AGE_ORD = {                                # six bands, one unit = one decade
    "20-29 Jahre": 0, "30-39 Jahre": 1, "40-49 Jahre": 2,
    "50-59 Jahre": 3, "60-69 Jahre": 4, "70 Jahre oder älter": 5,
}
AGE_GROUP3 = {0: "<40", 1: "<40", 2: "40-59", 3: "40-59", 4: ">=60", 5: ">=60"}


def setting_group(v: str) -> str:
    if v.startswith("Krankenhaus"):
        return "hospital"
    if v.startswith(("Praxis", "MVZ")):
        return "practice"
    return "other"


def specialty_group(v: str) -> str:
    if v == "Allgemeinmedizin":
        return "general_practice"
    if v == "Innere Medizin":
        return "internal_medicine"
    return "other"


def main() -> None:
    raw = pd.read_excel(SRC)
    cols = list(raw.columns)
    assert len(raw) == 363, f"expected 363 physicians, found {len(raw)}"
    assert (raw[cols[12]] == "Ärzt:in").all(), "non-physicians in export"
    assert cols[COL_TOOLS[CDSS_ITEM - 1]].startswith("Differentialdiagnostik"), "CDSS item not at expected position"

    d = pd.DataFrame({"id": raw[cols[0]]})

    # demographics
    d["age_band"] = raw[cols[COL_AGE]]
    d["age_ord"] = d["age_band"].map(AGE_ORD)
    d["age_group3"] = d["age_ord"].map(AGE_GROUP3)
    d["sex"] = raw[cols[COL_SEX]].map({"weiblich": "female", "männlich": "male"})
    d["setting_raw"] = raw[cols[COL_SETTING]]
    d["setting"] = d["setting_raw"].astype(str).map(setting_group)
    d["specialty_raw"] = raw[cols[COL_SPECIALTY]]
    d["specialty_group"] = d["specialty_raw"].astype(str).map(specialty_group)
    assert d["age_ord"].notna().all() and d["sex"].notna().all()

    # 19 digital-tool items, six levels
    for k, col in enumerate(COL_TOOLS, start=1):
        v = raw[cols[col]]
        unknown = set(v.dropna()) - set(RESPONSE_LABELS)
        assert not unknown, f"tool {k}: unexpected responses {unknown}"
        d[f"tool_{k:02d}"] = v.map(RESPONSE_LABELS)

    # AI use
    d["ai_use_any"] = raw[cols[COL_AI_ANY]].astype(str).str.startswith("Ja").astype(int)
    areas = raw[cols[COL_AI_AREAS]].fillna("")
    d["ai_use_diagnostics"] = areas.str.contains("Diagnostik und Befund").astype(int)

    d.to_csv(OUT, index=False)

    # checks against the manuscript
    cdss = d[f"tool_{CDSS_ITEM:02d}"]
    assert cdss.notna().sum() == 361
    assert d["ai_use_diagnostics"].sum() == 81
    print(f"analytical sample written: {OUT.name}  n = {len(d)}  CDSS item n = {cdss.notna().sum()}")
    print(f"AI use for diagnostic tasks: {d['ai_use_diagnostics'].sum()} ({d['ai_use_diagnostics'].mean()*100:.0f}%)")


if __name__ == "__main__":
    main()
