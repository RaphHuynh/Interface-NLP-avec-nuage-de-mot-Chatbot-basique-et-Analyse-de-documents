import math
from typing import List
from lib.descripteur.utils import appliquer_stemming

def tf_idf_new(corpus: List[str],list_mot: List[str], stemming: int) -> List[List[float]]:
    """ Calcule la matrice TF-IDF pour un corpus donné.
    
    Args:
        corpus (List[str]): Le corpus de documents.
        list_mot (List[str]): La liste des mots du corpus.
        
    Returns:
        List[List[float]]: La matrice TF-IDF.
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
        mots_document = appliquer_stemming(corpus[i], stemming)
        longueur_document = len(mots_document)

        for j, mot in enumerate(list_mot):
            # Calculer le nombre d'occurrences du mot dans le document
            nombre_occurrences = mots_document.count(mot)

            # Calculer le terme TF
            if longueur_document <= 0:
                tf = math.inf
            elif  math.log2(longueur_document) == 0:
                tf = math.inf
            else:
                log2longueur_document = math.log2(longueur_document)
                tf = math.log2(1 + nombre_occurrences) / log2longueur_document

            # Calculer le terme IDF avec vérification pour éviter la division par zéro
            if nombre_documents_mot[j] > 0:
                idf = math.log10(1 + (nombre_documents / nombre_documents_mot[j]))
            else:
                idf = 0

            # Calculer le terme TF-IDF
            matrix_tf_idf[i][j] = tf * idf

    return matrix_tf_idf