from typing import List
import numpy as np
from gensim.models import Word2Vec
from lib.descripteur.utils import appliquer_stemming


def word2vec_matrix(corpus: List[str], list_mot: List[str], stemming: str) -> List[List[float]]:
    """
    Génère une matrice où chaque ligne représente un document par la moyenne des vecteurs Word2Vec des mots de `list_mot`.

    Args:
        corpus (List[str]): Le corpus de documents.
        list_mot (List[str]): Liste des mots du corpus.
        stemming (str): Option pour choisir le stemming.

    Returns:
        List[List[float]]: Matrice où chaque ligne représente un document.
    """
    # Appliquer le stemming au corpus
    corpus_stemmed = [appliquer_stemming(doc, stemming) for doc in corpus]

    # Entraîner un modèle Word2Vec sur le corpus transformé
    model = Word2Vec(
        sentences=corpus_stemmed,
        vector_size=len(list_mot),  # Taille des vecteurs pour chaque mot
        window=5,
        min_count=1,
        workers=4
    )

    # Construire la matrice pour représenter les documents
    matrix = []
    for document in corpus_stemmed:
        # Filtrer les mots pertinents dans le document (ceux présents dans list_mot)
        vecteurs_mots = [
            model.wv[mot] for mot in document if mot in model.wv and mot in list_mot
        ]

        if vecteurs_mots:
            # Moyenne des vecteurs des mots pour représenter le document
            vecteur_document = np.mean(vecteurs_mots, axis=0)
        else:
            # Si aucun mot pertinent n'est trouvé, utiliser un vecteur nul
            vecteur_document = np.zeros(model.vector_size)

        matrix.append(vecteur_document)

    return matrix
