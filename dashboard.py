import streamlit as st
import pandas as pd
import plotly.express as px

# Liens Google Drive en mode "téléchargement direct"
HISTORIQUE_URL = "https://drive.google.com/uc?id=1qFUHW811O3DsMv8bRducbc4l0L3VRYY5"
CLASSEMENT_URL = "https://drive.google.com/uc?id=1F5XghVQghx1KZD7_ZRPSEVOjQbyXxDj2"

# Chargement des données
@st.cache_data
def load_data():
    historique = pd.read_csv(HISTORIQUE_URL)
    classement = pd.read_csv(CLASSEMENT_URL)
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

# Graphique d'évolution des likes ou du rang
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

# 🏆 Graphique de l'évolution du top 20 (likes)
st.markdown("""
### 🏆 Evolution du classement du Top 20
""")

# Filtrer l'historique pour les 20 vidéos les mieux classées actuellement
top20_ids = classement.sort_values("rank").head(20)["video_id"].tolist()
top20_historique = historique[historique["video_id"].isin(top20_ids)]

fig_likes = px.line(
    top20_historique,
    x="timestamp",
    y="likes",
    color="title",
    title="Évolution des likes pour les 20 premières vidéos"
)
st.plotly_chart(fig_likes)

# 📊 Graphique de l'évolution du classement (rang) du top 20
fig_rank = px.line(
    top20_historique,
    x="timestamp",
    y="rank",
    color="title",
    title="Classement dans le temps pour les 20 premières vidéos"
)
fig_rank.update_yaxes(title="rang", autorange="reversed")
st.plotly_chart(fig_rank)

# mise à jour automatique
