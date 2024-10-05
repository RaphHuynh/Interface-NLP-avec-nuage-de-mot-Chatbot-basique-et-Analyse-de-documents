def K_plus_proches_documents(doc_requete, k, corpus, matrice_distance):
    # Obtenir l'indice du document de requête dans le corpus
    index_doc_requete = corpus.index(doc_requete)

    # Initialiser une liste pour stocker les documents similaires et leurs distances
    documents_similaires = []

    # Parcourir la ligne de la matrice de distance correspondant au document de requête
    for i, distance in enumerate(matrice_distance[index_doc_requete]):
        # Ne pas inclure le document de requête lui-même
        if i != index_doc_requete:
            documents_similaires.append((corpus[i], distance))

    # Trier les documents par distance croissante (les plus proches d'abord)
    documents_similaires.sort(key=lambda x: x[1])

    # Retourner les k documents les plus proches
    return documents_similaires[:k]