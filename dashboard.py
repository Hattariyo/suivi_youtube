import streamlit as st
import pandas as pd
import plotly.express as px

# Liens vers les fichiers locaux (plus de Drive)
HISTORIQUE_PATH = "historique_complet.csv"
CLASSEMENT_PATH = "classement_youtube.csv"

# Chargement des données
@st.cache_data
def load_data():
    historique = pd.read_csv(HISTORIQUE_PATH)
    classement = pd.read_csv(CLASSEMENT_PATH)
    return historique, classement

historique, classement = load_data()

# Titre
st.title("🎟️ Suivi du concours YouTube - Les Trésors d'Ulysse")

# Vidéo par défaut = Les Trésors d'Ulysse
titre_defaut = "Les Trésors d'Ulysse (Hauts de France) - Gaëlle Vasse"
videos = classement["title"].tolist()
default_video = [v for v in videos if "Les Trésors d'Ulysse" in v]
selected_videos = st.multiselect("Choisis les vidéos à afficher :", videos, default=default_video)

# Choix de la métrique
metric = st.radio("Afficher :", ["Likes", "Rang"], horizontal=True)

# Filtrage historique
historique_selected = historique[historique["title"].isin(selected_videos)]

# Graphique principal
if not historique_selected.empty:
    st.markdown("### 📉 Évolution des likes" if metric == "Likes" else "### 📈 Évolution du rang")
    fig = px.line(
        historique_selected,
        x="timestamp",
        y="likes" if metric == "Likes" else "rank",
        color="title",
        height=500,
    )
    if metric == "Rang":
        fig.update_yaxes(autorange="reversed", title="Rang")
    else:
        fig.update_yaxes(title="Likes")
    st.plotly_chart(fig, use_container_width=True)

# 📊 Classement tableau
st.markdown("### 🏆 Classement actuel du Top 20")
top20 = classement.sort_values("rank").head(20)[["rank", "title", "likes"]]
top20 = top20.rename(columns={"rank": "Rang", "title": "Titre", "likes": "Likes"})
st.dataframe(top20, use_container_width=True)

# 🔁 Graphiques Top 20
top20_ids = top20["Titre"].tolist()
historique_top20 = historique[historique["title"].isin(top20_ids)]

# Likes dans le temps (Top 20)
st.markdown("### 📊 Évolution des likes (Top 20)")
fig_likes = px.line(
    historique_top20,
    x="timestamp",
    y="likes",
    color="title",
    height=500,
)
st.plotly_chart(fig_likes, use_container_width=True)

# Rang dans le temps (Top 20)
st.markdown("### 🧭 Classement dans le temps (Top 20)")
fig_rank = px.line(
    historique_top20,
    x="timestamp",
    y="rank",
    color="title",
    height=500,
)
fig_rank.update_yaxes(autorange="reversed", title="Rang")
st.plotly_chart(fig_rank, use_container_width=True)
