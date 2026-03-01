import streamlit as st

st.set_page_config(page_title="Neonatal Bilirubin Calculator", layout="centered")

st.title("Neonatal Bilirubin Calculator (30–38 weeks)")

# ---------------------------------------------------
# RAW CHART DATA (µmol/L)
# Time points available in guideline charts
# ---------------------------------------------------

time_points_96 = [6, 12, 24, 48, 72, 96]
time_points_120 = [6, 12, 24, 48, 72, 96, 120]

# -------------------------
# 30–34 weeks (STANDARD ONLY)
# -------------------------

data_30_34 = {
    30: {"pt":[50,65,95,145,200,200], "et":[100,115,150,220,300,300]},
    31: {"pt":[50,70,100,155,210,210], "et":[100,120,155,230,310,310]},
    32: {"pt":[50,70,100,160,220,220], "et":[100,120,160,240,320,320]},
    33: {"pt":[50,70,100,170,230,230], "et":[100,120,160,250,330,330]},
    34: {"pt":[50,70,110,170,240,240], "et":[100,120,170,250,340,340]},
}

# -------------------------
# 35–38 weeks STANDARD
# -------------------------

data_35_38_standard = {
    35: {"pt":[58,94,130,191,236,267,268],
         "et":[266,290,306,354,391,419,422]},
    36: {"pt":[84,109,140,202,248,279,280],
         "et":[295,309,327,374,412,436,439]},
    37: {"pt":[94,115,149,212,258,291,294],
         "et":[304,320,347,395,431,455,456]},
    38: {"pt":[101,121,159,222,270,303,306],
         "et":[321,336,366,410,443,462,462]},
}

# -------------------------
# 35–38 weeks NEUROTOXICITY
# -------------------------

data_35_38_neuro = {
    35: {"pt":[48,67,101,157,198,224,227],
         "et":[236,250,275,316,344,361,364]},
    36: {"pt":[56,75,109,167,212,239,241],
         "et":[246,260,284,327,357,378,381]},
    37: {"pt":[67,85,120,180,224,255,256],
         "et":[256,268,294,337,371,393,397]},
    38: {"pt":[74,94,128,188,232,259,260],
         "et":[265,279,303,344,378,402,402]},
}

# ---------------------------------------------------
# INTERPOLATION FUNCTION
# ---------------------------------------------------

def interpolate(hour, time_list, value_list):

    if hour <= time_list[0]:
        return value_list[0]

    if hour >= time_list[-1]:
        return value_list[-1]

    for i in range(len(time_list)-1):
        if time_list[i] <= hour <= time_list[i+1]:
            x1 = time_list[i]
            x2 = time_list[i+1]
            y1 = value_list[i]
            y2 = value_list[i+1]

            proportion = (hour - x1) / (x2 - x1)
            return round(y1 + proportion * (y2 - y1), 1)

# ---------------------------------------------------
# USER INPUT
# ---------------------------------------------------

ga = st.selectbox("Gestation (weeks)", [30,31,32,33,34,35,36,37,38])

hour = st.slider("Hour of life", 6, 120, 6)

if ga >= 35:
    neuro = st.checkbox("Neurotoxicity risk present?")
else:
    neuro = False

current_tsb = st.number_input("Current TSB (µmol/L)", min_value=0.0)

# ---------------------------------------------------
# SELECT DATA SOURCE
# ---------------------------------------------------

if ga <= 34:
    dataset = data_30_34[ga]
    times = time_points_96
elif ga >= 35:
    times = time_points_120
    if neuro:
        dataset = data_35_38_neuro[ga]
    else:
        dataset = data_35_38_standard[ga]

# ---------------------------------------------------
# CALCULATE THRESHOLDS
# ---------------------------------------------------

pt = interpolate(hour, times, dataset["pt"])
et = interpolate(hour, times, dataset["et"])
intensive_pt = round(pt + 51, 1)

# ---------------------------------------------------
# RESULTS
# ---------------------------------------------------

st.subheader("Results")

st.write(f"PT Threshold: {pt} µmol/L")
st.write(f"Intensive PT Threshold: {intensive_pt} µmol/L")
st.write(f"ET Threshold: {et} µmol/L")

if current_tsb >= et:
    decision = "Exchange Transfusion"
elif current_tsb >= intensive_pt:
    decision = "Intensive Phototherapy"
elif current_tsb >= pt:
    decision = "Conventional Phototherapy"
else:
    decision = "No Phototherapy"

st.success(f"Decision: {decision}")
