import streamlit as st
import joblib
import pandas as pd
import numpy as np
import os
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
import datetime

# Modell betöltése
model = joblib.load(os.path.join("models", "final_model.pkl"))

st.title("Airbnb árbecslő dashboard")

st.sidebar.header("Paraméterek")
bedrooms = st.sidebar.slider("Hálószobák száma", 0, 10, 2)
bathrooms = st.sidebar.slider("Fürdőszobák száma", 0.0, 5.0, 1.5)
accommodates = st.sidebar.slider("Vendégek száma", 1, 16, 4)
reviews = st.sidebar.slider("Értékelések száma", 0, 500, 10)

# Predikció
input_data = pd.DataFrame([{
    "bedrooms": bedrooms,
    "bathrooms": bathrooms,
    "accommodates": accommodates,
    "number_of_reviews": reviews
}])

st.subheader("Megadott paraméterek")
st.write(input_data)

if st.button("Ár előrejelzése"):
    prediction = model.predict(input_data)[0]
    st.subheader(f"Előrejelzett ár: ${prediction:,.2f}")



st.subheader("EvidentlyAI riport")

# Referencia adatok (lehet a tanító adathalmaz egy szelete is)
reference_data = pd.read_csv(os.path.join("data", "listings.csv"))
reference_data = reference_data[['bedrooms', 'bathrooms', 'accommodates', 'number_of_reviews']]
reference_data.dropna(inplace=True)

# Aktuális predikció input (mint production input szimuláció)
current_data = input_data.copy()

if st.button("Riport generálása"):
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference_data, current_data=current_data)

    # Riport megjelenítése HTML-ként
    html_path = os.path.join("evidently_report", f"report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
    os.makedirs("evidently_report", exist_ok=True)
    report.save_html(html_path)

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    st.components.v1.html(html, height=600, scrolling=True)
