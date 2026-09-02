import os
from core.ingestion.pipeline import process_document

fichier_a_tester = "storage/dossiers/48ef5e75-466a-4828-b0e4-63acb730e416/Avis Français.doc"

print("Le fichier existe :", os.path.exists(fichier_a_tester))
print("Chemin absolu résolu :", os.path.abspath(fichier_a_tester))

texte = process_document(fichier_a_tester)
print("--- TEXTE EXTRAIT ---")
print(texte[:2000])
print(f"\nLongueur totale : {len(texte)} caractères")