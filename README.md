# Real Estate Price Ratio Demo (Raissa Version)

This Streamlit app demonstrates a trained Ridge Regression model predicting the sale-to-appraisal price ratio.

## Features
- Predicts price ratio (sale / appraisal)
- Estimates sale price
- Uses property characteristics:
- Sale date
- Square footage
- Number of living units

## Notes
- Model trained on filtered data (ratio between 0.5 and 1.5)
- Predictions outside this range should be interpreted cautiously

## How to run
streamlit run webapp.py