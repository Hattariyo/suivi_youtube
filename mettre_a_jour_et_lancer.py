import os
from update_from_drive import update_files_from_drive

# 🔁 Étape 1 : Télécharger les derniers fichiers depuis Google Drive
update_files_from_drive()

# ✏️ Étape 2 : Modifier légèrement dashboard.py et historique_complet.csv
with open("dashboard.py", "a") as f:
    f.write("\n# mise à jour automatique")

with open("historique_complet.csv", "a") as f:
    f.write("\n")  # Ajout d’une ligne vide invisible mais détectée par Git

# 🌀 Étape 3 : Commit & Push automatique vers GitHub
os.system("git add .")
os.system("git commit -m \"🔄 Mise à jour auto des fichiers depuis Drive\"")
os.system("git push")
