import streamlit as st
import pandas as pd
import plotly.express as px

# Chargement des données locales
@st.cache_data
def load_data():
    historique = pd.read_csv("historique_complet.csv")
    classement = pd.read_csv("classement_youtube.csv")
    return historique, classement

historique, classement = load_data()

# Titre du dashboard
st.title("🎟️ Suivi du concours YouTube - Les Trésors d'Ulysse")

# Liste déroulante pour sélectionner une ou plusieurs vidéos
videos = classement["title"].tolist()
selected_videos = st.multiselect("Choisis les vidéos à afficher :", videos, default=videos[:1])

# Sélecteur du type de données à afficher
metric = st.radio("Afficher :", ["Likes", "Rang"], horizontal=True)

# Filtrage de l'historique pour les vidéos sélectionnées
historique_selected = historique[historique["title"].isin(selected_videos)]

# Graphique principal
if metric == "Likes":
    fig = px.line(
        historique_selected,
        x="timestamp",
        y="likes",
        color="title",
        title="Évolution des likes"
    )
    fig.update_yaxes(title="likes")
else:
    fig = px.line(
        historique_selected,
        x="timestamp",
        y="rank",
        color="title",
        title="Évolution du rang"
    )
    fig.update_yaxes(title="rang", autorange="reversed")

st.plotly_chart(fig)

# 🏆 Graphique du Top 20
st.markdown("### 🏆 Evolution du classement du Top 20")

top20_ids = classement.sort_values("rank").head(20)["video_id"].tolist()
top20_historique = historique[historique["video_id"].isin(top20_ids)]

fig_likes = px.line(
    top20_historique,
    x="timestamp",
    y="likes",
    color="title",
    title="Évolution des likes (Top 20)"
)
st.plotly_chart(fig_likes)

fig_rank = px.line(
    top20_historique,
    x="timestamp",
    y="rank",
    color="title",
    title="Classement dans le temps (Top 20)"
)
fig_rank.update_yaxes(title="rang", autorange="reversed")
st.plotly_chart(fig_rank)
