# app/app.py

import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium

# Charger les données
df = pd.read_csv("../data/event_data.csv")

st.title("Visualisation des Événements et Statistiques Utilisateurs")

# Carte des événements
st.subheader("Carte des événements")
m = folium.Map(location=[df["location_lat"].mean(), df["location_lon"].mean()], zoom_start=5)
for _, row in df.iterrows():
    folium.Marker(
        [row["location_lat"], row["location_lon"]],
        popup=f"Event ID: {row['event_id']}"
    ).add_to(m)
st_folium(m, width=700)

# Top événements
st.subheader("Événements les plus populaires")
top_events = df[df["attended"] == 1]["event_id"].value_counts().head(5)
st.bar_chart(top_events)

# Filtrer par utilisateur
st.subheader("Participation d'un utilisateur")
user_id = st.text_input("Entrer un user_id", "42")
user_events = df[df["user_id"] == user_id]
st.write(user_events)
