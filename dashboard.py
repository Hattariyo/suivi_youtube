import streamlit as st
import pandas as pd
import plotly.express as px

# Lecture des fichiers locaux
@st.cache_data
def load_data():
    historique = pd.read_csv("historique_complet.csv")
    classement = pd.read_csv("classement_youtube.csv")
    return historique, classement

historique, classement = load_data()

# Sélection de la vidéo d'Ulysse par défaut
ulysse_title = "Les Trésors d'Ulysse (Hauts de France) - Gaëlle Vasse"
videos = classement["title"].tolist()
default_video = ulysse_title if ulysse_title in videos else videos[0]
selected_videos = st.multiselect("🎞️ Choisis les vidéos à afficher :", videos, default=[default_video])

metric = st.radio("Afficher :", ["Likes", "Rang"], horizontal=True)

# Filtrage
historique_selected = historique[historique["title"].isin(selected_videos)]

# 📈 Graphique principal (agrandi)
if metric == "Likes":
    fig = px.line(
        historique_selected,
        x="timestamp",
        y="likes",
        color="title",
        title="📉 Évolution des likes"
    )
    fig.update_yaxes(title="Likes")
else:
    fig = px.line(
        historique_selected,
        x="timestamp",
        y="rank",
        color="title",
        title="📈 Évolution du rang"
    )
    fig.update_yaxes(title="Rang", autorange="reversed")

fig.update_layout(height=700, width=1200)
st.plotly_chart(fig)

# 🏆 Tableau du top 20
st.markdown("### 🏆 Classement actuel du Top 20")
top20 = classement.sort_values("rank").head(20)[["rank", "title", "likes"]]
st.dataframe(top20.reset_index(drop=True), use_container_width=True)

# 📊 Graphiques du Top 20
top20_ids = classement.sort_values("rank").head(20)["video_id"].tolist()
top20_historique = historique[historique["video_id"].isin(top20_ids)]

if not top20_historique.empty:
    # Graph likes
    fig_likes = px.line(
        top20_historique,
        x="timestamp",
        y="likes",
        color="title",
        title="📊 Évolution des likes (Top 20)"
    )
    fig_likes.update_layout(height=700, width=1200)
    st.plotly_chart(fig_likes)

    # Graph rang
    fig_rank = px.line(
        top20_historique,
        x="timestamp",
        y="rank",
        color="title",
        title="📈 Classement dans le temps (Top 20)"
    )
    fig_rank.update_yaxes(autorange="reversed")
    fig_rank.update_layout(height=700, width=1200)
    st.plotly_chart(fig_rank)
else:
    st.warning("Aucune donnée historique disponible pour le top 20.")
