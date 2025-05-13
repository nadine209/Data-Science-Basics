import pandas as pd
import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# Charger les données
df = pd.read_csv(r"C:\Users\nadin_pbj\Data-Science-Basics\data\event_data.csv")

# Vérifier si les colonnes nécessaires sont présentes
if not all(col in df.columns for col in ["user_id", "event_id", "attended", "location_lat", "location_lon"]):
    st.error("Le fichier CSV ne contient pas toutes les colonnes nécessaires.")
else:
    # Convertir user_id en chaîne si nécessaire
    df['user_id'] = df['user_id'].astype(str)

# Titre de l'application
st.title("Visualisation des Événements et Statistiques Utilisateurs")

# Carte des événements
st.subheader("Carte des événements")
# Initialiser la carte à la moyenne des coordonnées
m = folium.Map(location=[df["location_lat"].mean(), df["location_lon"].mean()], zoom_start=5)

# Créer un objet MarkerCluster pour grouper les événements proches
marker_cluster = MarkerCluster().add_to(m)

# Ajouter les marqueurs sur la carte avec une personnalisation
for _, row in df.iterrows():
    # Choisir une couleur pour chaque événement basé sur l'ID (par exemple)
    color = "blue" if row["attended"] == 1 else "red"
    
    folium.Marker(
        location=[row["location_lat"], row["location_lon"]],
        popup=f"Event ID: {row['event_id']} - {'Attended' if row['attended'] == 1 else 'Not Attended'}",
        icon=folium.Icon(color=color)
    ).add_to(marker_cluster)

# Afficher la carte dans Streamlit
st_folium(m, width=700)

# Top événements les plus populaires (les événements auxquels les utilisateurs ont assisté)
st.subheader("Événements les plus populaires")
top_events = df[df["attended"] == 1]["event_id"].value_counts().head(5)
st.bar_chart(top_events)

# Filtrer par utilisateur
st.subheader("Participation d'un utilisateur")
user_id = st.text_input("Entrer un user_id", "42")

# Vérifier si l'utilisateur existe dans les données
if user_id in df["user_id"].values:
    user_events = df[df["user_id"] == user_id]  # Filtrer les événements de l'utilisateur
    if user_events.empty:
        st.write(f"Aucun événement trouvé pour l'utilisateur {user_id}.")
    else:
        st.write(f"Événements de l'utilisateur {user_id}:")
        st.write(user_events)
else:
    st.write(f"Utilisateur {user_id} non trouvé dans les données.")
