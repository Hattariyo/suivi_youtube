@echo off
chcp 65001 >nul
echo 🔄 Lancement de la mise à jour des stats YouTube...
call mettre_a_jour_v3.bat

echo.
echo 🚀 Mise à jour du dashboard Streamlit en ligne...
python mettre_a_jour_et_lancer.py

echo.
echo ✅ Tout est à jour ! Tu peux rafraîchir : https://suivi-youtube-ulysse.streamlit.app/
pause
