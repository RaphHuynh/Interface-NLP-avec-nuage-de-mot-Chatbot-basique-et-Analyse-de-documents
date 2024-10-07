def distance_bray_curtis(vecteur_1, vecteur_2):
    # Calcul de la somme des différences absolues
    somme_diff_absolue = sum(abs(a - b) for a, b in zip(vecteur_1, vecteur_2))

    # Calcul de la somme des valeurs absolues
    somme_valeurs_absolues = sum(abs(a) + abs(b) for a, b in zip(vecteur_1, vecteur_2))

    # Vérifier si la somme des valeurs absolues est nulle pour éviter la division par zéro
    if somme_valeurs_absolues == 0:
        return 0

    # Calcul de la distance de Bray-Curtis
    return somme_diff_absolue / somme_valeurs_absolues

def matrice_distance_bray_curtis(corpus):
    taille = len(corpus)
    matrice = [[0 for _ in range(taille)] for _ in range(taille)]

    for i in range(taille):
        for j in range(taille):
            matrice[i][j] = distance_bray_curtis(corpus[i], corpus[j])

    return matrice