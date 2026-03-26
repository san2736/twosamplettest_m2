import streamlit as st
import numpy as np
from statistics import stdev
from scipy.stats import t

# Your function (kept same)
def san(a, b, alt):
    alpha = 0.05
    n1 = len(a)
    n2 = len(b)
    x1 = np.mean(a)
    x2 = np.mean(b)
    sd1 = stdev(a)
    sd2 = stdev(b)
    df = n1 + n2 - 2
    mu = 0
    se = np.sqrt((sd1**2 / n1) + (sd2**2 / n2))
    tcal = ((x1 - x2) - 0) / se

    result = {}
    result["t_calculated"] = tcal

    if alt == "two-sided":
        alpha = alpha / 2
        t_pos = t.ppf(1 - alpha, df)
        t_neg = t.ppf(alpha, df)
        p_val = (1 - t.cdf(tcal, df)) * 2

        result["t_critical_positive"] = t_pos
        result["t_critical_negative"] = t_neg
        result["p_value"] = p_val

    elif alt == "greater":
        t_pos = t.ppf(1 - alpha, df)
        p_val = (1 - t.cdf(tcal, df))

        result["t_critical_positive"] = t_pos
        result["p_value"] = p_val

    elif alt == "less":
        t_neg = t.ppf(alpha, df)
        p_val = t.cdf(tcal, df)

        result["t_critical_negative"] = t_neg
        result["p_value"] = p_val

    return result


# Streamlit UI
st.title("Two Sample t-Test Calculator")

st.write("Enter values separated by commas")

a_input = st.text_area("Sample A", "56,128.6,12,123.8,64.34,78,763.3")
b_input = st.text_area("Sample B", "1.1,2.9,4.2")

alt = st.selectbox("Alternative Hypothesis", ["two-sided", "greater", "less"])

if st.button("Calculate"):
    try:
        a = np.array([float(i.strip()) for i in a_input.split(",")])
        b = np.array([float(i.strip()) for i in b_input.split(",")])

        result = san(a, b, alt)

        st.subheader("Results")
        for key, value in result.items():
            st.write(f"{key}: {value}")

    except:
        st.error("Please enter valid numeric inputs.")
