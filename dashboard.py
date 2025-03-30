
import streamlit as st
import pandas as pd
import plotly.express as px

# Liens Google Drive en mode "téléchargement direct"
HISTORIQUE_URL = "https://drive.google.com/uc?id=1Oi5kWc173-Z4ecnySTkbz6hffuYigXri"
CLASSEMENT_URL = "https://drive.google.com/uc?id=1c0LeysCYhrKr6JaXD6w-XCHmPMwpXvAu"

# Chargement des données
@st.cache_data
def load_data():
    historique = pd.read_csv(HISTORIQUE_URL)
    classement = pd.read_csv(CLASSEMENT_URL)
    return historique, classement

historique, classement = load_data()

# Sélection de la vidéo "Les Trésors d'Ulysse" par défaut
ulysse_title = classement[classement["title"].str.contains("Trésors d'Ulysse", case=False, na=False)]["title"].iloc[0]

# Titre du dashboard
st.title("🎟️ Suivi du concours YouTube - Les Trésors d'Ulysse")

# Liste déroulante pour sélectionner une ou plusieurs vidéos
videos = classement["title"].tolist()
selected_videos = st.multiselect("Choisis les vidéos à afficher :", videos, default=[ulysse_title])

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
        title="📈 Évolution des likes"
    )
    fig.update_yaxes(title="likes")
else:
    fig = px.line(
        historique_selected,
        x="timestamp",
        y="rank",
        color="title",
        title="📉 Évolution du rang"
    )
    fig.update_yaxes(title="rang", autorange="reversed")

st.plotly_chart(fig, use_container_width=True, height=500)

# 🏆 Classement top 20 actuel sous forme de tableau
st.markdown("### 🏆 Classement actuel du Top 20")
top20 = classement.sort_values("rank").head(20)[["rank", "title", "likes", "views"]]
st.dataframe(top20.style.format({"likes": "{:,}", "views": "{:,}"}), use_container_width=True)

# 🔁 Historique du top 20
top20_ids = top20["title"].tolist()
top20_historique = historique[historique["title"].isin(top20_ids)]

# 📊 Graphique de l'évolution des likes
fig_likes = px.line(
    top20_historique,
    x="timestamp",
    y="likes",
    color="title",
    title="📊 Évolution des likes (Top 20)"
)
st.plotly_chart(fig_likes, use_container_width=True, height=600)

# 📈 Graphique de l'évolution du classement (rang)
fig_rank = px.line(
    top20_historique,
    x="timestamp",
    y="rank",
    color="title",
    title="📉 Classement dans le temps (Top 20)"
)
fig_rank.update_yaxes(title="rang", autorange="reversed")
st.plotly_chart(fig_rank, use_container_width=True, height=600)
