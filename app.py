import streamlit as st

st.set_page_config(page_title="Neonatal Bilirubin Calculator", layout="centered")

st.title("Neonatal Bilirubin Calculator (35–38 weeks)")

# --------------------------------------------------
# Official Time Points (hours)
# --------------------------------------------------

time_points = [6, 12, 24, 48, 72, 96, 120]

# --------------------------------------------------
# EXACT µmol VALUES — NO NEUROTOXICITY
# --------------------------------------------------

standard_data = {

    35: {
        "pt": [58, 94, 130, 191, 236, 267, 268],
        "et": [266, 290, 306, 354, 391, 419, 422],
    },

    36: {
        "pt": [84, 109, 140, 202, 248, 279, 280],
        "et": [295, 309, 327, 374, 412, 436, 439],
    },

    37: {
        "pt": [94, 113, 149, 212, 258, 291, 294],
        "et": [304, 320, 347, 395, 431, 455, 456],
    },

    38: {
        "pt": [101, 121, 159, 222, 270, 303, 306],
        "et": [321, 336, 366, 410, 443, 462, 462],
    },
}

# --------------------------------------------------
# EXACT µmol VALUES — WITH NEUROTOXICITY
# --------------------------------------------------

neuro_data = {

    35: {
        "pt": [48, 67, 101, 157, 198, 224, 227],
        "et": [236, 250, 275, 316, 344, 361, 364],
    },

    36: {
        "pt": [56, 75, 109, 167, 212, 239, 241],
        "et": [246, 260, 284, 327, 357, 378, 381],
    },

    37: {
        "pt": [67, 85, 120, 180, 224, 255, 256],
        "et": [256, 268, 294, 337, 371, 393, 397],
    },

    38: {
        "pt": [74, 94, 128, 188, 232, 259, 260],
        "et": [265, 279, 303, 344, 378, 402, 402],
    },
}

# --------------------------------------------------
# INTERPOLATION FUNCTION
# --------------------------------------------------

def interpolate(hour, times, values):

    if hour <= times[0]:
        return values[0]

    if hour >= times[-1]:
        return values[-1]

    for i in range(len(times) - 1):
        if times[i] <= hour <= times[i + 1]:
            x1 = times[i]
            x2 = times[i + 1]
            y1 = values[i]
            y2 = values[i + 1]

            proportion = (hour - x1) / (x2 - x1)
            return y1 + proportion * (y2 - y1)


# --------------------------------------------------
# USER INPUT
# --------------------------------------------------

ga = st.selectbox("Gestation (weeks)", [35, 36, 37, 38])

neuro = st.checkbox("Neurotoxicity risk present?")

hour = st.number_input(
    "Hour of life (6–120)",
    min_value=6,
    max_value=120,
    value=6,
    step=1
)

current_tsb = st.number_input("Current TSB (µmol/L)", min_value=0.0)

previous_tsb = st.number_input("Previous TSB (µmol/L)", min_value=0.0)

hours_between = st.number_input("Hours between samples", min_value=0.0)

# --------------------------------------------------
# SELECT DATASET
# --------------------------------------------------

dataset = neuro_data[ga] if neuro else standard_data[ga]

pt = interpolate(hour, time_points, dataset["pt"])
et = interpolate(hour, time_points, dataset["et"])

intensive_pt = pt + 51   # 3 mg/dL = 51 µmol/L (as guideline)

# --------------------------------------------------
# DECISION LOGIC
# --------------------------------------------------

if current_tsb >= et:
    decision = "Exchange Transfusion"

elif current_tsb >= intensive_pt:
    decision = "Intensive Phototherapy"

elif current_tsb >= pt:
    decision = "Conventional Phototherapy"

else:
    decision = "No Phototherapy"

# --------------------------------------------------
# RATE OF RISE
# --------------------------------------------------

if hours_between > 0:
    rate = (current_tsb - previous_tsb) / hours_between
else:
    rate = 0

if rate > 8.5:
    rate_alert = "HIGH RISK (Rapid rise >8.5 µmol/L/hr)"
else:
    rate_alert = "Normal rate"

# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

st.subheader("Results")

st.write(f"PT Threshold: {pt:.1f} µmol/L")
st.write(f"Intensive PT Threshold: {intensive_pt:.1f} µmol/L")
st.write(f"ET Threshold: {et:.1f} µmol/L")

st.success(f"Decision: {decision}")

st.subheader("Rate of Rise")

st.write(f"Rate: {rate:.2f} µmol/L/hr")
st.write(f"Rate Alert: {rate_alert}")
