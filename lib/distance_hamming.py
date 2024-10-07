def distance_hamming(vecteur_1, vecteur_2):
    # Calcul du nombre de bits différents
    distance = sum(a != b for a, b in zip(vecteur_1, vecteur_2))

    return distance

def matrice_distance_hamming(corpus):
    taille = len(corpus)
    matrice = [[0 for _ in range(taille)] for _ in range(taille)]

    for i in range(taille):
        for j in range(taille):
            matrice[i][j] = distance_hamming(corpus[i], corpus[j])

    return matrice