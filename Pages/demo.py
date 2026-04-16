import streamlit as st
import pandas as pd
from datetime import date

# Load data
model_weights = pd.read_csv("ridge_weights_skl.csv")
x_describe = pd.read_csv("x_describe.csv")

intercept = 1.087586

# Model weights
w_month = model_weights.loc[0, "SaleMonth"]
w_year = model_weights.loc[0, "SaleYear"]
w_sqr_ftg = model_weights.loc[0, "TotalFinishedArea"]
w_living_units = model_weights.loc[0, "LivingUnits"]

# Describe stats
month_d = x_describe["SaleMonth"]
year_d = x_describe["SaleYear"]
sqrt_ftg_d = x_describe["TotalFinishedArea"]
living_units_d = x_describe["LivingUnits"]

# Page setup
st.set_page_config(page_title="Model Demonstration")

st.title("Real Estate Price Ratio Model")

st.write("""This demo predicts the **sale-to-appraisal price ratio** based on property features.  
If you provide a known appraised value, the model will also estimate the expected sale price.""")

# Inputs

# Fixed data Frame
date = st.date_input("Transaction Date",min_value=date(2020, 1, 1),max_value=date(2024, 12, 31),value=date(2022, 6, 1))
sqr_ftg = st.number_input("Total Square Footage (ft):",min_value=200,max_value=20000,value=1500,step=50)
living_units = st.number_input("Number of Living Units:",min_value=1,max_value=4,value=1,step=1,format="%d")
appraised_val = st.number_input("Known Appraised Value ($):",min_value=50000.0,value=300000.0,step=10000.0,format="%.2f")

# Standardization

month = (date.month - month_d.iloc[1]) / month_d.iloc[2]
year = (date.year - year_d.iloc[1]) / year_d.iloc[2]
sqr_ftg = (sqr_ftg - sqrt_ftg_d.iloc[1]) / sqrt_ftg_d.iloc[2]
living_units = (living_units - living_units_d.iloc[1]) / living_units_d.iloc[2]

# Model prediction

price_ratio = (intercept + (w_month * month) + (w_year * year) + (w_sqr_ftg * sqr_ftg) + (w_living_units * living_units))
price_ratio = round(price_ratio, 2)

#raw_price_ratio = (intercept + (w_month * month) + (w_year * year) + (w_sqr_ftg * sqr_ftg) + (w_living_units * living_units))

# Calibration
#calibration_shift = 0.09
#price_ratio = raw_price_ratio - calibration_shift
#price_ratio = max(0.50, min(1.50, price_ratio))
#price_ratio = round(price_ratio, 2)

# Output

st.subheader("Prediction Results")

st.metric("Estimated Price Ratio", f"{price_ratio:.2f}")

# Interpretation
if price_ratio < 0.95:
    st.warning("Predicted to sell BELOW appraised value")
elif price_ratio <= 1.05:
    st.info("Predicted to sell NEAR appraised value")
else:
    st.success("Predicted to sell ABOVE appraised value")

# Sale price

st.subheader("Estimated Sale Price")

sale_price = round(price_ratio * appraised_val, 2)
st.metric("Estimated Sale Price", f"${sale_price:,.2f}")