def build_text_from_pdf(data: dict) -> str:
    """
    Transforme les données extraites d'un PDF
    en texte prêt pour le chunking.
    """

    parts = []

    for page in data["pages"]:

        page_number = page["page_number"]
        text = page["text"].strip()

        if not text:
            continue

        parts.append(
            f"[Page {page_number}]\n{text}"
        )

    return "\n\n".join(parts)


def build_text_from_docx(data: dict) -> str:
    """
    Transforme les données extraites d'un DOCX
    en texte prêt pour le chunking.

    Combine les paragraphes (texte libre) et les tableaux
    (aplatis ligne par ligne, séparateur " | ").
    """

    parts = []

    # Paragraphes
    for paragraphe in data["paragraphes"]:
        parts.append(paragraphe)

    # Tableaux
    for numero_tableau, tableau in enumerate(data["tableaux"], start=1):

        parts.append(f"[Tableau {numero_tableau}]")

        for ligne in tableau:

            cellules_non_vides = [cell for cell in ligne if cell]

            if cellules_non_vides:
                parts.append(" | ".join(cellules_non_vides))

    return "\n\n".join(parts)


def build_text_from_xlsx(data: dict) -> str:
    """
    Transforme les données extraites d'un XLSX
    en texte prêt pour le chunking.
    """

    parts = []

    for sheet_name, rows in data["sheets"].items():

        parts.append(f"[Feuille : {sheet_name}]")

        for row in rows:

            valeurs_non_vides = [
                str(value) for value in row if value
            ]

            if valeurs_non_vides:
                parts.append(" | ".join(valeurs_non_vides))

    return "\n".join(parts)