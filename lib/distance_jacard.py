def distance_jacard(vecteur_1, vecteur_2):
    # Calcul de l'intersection
    intersection = sum(a and b for a, b in zip(vecteur_1, vecteur_2))

    # Calcul de l'union
    union = sum(a or b for a, b in zip(vecteur_1, vecteur_2))

    # Vérifier si l'union est nulle pour éviter la division par zéro
    if union == 0:
        return 0

    # Calcul de la distance de Jaccard
    return 1 - intersection / union

def matrice_distance_jacard(corpus):
    taille = len(corpus)
    matrice = [[0 for _ in range(taille)] for _ in range(taille)]

    for i in range(taille):
        for j in range(taille):
            matrice[i][j] = distance_jacard(corpus[i], corpus[j])

    return matrice
