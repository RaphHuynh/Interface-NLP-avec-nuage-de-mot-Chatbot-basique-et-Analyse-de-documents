def matrice_similarite(corpus, list_mot, distance_func, descripteur_func):
    matrix = [[0 for _ in corpus] for _ in corpus]

    for i in range(len(corpus)):
        for j in range(len(corpus)):
            matrix[i][j] = distance_func(descripteur_func([corpus[i]], list_mot)[0],
                                         descripteur_func([corpus[j]], list_mot)[0])

    return matrix
