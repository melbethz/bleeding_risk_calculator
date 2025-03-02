import streamlit as st
import numpy as np
import altair as alt
import pandas as pd

########################
# 1) Title & User Inputs
########################
st.title("Postoperative Bleeding Risk Calculator")

# Sidebar inputs
has_bled = st.sidebar.slider("HAS-BLED Score", 0, 9, 0)
alcohol = st.sidebar.selectbox("High-risk Alcohol Consumption?", ["No", "Yes"])
pai = st.sidebar.selectbox("Platelet Aggregation Inhibitor Therapy?", ["No", "Yes"])
oac = st.sidebar.selectbox("Oral Anticoagulation Therapy?", ["No", "Yes"])
bridging = st.sidebar.selectbox("Perioperative Bridging Therapy?", ["No", "Yes"])

# Convert selections to binary
alcohol_val = 1 if alcohol == "Yes" else 0
pai_val     = 1 if pai == "Yes" else 0
oac_val     = 1 if oac == "Yes" else 0
bridging_val= 1 if bridging == "Yes" else 0

########################
# 2) Logistic Model
########################
# Coefficients from your final logistic regression model
intercept = -3.7634
b_has_bled = 0.0284
b_alcohol = 0.9575
b_pai = 1.0074
b_oac = 0.5272
b_bridging = 1.0557

# Calculate the linear predictor (logit)
user_logit = (
    intercept +
    b_has_bled * has_bled +
    b_alcohol  * alcohol_val +
    b_pai      * pai_val +
    b_oac      * oac_val +
    b_bridging * bridging_val
)

# Convert logit to probability
prob = 1 / (1 + np.exp(-user_logit))

########################
# 3) Display Probability
########################
st.subheader("Estimated Probability of Postoperative Bleeding")
st.write(f"**{prob:.2%}**")

########################
# 4) Interactive Altair Chart
########################
st.subheader("Interactive Logit vs. Probability Chart")

# Generate a range of logit values to plot
logit_values = np.linspace(-6, 6, 200)
df = pd.DataFrame({
    "logit": logit_values,
    "probability": 1 / (1 + np.exp(-logit_values))
})

# Create a line chart for Probability vs. Logit
line_chart = (
    alt.Chart(df)
    .mark_line()
    .encode(
        x=alt.X("logit", title="Logit"),
        y=alt.Y("probability", title="Probability", scale=alt.Scale(domain=[0,1]))
    )
)

# Add a vertical rule at the user's current logit
rule_data = pd.DataFrame({"logit": [user_logit]})
rule = alt.Chart(rule_data).mark_rule(color="red").encode(x="logit")

# Combine the line + rule
final_chart = (line_chart + rule).properties(
    width=600,
    height=400,
    title="Logit vs. Probability of Bleeding"
)

# Show the chart in Streamlit
st.altair_chart(final_chart, use_container_width=True)
