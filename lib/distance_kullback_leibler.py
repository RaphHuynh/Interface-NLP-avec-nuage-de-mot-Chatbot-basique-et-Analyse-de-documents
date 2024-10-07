def distance_kullback_leibler(vecteur_1, vecteur_2):
    """
    Calculate the Kullback-Leibler distance between two vectors.

    Args:
        vecteur_1 (list): The first vector.
        vecteur_2 (list): The second vector.

    Returns:
        float: The Kullback-Leibler distance.
    """
    # Calcul de la somme des logarithmes des ratios
    resultat = sum(a * math.log(a / b) for a, b in zip(vecteur_1, vecteur_2) if a != 0 and b != 0)

    return resultat

def matrice_kullback_leibler(corpus):
    """
    Calcule la matrice de distance de Kullback-Leibler pour un corpus donné.
    """
    taille = len(corpus)
    matrice = [[0 for _ in range(taille)] for _ in range(taille)]

    for i in range(taille):
        for j in range(taille):
            matrice[i][j] = distance_kullback_leibler(corpus[i], corpus[j])

    return matrice