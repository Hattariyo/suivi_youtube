import pandas as pd
import plotly.express as px
import streamlit as st
import os

st.set_page_config(page_title="Suivi concours YouTube", layout="wide")
st.title("📊 Suivi du concours YouTube - Les Trésors d'Ulysse")

# === CHARGEMENT DES DONNÉES ===
HISTO_FILE = "historique_complet.csv"
if not os.path.exists(HISTO_FILE):
    st.error("Le fichier historique_complet.csv est introuvable.")
    st.stop()

historique = pd.read_csv(HISTO_FILE)
historique["timestamp"] = pd.to_datetime(historique["timestamp"])

# === SÉLECTION DES VIDÉOS ===
videos = historique["title"].unique()
defaut = [v for v in videos if "ulysse" in v.lower()]
selection = st.multiselect("Choisis les vidéos à afficher :", videos, default=defaut)
filtre = historique[historique["title"].isin(selection)]

# === GRAPHIQUE PERSONNALISÉ ===
graph_type = st.radio("Afficher :", ["Likes", "Rang"], horizontal=True)
fig = px.line(
    filtre,
    x="timestamp",
    y="likes" if graph_type == "Likes" else "rank",
    color="title",
    markers=True,
    title=f"Evolution des {'likes' if graph_type == 'Likes' else 'rangs'}"
)
if graph_type == "Rang":
    fig.update_yaxes(autorange="reversed")
st.plotly_chart(fig, use_container_width=True)

# === NOUVEAU : GRAPHIQUE TOP 20 ===
st.markdown("### 🏆 Evolution du classement du Top 20")
# Récupérer les 20 premières vidéos du dernier classement
last_ts = historique["timestamp"].max()
top20_ids = historique[historique["timestamp"] == last_ts].sort_values("rank").head(20)["video_id"].tolist()
top20_data = historique[historique["video_id"].isin(top20_ids)]
fig_top20 = px.line(
    top20_data,
    x="timestamp",
    y="rank",
    color="title",
    markers=True,
    title="Classement au fil du temps (Top 20)"
)
fig_top20.update_yaxes(autorange="reversed")
st.plotly_chart(fig_top20, use_container_width=True)

# === CLASSEMENT ACTUEL ===
st.markdown("### 📋 Classement actuel")
df_latest = historique[historique["timestamp"] == last_ts].sort_values("rank")
df_latest = df_latest[["rank", "title", "likes"]].reset_index(drop=True)
st.dataframe(df_latest, use_container_width=True)

# === BOUTON DE MISE A JOUR (optionnel) ===
if st.button("🔁 Mettre à jour maintenant"):
    os.system("python suivi_concours_v3.py")
    st.experimental_rerun()
