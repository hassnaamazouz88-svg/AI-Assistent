from core.rag import vector_store
from core.rag.embedder import embed_query

# Remplace par le vrai id de ton dossier testé
dossier_id = "37e3cb7d-3acc-4057-bd54-2348fbc4df06"

# Vérifier combien de chunks ont été indexés au total pour ce dossier
collection = vector_store.get_collection()
resultat = collection.get(where={"dossier_id": dossier_id})
print(f"Nombre de chunks indexés : {len(resultat['ids'])}")

# Tester une vraie recherche sémantique
question = "Quel est le délai d'exécution du marché ?"
vecteur_question = embed_query(question)

resultats_recherche = vector_store.search(
    dossier_id=dossier_id,
    query_embedding=vecteur_question,
    top_k=5
)

print("\n--- Résultats de la recherche ---")
for doc, distance, metadata in zip(
    resultats_recherche["documents"][0],
    resultats_recherche["distances"][0],
    resultats_recherche["metadatas"][0]
):
    print(f"\n[{metadata['nom_fichier']}, distance: {distance:.3f}]")
    print(doc[:200])