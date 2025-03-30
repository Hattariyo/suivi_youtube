import streamlit as st
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

HISTORIQUE_URL = os.getenv("HISTORIQUE_URL", "historique_complet.csv")
CLASSEMENT_URL = os.getenv("CLASSEMENT_URL", "classement_youtube.csv")

@st.cache_data
def load_data():
    historique = pd.read_csv(HISTORIQUE_URL)
    classement = pd.read_csv(CLASSEMENT_URL, sep=",", names=["video_id", "title", "likes", "rank"], skiprows=1)
    return historique, classement

historique, classement = load_data()

# Sélection automatique de la vidéo d'Ulysse
default_video = [titre for titre in historique['title'].unique() if "Ulysse" in titre][:1]

st.markdown("""
    <h1 style='font-size: 3em;'>🎫 Suivi du concours YouTube - Les Trésors d'Ulysse</h1>
""", unsafe_allow_html=True)

selected_titles = st.multiselect("Choisis les vidéos à afficher :", options=historique['title'].unique(), default=default_video)
mode = st.radio("Afficher :", ["Likes", "Rang"], horizontal=True)

if selected_titles:
    filtered = historique[historique['title'].isin(selected_titles)]
    fig = px.line(
        filtered,
        x="timestamp",
        y="likes" if mode == "Likes" else "rank",
        color="title",
        markers=True,
    )
    fig.update_layout(height=600)
    st.markdown(f"""
        <h3 style='margin-top: 30px;'>📉 Évolution des {mode.lower()}</h3>
    """, unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)

# Classement Top 20
top20 = classement.sort_values("rank").head(20)[["rank", "title", "likes"]].reset_index(drop=True)
top20.columns = ["Rang", "Titre", "Likes"]

st.markdown("""
    <h3 style='margin-top: 50px;'>🏆 Classement actuel du Top 20</h3>
""", unsafe_allow_html=True)
st.dataframe(top20, use_container_width=True, hide_index=True)

# Graphiques globaux sur le top 20
top20_titles = top20["Titre"].tolist()
filtered_top20 = historique[historique["title"].isin(top20_titles)]

# Évolution des likes (Top 20)
fig_likes = px.line(
    filtered_top20,
    x="timestamp",
    y="likes",
    color="title",
    markers=False,
)
fig_likes.update_layout(height=700)
st.markdown("""
    <h3 style='margin-top: 50px;'>📊 Évolution des likes (Top 20)</h3>
""", unsafe_allow_html=True)
st.plotly_chart(fig_likes, use_container_width=True)

# Évolution du rang (Top 20)
fig_rank = px.line(
    filtered_top20,
    x="timestamp",
    y="rank",
    color="title",
    markers=False,
)
fig_rank.update_layout(height=700, yaxis_autorange="reversed")
st.markdown("""
    <h3 style='margin-top: 50px;'>📈 Classement dans le temps (Top 20)</h3>
""", unsafe_allow_html=True)
st.plotly_chart(fig_rank, use_container_width=True)