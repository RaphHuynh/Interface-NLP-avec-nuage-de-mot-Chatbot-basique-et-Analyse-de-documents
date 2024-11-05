import math

def tf_idf_norm(corpus,list_mot):
    """
    Calcule la matrice TF-IDF pour un corpus donné.

    Args:
        corpus (list): La liste des documents.
        list_mot (list): La liste des mots.

    Returns:
        list: La matrice TF-IDF.
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
        mots_document = corpus[i].split()
        longueur_document = len(mots_document)

        for j, mot in enumerate(list_mot):
            # Calculer le nombre d'occurrences du mot dans le document
            nombre_occurrences = mots_document.count(mot)

            # Calculer le terme TF
            tf = nombre_occurrences / longueur_document if longueur_document > 0 else 0

            # Calculer le terme IDF avec vérification pour éviter la division par zéro
            if nombre_documents_mot[j] > 0:
                idf = math.log10(nombre_documents / nombre_documents_mot[j])
            else:
                idf = 0

            # Calculer le terme TF-IDF
            matrix_tf_idf[i][j] = tf * idf

    return matrix_tf_idf