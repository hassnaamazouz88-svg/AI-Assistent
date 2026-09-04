import uuid

import chromadb


CHROMA_PATH = "storage/chroma"
COLLECTION_NAME = "documents_ao"


_client = chromadb.PersistentClient(path=CHROMA_PATH)


def get_collection():
    """
    Récupère (ou crée si elle n'existe pas encore) la collection
    unique utilisée pour tous les dossiers. L'isolation entre
    dossiers se fait par filtrage sur la métadonnée "dossier_id",
    pas par une collection séparée par dossier.
    """
    return _client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )


def add_chunks(
    dossier_id: uuid.UUID,
    document_id: uuid.UUID,
    nom_fichier: str,
    chunks: list[dict]
) -> None:
    """
    Indexe les chunks d'un document dans ChromaDB.

    chunks: liste de dicts, chacun contenant au minimum :
        {"text": "...", "chunk_index": 0, "embedding": [...]}
    """
    if not chunks:
        return

    collection = get_collection()

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for chunk in chunks:
        chunk_id = f"{document_id}_{chunk['chunk_index']}"

        ids.append(chunk_id)
        documents.append(chunk["text"])
        embeddings.append(chunk["embedding"])
        metadatas.append({
            "dossier_id": str(dossier_id),
            "document_id": str(document_id),
            "nom_fichier": nom_fichier,
            "chunk_index": chunk["chunk_index"],
        })

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )


def search(
    dossier_id: uuid.UUID,
    query_embedding: list[float],
    top_k: int = 8
) -> dict:
    """
    Recherche les chunks les plus pertinents pour une question,
    filtrés sur un dossier précis.
    """
    collection = get_collection()

    return collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where={"dossier_id": str(dossier_id)},
    )


def delete_document_chunks(document_id: uuid.UUID) -> None:
    """
    Supprime tous les chunks d'un document précis.
    """
    collection = get_collection()
    collection.delete(where={"document_id": str(document_id)}) 