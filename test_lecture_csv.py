with open("historique_complet.csv", "rb") as f:
    content = f.read()

for i in range(len(content)):
    try:
        content[:i].decode("utf-8")
    except UnicodeDecodeError as e:
        print(f"❌ Erreur à la position {i} : {e}")
        break
