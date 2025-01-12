import math
from typing import List
from lib.spacy_nltk.stemming import *

def tf_idf_bin(corpus: List[str], list_mot: List[str], stemming: str) -> List[List[float]]:
    """
    Calcule la matrice TF-IDF binaire pour un corpus donné.

    Args:
        corpus (List[str]): Le corpus de documents.
        list_mot (List[str]): La liste des mots du corpus.
        stemming (str): Option pour choisir le stemming (1 -> Porter, 2 -> Snowball, 3 -> Lancaster, 4 -> Lemmatization, 5 -> Lovins, 6 -> Aucun stemming)

    Returns:
        List[List[float]]: La matrice TF-IDF binaire.
    """
    
    # Fonction de stemming en fonction de l'option
    def appliquer_stemming(phrase: str, stemming: str) -> List[str]:
        phrase = phrase.lower()

        if stemming == "1":
            return porter_stemmer_phrase(phrase)
        elif stemming == "2":
            return snowball_stemmer_phrase(phrase)
        elif stemming == "3":
            return lancaster_stemmer_phrase(phrase)
        elif stemming == "4":
            return wordnet_lemmatizer_phrase(phrase)
        elif stemming == "5":
            return lovins_stemmer(phrase)
        else:
            # Pas de stemming appliqué, on garde les mots d'origine
            return phrase.split()

    # Initialiser la matrice TF-IDF
    matrix_tf_idf = [[0 for _ in list_mot] for _ in corpus]

    # Calculer le nombre de documents
    nombre_documents = len(corpus)

    # Calculer le nombre de documents contenant chaque mot
    nombre_documents_mot = [sum(1 for doc in corpus if mot in doc.split()) for mot in list_mot]

    # Calculer la matrice TF-IDF
    for i in range(len(corpus)):
        # Appliquer le stemming ou non selon l'option
        mots_document = appliquer_stemming(corpus[i], stemming)

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
