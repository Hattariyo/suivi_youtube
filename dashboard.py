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

# Titre du dashboard
st.title("🎟️ Suivi du concours YouTube - Les Trésors d'Ulysse")

# Sélection automatique de la vidéo d'Ulysse
videos = classement["title"].tolist()
selected_videos = st.multiselect("Choisis les vidéos à afficher :", videos, default=["Les trésors d'Ulysse"])

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
        title="Évolution des likes",
        width=800, height=400
    )
    fig.update_yaxes(title="likes")
else:
    fig = px.line(
        historique_selected,
        x="timestamp",
        y="rank",
        color="title",
        title="Évolution du rang",
        width=800, height=400
    )
    fig.update_yaxes(title="rang", autorange="reversed")

st.plotly_chart(fig)

# 🏆 Tableau du classement des 20 vidéos
st.markdown("""
### 🏆 Classement des 20 premières vidéos
""")
top20_df = classement.sort_values("rank").head(20)[["title", "likes", "views"]]
st.dataframe(top20_df)

# 📊 Graphique de l'évolution du top 20 (likes)
fig_likes = px.line(
    historique[historique["video_id"].isin(top20_df["video_id"])],
    x="timestamp",
    y="likes",
    color="title",
    title="Évolution des likes pour les 20 premières vidéos",
    width=800, height=400
)
st.plotly_chart(fig_likes)

# 📊 Graphique de l'évolution du classement (rang) du top 20
fig_rank = px.line(
    historique[historique["video_id"].isin(top20_df["video_id"])],
    x="timestamp",
    y="rank",
    color="title",
    title="Classement dans le temps pour les 20 premières vidéos",
    width=800, height=400
)
fig_rank.update_yaxes(title="rang", autorange="reversed")
st.plotly_chart(fig_rank)
