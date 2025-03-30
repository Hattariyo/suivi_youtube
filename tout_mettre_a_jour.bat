@echo off
echo 🔄 Lancement de la mise à jour des stats YouTube...
python suivi_concours_v3.py
echo ✅ historique_complet.csv mis à jour avec les dernières données.
pause

echo 🚀 Commit et push Git...
git add historique_complet.csv classement_youtube.csv dashboard.py
git commit -m "🔄 Mise à jour des fichiers manuelle"
git push

echo ✅ Tout est à jour ! Tu peux rafraîchir : https://suivi-youtube-ulysse.streamlit.app/
pause
