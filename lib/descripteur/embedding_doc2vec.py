from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from typing import List
import numpy as np
from lib.descripteur.utils import appliquer_stemming


def calculer_vecteurs_doc2vec(corpus: List[str], list_mot: List[str], stemming: str) -> List[List[float]]:
    """
    Génère une matrice où chaque ligne représente un document par son vecteur Doc2Vec.

    Args:
        corpus (List[str]): Le corpus de documents.
        ist_mot (List[str]): Liste des mots du corpus.
        stemming (str): Option pour choisir le stemming.

    Returns:
        List[List[float]]: Matrice où chaque ligne représente un document par son vecteur Doc2Vec.
    """
    # Préparer les documents taggés avec le stemming appliqué
    documents_tagged = [
        TaggedDocument(words=appliquer_stemming(doc, stemming), tags=[i]) for i, doc in enumerate(corpus)
    ]

    # Entraîner un modèle Doc2Vec sur les documents taggés
    model = Doc2Vec(
        documents_tagged,
        vector_size=len(list_mot),  # Taille des vecteurs Doc2Vec
        window=5,
        min_count=1,
        workers=4,
        epochs=10
    )

    # Construire la matrice des vecteurs Doc2Vec
    matrix = []
    for document in corpus:
        mots_document = appliquer_stemming(document, stemming)

        # Vérifier la présence des mots de `list_mot` dans le document
        mots_filtres = [mot for mot in mots_document if mot in list_mot]

        if mots_filtres:
            # Inférer un vecteur pour le document complet basé sur les mots filtrés
            vecteur_document = model.infer_vector(mots_filtres)
        else:
            # Si aucun mot pertinent n'est trouvé, utiliser un vecteur nul
            vecteur_document = np.zeros(model.vector_size, dtype=float)

        # Convertir en liste explicite de float
        matrix.append(vecteur_document.tolist())

    return matrix
