import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Suivi du concours YouTube", layout="wide")

# Chargement de l'historique
@st.cache_data
def load_data():
    return pd.read_csv("historique_complet.csv", parse_dates=["timestamp"])

df = load_data()

st.title("📊 Suivi du concours YouTube - Les Trésors d'Ulysse")

# Liste des vidéos
videos = df["title"].dropna().unique()
selection = st.multiselect("Choisis les vidéos à afficher :", videos, default=["Les Trésors d'Ulysse (Hauts de France) - Gaëlle Vasse"])

mode = st.radio("Afficher :", ["Likes", "Rang"], horizontal=True)

filtered_df = df[df["title"].isin(selection)]

if mode == "Likes":
    fig = px.line(filtered_df, x="timestamp", y="likes", color="title", markers=True, title="Evolution des likes")
else:
    fig = px.line(filtered_df, x="timestamp", y="rank", color="title", markers=True, title="Evolution du classement")
    fig.update_yaxes(autorange="reversed")

st.plotly_chart(fig, use_container_width=True)

# 💡 Top 20 à chaque instant
st.markdown("## 🏆 Evolution du classement du Top 20")

# Sélection des top 20 à chaque date
top20_historique = (
    df.sort_values(["timestamp", "rank"])
      .groupby("timestamp")
      .head(20)
)

fig_rank = px.line(
    top20_historique,
    x="timestamp",
    y="rank",
    color="title",
    markers=True,
    title="Classement dans le temps pour les 20 premières vidéos"
)
fig_rank.update_yaxes(autorange="reversed")
st.plotly_chart(fig_rank, use_container_width=True)

# ❤️ Likes des top 20
st.markdown("## ❤️ Evolution des likes du Top 20")

fig_likes = px.line(
    top20_historique,
    x="timestamp",
    y="likes",
    color="title",
    markers=True,
    title="Evolution des likes dans le temps pour les 20 premières vidéos"
)
st.plotly_chart(fig_likes, use_container_width=True)
