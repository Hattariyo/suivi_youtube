import streamlit as st
import pandas as pd
import plotly.express as px

# Chemins vers les fichiers locaux
HISTORIQUE_PATH = "historique_complet.csv"
CLASSEMENT_PATH = "classement_youtube.csv"

# Chargement des données
@st.cache_data
def load_data():
    historique = pd.read_csv(HISTORIQUE_PATH)
    classement = pd.read_csv(CLASSEMENT_PATH)
    return historique, classement

historique, classement = load_data()

# Sélection par défaut de la vidéo d'Ulysse
default_video = classement[classement["title"].str.contains("Ulysse")]["title"].iloc[0]

# Titre principal
st.title("🎟️ Suivi du concours YouTube - Les Trésors d'Ulysse")

# Sélecteur de vidéos
videos = classement["title"].tolist()
selected_videos = st.multiselect("Choisis les vidéos à afficher :", videos, default=[default_video])

# Choix de la métrique à afficher
metric = st.radio("Afficher :", ["Likes", "Rang"], horizontal=True)

# Filtrage des données sélectionnées
historique_selected = historique[historique["title"].isin(selected_videos)]

# Graphique principal (plus grand)
if not historique_selected.empty:
    st.markdown("### 📉 Évolution des likes" if metric == "Likes" else "### 📈 Évolution du rang")
    fig = px.line(
        historique_selected,
        x="timestamp",
        y="likes" if metric == "Likes" else "rank",
        color="title",
        height=700,
        width=1000
    )
    if metric == "Rang":
        fig.update_yaxes(autorange="reversed", title="Rang")
    else:
        fig.update_yaxes(title="Likes")
    st.plotly_chart(fig, use_container_width=False)

# 🏆 Classement actuel du top 20
st.markdown("""
### 🏅 Classement actuel du Top 20
""")
top20 = classement.sort_values("rank").head(20)[["rank", "title", "likes"]].reset_index(drop=True)
st.dataframe(top20, hide_index=True)

# 📊 Graphiques de l'évolution du top 20
historique_top20 = historique[historique["video_id"].isin(top20["rank"].index + 1)]

st.markdown("### 📊 Évolution des likes (Top 20)")
fig_likes = px.line(
    historique[historique["video_id"].isin(top20["video_id"])] if "video_id" in top20 else historique_top20,
    x="timestamp",
    y="likes",
    color="title",
    height=700,
    width=1000
)
st.plotly_chart(fig_likes, use_container_width=False)

st.markdown("### 🧭 Classement dans le temps (Top 20)")
fig_rank = px.line(
    historique[historique["video_id"].isin(top20["video_id"])] if "video_id" in top20 else historique_top20,
    x="timestamp",
    y="rank",
    color="title",
    height=700,
    width=1000
)
fig_rank.update_yaxes(autorange="reversed", title="Rang")
st.plotly_chart(fig_rank, use_container_width=False)