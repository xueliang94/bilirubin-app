import streamlit as st
import numpy as np

st.title("Neonatal Bilirubin Calculator (30–38 weeks)")

# --------------------------
# DATA
# --------------------------

hours_preterm = np.array([6,12,24,48,72,96])
hours_term = np.array([6,12,24,48,72,96,120])

preterm_data = {
    30: {"PT":[50,65,95,145,200,200],"ET":[100,115,150,220,290,290]},
    31: {"PT":[50,70,100,155,210,210],"ET":[100,120,155,230,310,310]},
    32: {"PT":[50,70,100,160,220,220],"ET":[100,120,160,240,320,320]},
    33: {"PT":[50,70,100,170,230,230],"ET":[100,120,160,245,330,330]},
    34: {"PT":[50,70,110,170,240,240],"ET":[100,120,170,250,340,340]},
}

term_data = {
    35: {"PT":[58,94,130,191,236,267,268],"ET":[266,280,306,354,391,419,422]},
    36: {"PT":[84,103,140,202,248,279,280],"ET":[285,299,327,374,412,436,439]},
    37: {"PT":[94,113,149,212,258,291,294],"ET":[304,320,347,395,431,455,456]},
    38: {"PT":[101,121,159,222,270,303,306],"ET":[321,337,366,410,443,462,462]},
}

# --------------------------
# INPUT
# --------------------------

ga = st.selectbox("Gestation (weeks)", [30,31,32,33,34,35,36,37,38], key="ga")
hour = st.number_input("Hour of life", 6, 120, key="hour")
tsb = st.number_input("Current TSB (µmol/L)", key="tsb")
prev = st.number_input("Previous TSB (µmol/L)", key="prev")
delta = st.number_input("Hours between samples", key="delta")

# --------------------------
# CALCULATION
# --------------------------

if ga <= 34:
    hour_use = min(hour, 96)
    pt = np.interp(hour_use, hours_preterm, preterm_data[ga]["PT"])
    et = np.interp(hour_use, hours_preterm, preterm_data[ga]["ET"])
else:
    pt = np.interp(hour, hours_term, term_data[ga]["PT"])
    et = np.interp(hour, hours_term, term_data[ga]["ET"])

intensive = pt + 51

if tsb >= et:
    decision = "EXCHANGE TRANSFUSION"
elif tsb >= intensive:
    decision = "INTENSIVE PHOTOTHERAPY"
elif tsb >= pt:
    decision = "CONVENTIONAL PHOTOTHERAPY"
else:
    decision = "OBSERVE"

if delta > 0:
    rate = (tsb - prev) / delta
else:
    rate = 0

# --------------------------
# OUTPUT
# --------------------------

st.subheader("Results")

st.write("PT Threshold:", round(pt,1))
st.write("Intensive PT Threshold:", round(intensive,1))
st.write("ET Threshold:", round(et,1))
st.write("Decision:", decision)

if delta > 0:
    st.write("Rate of Rise:", round(rate,2), "µmol/L/hr")
    if rate > 8.5:
        st.warning("⚠ High Risk: Rate > 8.5 µmol/L/hr")
