from sentence_transformers import SentenceTransformer


# Configuration

MODEL_NAME = "LiquidAI/LFM2.5-Embedding-350M"


# Chargement du modèle

_model = SentenceTransformer(
    MODEL_NAME,
    trust_remote_code=True
)


# Embeddings de documents (chunks à indexer)


def embed_documents(texts: list[str]) -> list[list[float]]:
    """
    Génère les embeddings d'une liste de chunks de documents,
    destinés à être indexés dans ChromaDB.

    Utilise prompt_name="document" : LFM2.5-Embedding-350M est un
    modèle asymétrique, entraîné avec des préfixes différents pour
    les requêtes et les passages. Omettre ce préfixe ne provoque
    aucune erreur, mais dégrade silencieusement la qualité de la
    recherche par similarité — donc à ne jamais oublier.
    """
    embeddings = _model.encode(
        texts,
        prompt_name="document",
        normalize_embeddings=True
    )
    return embeddings.tolist()


def embed_document(text: str) -> list[float]:
    """
    Génère l'embedding d'un seul chunk de document.
    """
    return embed_documents([text])[0]


# Embedding de requête (question posée par l'utilisateur)

def embed_query(text: str) -> list[float]:
    """
    Génère l'embedding d'une question utilisateur, destinée à être
    comparée aux chunks déjà indexés dans ChromaDB (retrieval).

    Utilise prompt_name="query" — préfixe différent de celui des
    documents, car ce modèle est un retriever asymétrique.
    """
    embedding = _model.encode(
        text,
        prompt_name="query",
        normalize_embeddings=True
    )
    return embedding.tolist()