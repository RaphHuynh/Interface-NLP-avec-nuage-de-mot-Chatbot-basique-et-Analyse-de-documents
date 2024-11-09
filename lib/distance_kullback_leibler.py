import math
from typing import List

def distance_kullback_leibler(vecteur_1: str, vecteur_2:str) -> float:
    """
    Calculate the Kullback-Leibler distance between two vectors.

    Args:
        vecteur_1 (str): vecteur de mots 1
        vecteur_2 (str): vecteur de mots 2

    Returns:
        float: la distance de Kullback-Leibler entre les deux vecteurs
    """
    # Calcul de la somme des logarithmes des ratios
    resultat = sum(a * math.log(a / b) for a, b in zip(vecteur_1, vecteur_2) if a != 0 and b != 0)

    return resultat

def matrice_kullback_leibler(corpus: List[str]) -> List[List[float]]:
    """ Calcul de la matrice de distance de Kullback-Leibler entre les vecteurs de mots de chaque phrase du corpus
    
    Args:
        corpus (List[str]): corpus de phrases
        
    Returns:
        List[List[float]]: matrice de distance de Kullback-Leibler
    """
    taille = len(corpus)
    matrice = [[0 for _ in range(taille)] for _ in range(taille)]

    for i in range(taille):
        for j in range(taille):
            matrice[i][j] = distance_kullback_leibler(corpus[i], corpus[j])

    return matrice