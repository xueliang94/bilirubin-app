import streamlit as st

st.set_page_config(page_title="Neonatal Bilirubin Calculator", layout="centered")

st.title("Neonatal Bilirubin Calculator (30–38 weeks)")

# ----------------------------
# DATA SECTION
# ----------------------------

# 30–34 weeks (NO neurotoxicity, up to 96h)
data_30_34 = {
    30: {6: (50,100), 12:(65,115), 24:(95,150), 48:(145,220), 72:(200,300), 96:(200,300)},
    31: {6:(50,100),12:(70,120),24:(100,155),48:(155,230),72:(210,310),96:(210,310)},
    32: {6:(50,100),12:(70,120),24:(100,160),48:(160,240),72:(220,320),96:(220,320)},
    33: {6:(50,100),12:(70,120),24:(100,160),48:(170,245),72:(230,330),96:(230,330)},
    34: {6:(50,100),12:(70,120),24:(110,170),48:(170,250),72:(240,340),96:(240,340)}
}

# 35–38 weeks STANDARD (up to 120h)
data_35_38_standard = {
    35:{6:(48,236),12:(67,250),24:(101,275),48:(157,316),72:(198,344),96:(224,361),120:(227,364)},
    36:{6:(56,246),12:(75,260),24:(109,284),48:(167,327),72:(212,357),96:(239,378),120:(241,381)},
    37:{6:(67,256),12:(85,268),24:(120,294),48:(180,337),72:(224,371),96:(255,393),120:(256,397)},
    38:{6:(74,265),12:(94,279),24:(128,303),48:(188,344),72:(232,378),96:(259,402),120:(260,402)}
}

# 35–38 weeks NEUROTOXICITY
data_35_38_neuro = {
    35:{6:(48,236),12:(67,250),24:(101,275),48:(157,316),72:(198,344),96:(224,361),120:(227,364)},
    36:{6:(56,246),12:(75,260),24:(109,284),48:(167,327),72:(212,357),96:(239,378),120:(241,381)},
    37:{6:(67,256),12:(85,268),24:(120,294),48:(180,337),72:(224,371),96:(255,393),120:(256,397)},
    38:{6:(74,265),12:(94,279),24:(128,303),48:(188,344),72:(232,378),96:(259,402),120:(260,402)}
}

# ----------------------------
# INPUT SECTION
# ----------------------------

ga = st.selectbox("Gestation (weeks)", [30,31,32,33,34,35,36,37,38])

if ga <= 34:
    hour_options = [6,12,24,48,72,96]
else:
    hour_options = [6,12,24,48,72,96,120]

hour = st.selectbox("Hour of life", hour_options)

if ga >= 35:
    neuro = st.checkbox("Neurotoxicity risk present?")
else:
    neuro = False

current_tsb = st.number_input("Current TSB (µmol/L)", min_value=0.0)

# ----------------------------
# CALCULATION SECTION
# ----------------------------

if ga <= 34:
    pt, et = data_30_34[ga][hour]
else:
    if neuro:
        pt, et = data_35_38_neuro[ga][hour]
    else:
        pt, et = data_35_38_standard[ga][hour]

intensive_pt = pt + 51

# ----------------------------
# RESULTS
# ----------------------------

st.subheader("Results")

st.write(f"PT Threshold: {pt} µmol/L")
st.write(f"Intensive PT Threshold: {intensive_pt} µmol/L")
st.write(f"ET Threshold: {et} µmol/L")

# Decision logic
if current_tsb >= et:
    decision = "Exchange Transfusion"
elif current_tsb >= intensive_pt:
    decision = "Intensive Phototherapy"
elif current_tsb >= pt:
    decision = "Conventional Phototherapy"
else:
    decision = "No Phototherapy"

st.success(f"Decision: {decision}")
