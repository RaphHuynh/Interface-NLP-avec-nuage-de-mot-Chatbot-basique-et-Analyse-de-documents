from typing import List
import numpy as np
from gensim.models import FastText
from lib.descripteur.utils import appliquer_stemming

def calculer_vecteurs_fasttext(corpus: List[str], list_mot: List[str], stemming: str) -> List[List[float]]:
    """
    Génère une représentation vectorielle pour chaque document du corpus en utilisant Word2Vec ou FastText.
    
    Args:
        corpus (List[str]): Le corpus de documents.
        list_mot (List[str]): Liste des mots du corpus.
        stemming (str): Option pour choisir le stemming.

    Returns:
        List[np.ndarray]: Liste des vecteurs pour chaque document.
    """
    corpus_stemmed = [appliquer_stemming(doc, stemming) for doc in corpus]
    
    model = FastText(
        sentences=[appliquer_stemming(doc, stemming) for doc in corpus],
        vector_size=len(list_mot),
        window=5,
        min_count=1,
        workers=4,
        sg=1
    )
    
    # Construire la matrice
    matrix = []
    for document in corpus_stemmed:
        vecteurs_mots = [
            model.wv[mot] for mot in document if mot in model.wv and mot in list_mot
        ]
        if vecteurs_mots:
            # Calculer la moyenne des vecteurs des mots du document
            vecteur_document = np.mean(vecteurs_mots, axis=0)
        else:
            # Si aucun mot pertinent n'est trouvé, utiliser un vecteur nul
            vecteur_document = np.zeros(model.vector_size)
        
        matrix.append(vecteur_document)
    
    return matrix