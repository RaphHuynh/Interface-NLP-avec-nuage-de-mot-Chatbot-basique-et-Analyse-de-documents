import math
from typing import List

def similarite_cosinus(vecteur_1: str, vecteur_2: str) -> float:
    """Calcul de la similarité cosinus entre deux vecteurs.
    
    Args:
        vecteur_1 (str): premier vecteur
        vecteur_2 (str): deuxième vecteur
        
    Returns:
        float: similarité cosinus
    """
    # Calcul du produit scalaire
    produit_scalaire = sum(a * b for a, b in zip(vecteur_1, vecteur_2))

    # Calcul des normes
    norme_vecteur_1 = math.sqrt(sum(a ** 2 for a in vecteur_1))
    norme_vecteur_2 = math.sqrt(sum(b ** 2 for b in vecteur_2))

    # Vérifier si les normes sont différentes de zéro pour éviter la division par zéro
    if norme_vecteur_1 == 0 or norme_vecteur_2 == 0:
        return 0

    # Calcul de la similarité cosinus
    similarite = produit_scalaire / (norme_vecteur_1 * norme_vecteur_2)

    return similarite

def distance_cosinus(vecteur_1: str, vecteur_2: str) -> float:
    """Calcul de la distance cosinus entre deux vecteurs.
    
    Args:
        vecteur_1 (str): premier vecteur
        vecteur_2 (str): deuxième vecteur
        
    Returns:
        float: distance cosinus
    """
    # Calcul de la similarité cosinus
    similarite = similarite_cosinus(vecteur_1, vecteur_2)

    # Calcul de la distance cosinus
    return 1 - similarite

def matrice_distance_cosinus(corpus: List[str]) -> List[List[float]]:
    """Calcul de la matrice de distance cosinus.
    
    Args:
        corpus (List[str]): liste des vecteurs
        
    Returns:
        List[List[float]]: matrice de distance cosinus
    """
    taille = len(corpus)
    matrice = [[0 for _ in range(taille)] for _ in range(taille)]

    for i in range(taille):
        for j in range(taille):
            matrice[i][j] = distance_cosinus(corpus[i], corpus[j])

    return matrice