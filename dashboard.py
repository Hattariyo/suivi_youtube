import streamlit as st
import pandas as pd
import plotly.express as px

# Liens vers fichiers statiques
HISTORIQUE_URL = "historique_complet.csv"
CLASSEMENT_URL = "classement_youtube.csv"

# Chargement des données
@st.cache_data
def load_data():
    historique = pd.read_csv(HISTORIQUE_URL)
    classement = pd.read_csv(CLASSEMENT_URL)
    return historique, classement

historique, classement = load_data()

# Titre du dashboard
st.title("🎟️ Suivi du concours YouTube - Les Trésors d'Ulysse")

# Choix des vidéos
videos = classement["title"].tolist()

# ➤ Sélection par défaut = Ulysse
default_selection = [v for v in videos if "ulysse" in v.lower()]
if not default_selection:
    default_selection = [videos[0]]

selected_videos = st.multiselect("Choisis les vidéos à afficher :", videos, default=default_selection)

# ➤ Radio : Likes ou Rang
metric = st.radio("Afficher :", ["Likes", "Rang"], horizontal=True)

# ➤ Historique filtré
historique_selected = historique[historique["title"].isin(selected_videos)]

# ➤ Graphique principal : Likes ou Rang
if metric == "Likes":
    fig = px.line(historique_selected, x="timestamp", y="likes", color="title", title="📈 Évolution des likes", height=500)
    fig.update_yaxes(title="likes")
else:
    fig = px.line(historique_selected, x="timestamp", y="rank", color="title", title="📉 Évolution du rang", height=500)
    fig.update_yaxes(title="rang", autorange="reversed")

st.plotly_chart(fig, use_container_width=True)

# ➤ Tableau de classement
st.markdown("## 🏆 Classement Actuel (Top 20)")
top20 = classement.sort_values("rank").head(20)[["rank", "title", "likes"]].reset_index(drop=True)
top20.index = top20["rank"]
st.dataframe(top20[["title", "likes"]], use_container_width=True, height=600)

# ➤ Graphiques d'évolution du top 20
top20_ids = classement.sort_values("rank").head(20)["video_id"].tolist()
top20_historique = historique[historique["video_id"].isin(top20_ids)]

st.markdown("## 🔁 Évolution des likes du Top 20")
fig_likes = px.line(top20_historique, x="timestamp", y="likes", color="title", height=500)
st.plotly_chart(fig_likes, use_container_width=True)

st.markdown("## 🔁 Évolution du classement du Top 20")
fig_rank = px.line(top20_historique, x="timestamp", y="rank", color="title", height=500)
fig_rank.update_yaxes(autorange="reversed")
st.plotly_chart(fig_rank, use_container_width=True)
