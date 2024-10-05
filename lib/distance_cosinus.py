import math

def distance_cosinus(list_mot_phrase_1, list_mot_phrase_2):
    # Calcul du produit scalaire
    produit_scalaire = sum(a * b for a, b in zip(list_mot_phrase_1, list_mot_phrase_2))

    # Calcul des normes
    norme_phrase_1 = math.sqrt(sum(a ** 2 for a in list_mot_phrase_1))
    norme_phrase_2 = math.sqrt(sum(b ** 2 for b in list_mot_phrase_2))

    # Calcul et retour de la distance cosinus
    if norme_phrase_1 == 0 or norme_phrase_2 == 0:
        return 0  # Évite la division par zéro
    else:
        return produit_scalaire / (norme_phrase_1 * norme_phrase_2)


def matrix_distance_Cosinus(corpus):
    matrix = [[0 for _ in corpus] for _ in corpus]

    for i in range(len(corpus)):
        for j in range(len(corpus)):
            matrix[i][j] = distance_cosinus(corpus[i], corpus[j])

    return matrix