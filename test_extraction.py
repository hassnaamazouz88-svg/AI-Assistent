import os
from core.ingestion.pipeline import process_document

fichier_a_tester = "storage/dossiers/37e3cb7d-3acc-4057-bd54-2348fbc4df06/Dernières pages.pdf"

print("Le fichier existe :", os.path.exists(fichier_a_tester))
print("Chemin absolu résolu :", os.path.abspath(fichier_a_tester))

texte = process_document(fichier_a_tester)
print("--- TEXTE EXTRAIT ---")
print(texte[:2000])
print(f"\nLongueur totale : {len(texte)} caractères")