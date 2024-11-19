import math
from typing import List

def tf_idf_bin(corpus: List[str],list_mot: List[str]) -> List[List[float]]:
    """
    Calcule la matrice TF-IDF binaire pour un corpus donné.

    Args:
        corpus (List[str]): Le corpus de documents.
        list_mot (List[str]): La liste des mots du corpus.

    Returns:
        List[List[float]]: La matrice TF-IDF binaire.
    """
    # Initialiser la matrice TF-IDF
    matrix_tf_idf = [[0 for _ in list_mot] for _ in corpus]

    # Calculer le nombre de documents
    nombre_documents = len(corpus)

    # Calculer le nombre de documents contenant chaque mot
    nombre_documents_mot = [sum(1 for doc in corpus if mot in doc.split()) for mot in list_mot]

    # Calculer la matrice TF-IDF
    for i in range(len(corpus)):
        # Découper le document en mots
        mots_document = set(corpus[i].split())  # Utiliser un ensemble pour une recherche rapide

        for j, mot in enumerate(list_mot):
            # Calculer le terme TF binaire
            tf_binaire = 1 if mot in mots_document else 0

            # Calculer le terme IDF avec vérification pour éviter la division par zéro
            if nombre_documents_mot[j] > 0:
                idf = math.log10(nombre_documents / nombre_documents_mot[j])
            else:
                idf = 0

            # Calculer le terme TF-IDF binaire
            matrix_tf_idf[i][j] = tf_binaire * idf

    return matrix_tf_idf