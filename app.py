import streamlit as st
import numpy as np

st.title("Postoperative Bleeding Risk Calculator")

# Sidebar inputs
has_bled = st.sidebar.slider("HAS-BLED Score", 0, 9, 0)
alcohol = st.sidebar.selectbox("High-risk Alcohol Consumption?", ["No", "Yes"])
pai = st.sidebar.selectbox("Platelet Aggregation Inhibitor Therapy?", ["No", "Yes"])
oac = st.sidebar.selectbox("Oral Anticoagulation Therapy?", ["No", "Yes"])
bridging = st.sidebar.selectbox("Perioperative Bridging Therapy?", ["No", "Yes"])

# Convert selections to binary (0 or 1)
alcohol_val = 1 if alcohol == "Yes" else 0
pai_val     = 1 if pai == "Yes" else 0
oac_val     = 1 if oac == "Yes" else 0
bridging_val= 1 if bridging == "Yes" else 0

# Logistic regression coefficients
intercept = -3.7634
b_has_bled = 0.0284
b_alcohol = 0.9575
b_pai = 1.0074
b_oac = 0.5272
b_bridging = 1.0557

# Calculate logit and probability
logit = (intercept +
         b_has_bled * has_bled +
         b_alcohol * alcohol_val +
         b_pai * pai_val +
         b_oac * oac_val +
         b_bridging * bridging_val)
prob = 1 / (1 + np.exp(-logit))

st.subheader("Estimated Probability of Postoperative Bleeding")
st.write(f"{prob:.2%}")
