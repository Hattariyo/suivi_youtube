import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Récupération des URLs ou chemins locaux
HISTORIQUE_PATH = "historique_complet.csv"
CLASSEMENT_PATH = "classement_youtube.csv"

@st.cache_data
def load_data():
    historique = pd.read_csv(HISTORIQUE_PATH)
    classement = pd.read_csv(CLASSEMENT_PATH)
    return historique, classement

historique, classement = load_data()

# 🧠 Préparation
video_titles = classement["title"].tolist()
default_video = [v for v in video_titles if "Trésors d'Ulysse" in v]
selected_videos = st.multiselect(
    "Choisis les vidéos à afficher :",
    options=video_titles,
    default=default_video or video_titles[:1]
)

# 🎯 Choix métrique
metric = st.radio("Afficher :", ["Likes", "Rang"], horizontal=True)

# 📈 Graphique d'évolution (vidéo sélectionnée)
filtered_data = historique[historique["title"].isin(selected_videos)]
y_axis = "likes" if metric == "Likes" else "rank"
fig = px.line(
    filtered_data,
    x="timestamp",
    y=y_axis,
    color="title",
    markers=True,
)
fig.update_layout(
    autosize=True,
    width=None,
    height=500,
    margin=dict(l=40, r=40, t=40, b=40)
)
st.header("📉 Évolution des " + metric.lower())
st.plotly_chart(fig, use_container_width=True)

# 🏆 Tableau du top 20
st.markdown("### 🏅 Classement actuel du Top 20")
top20 = (
    classement.sort_values("rank")
    .head(20)
    [["rank", "title", "likes", "views"]]
    .rename(columns={
        "rank": "Rang",
        "title": "Titre",
        "likes": "Likes",
        "views": "Vues"
    })
)
st.dataframe(top20, use_container_width=True, hide_index=True)

# 📊 Graphique likes (top 20)
top20_titles = top20["Titre"].tolist()
df_top20 = historique[historique["title"].isin(top20_titles)]

fig_likes = px.line(df_top20, x="timestamp", y="likes", color="title")
fig_likes.update_layout(
    autosize=True,
    width=None,
    height=600,
    margin=dict(l=40, r=40, t=40, b=40)
)
st.header("📊 Évolution des likes (Top 20)")
st.plotly_chart(fig_likes, use_container_width=True)

# 📊 Graphique classement (top 20)
fig_rank = px.line(df_top20, x="timestamp", y="rank", color="title")
fig_rank.update_yaxes(autorange="reversed")
fig_rank.update_layout(
    autosize=True,
    width=None,
    height=600,
    margin=dict(l=40, r=40, t=40, b=40)
)
st.header("📉 Classement dans le temps (Top 20)")
st.plotly_chart(fig_rank, use_container_width=True)
