import os
from update_from_drive import update_files_from_drive

# 🔁 Étape 1 : Télécharger les derniers fichiers depuis Google Drive
update_files_from_drive()

# ✏️ Étape 2 : Modifier légèrement dashboard.py pour forcer un changement détecté par Git
with open("dashboard.py", "a", encoding="utf-8") as f:
    f.write("\n# mise à jour automatique\n")

# 🌀 Étape 3 : Commit & Push automatique vers GitHub
os.system("git add .")
os.system('git commit -m "🔄 Mise à jour auto des fichiers depuis Drive"')
os.system("git push")
