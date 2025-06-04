import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="PrizePicks Edge Model", layout="wide")

st.title("📈 PrizePicks Model Predictions")
st.markdown("✅ Auto-updating props. 💥 Smash % = model confidence edge.")

# Load data
data_path = "data/model_predictions.csv"

if os.path.exists(data_path):
    df = pd.read_csv(data_path)
    
    # Basic cleaning
    df.columns = [col.strip().capitalize() for col in df.columns]
    df = df.rename(columns={
        'Prediction': 'Model Prediction',
        'Confidence': 'Smash %'
    })

    # Filter options
    if 'Sport' in df.columns:
        sports = ['All'] + sorted(df['Sport'].dropna().unique())
        selected_sport = st.selectbox("Filter by sport", sports)
        if selected_sport != "All":
            df = df[df['Sport'] == selected_sport]

    min_smash = st.slider("Minimum Smash %", min_value=0, max_value=100, value=80)
    df = df[df['Smash %'] >= min_smash]

    # Sort by Smash %
    df = df.sort_values("Smash %", ascending=False)

    # Display table
    st.dataframe(df.reset_index(drop=True), use_container_width=True)
else:
    st.warning("No model_predictions.csv file found in /data. Scraper/model may not have run yet.")