from typing import List

def distance_jacard(vecteur_1: str, vecteur_2: str) -> float:
    """ Calcule la distance de Jaccard entre deux vecteurs de mots
    
    Args:
        vecteur_1 (str): vecteur de mots 1
        vecteur_2 (str): vecteur de mots 2
        
    Returns:
        float: la distance de Jaccard entre les deux vecteurs
    """
    # Calcul de l'intersection
    intersection = sum(a and b for a, b in zip(vecteur_1, vecteur_2))

    # Calcul de l'union
    union = sum(a or b for a, b in zip(vecteur_1, vecteur_2))

    # Vérifier si l'union est nulle pour éviter la division par zéro
    if union == 0:
        return 0

    # Calcul de la distance de Jaccard
    return 1 - intersection / union

def matrice_distance_jacard(corpus: List[str]) -> List[List[float]]:
    """ Calcule la matrice de distance de Jaccard entre les vecteurs de mots de chaque phrase du corpus
    
    Args:
        corpus (List[str]): corpus de phrases
        
    Returns:    
        List[List[float]]: matrice de distance de Jaccard
    """
    taille = len(corpus)
    matrice = [[0 for _ in range(taille)] for _ in range(taille)]

    for i in range(taille):
        for j in range(taille):
            matrice[i][j] = distance_jacard(corpus[i], corpus[j])

    return matrice
