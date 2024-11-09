from typing import List

def distance_hamming(vecteur_1: str, vecteur_2: str) -> int:
    """ Calcule la distance de Hamming entre deux vecteurs de mots
    
    Args:
        vecteur_1 (str): vecteur de mots 1
        vecteur_2 (str): vecteur de mots 2
        
    Returns:
        int: la distance de Hamming entre les deux vecteurs
    """
    # Calcul du nombre de bits différents
    distance = sum(a != b for a, b in zip(vecteur_1, vecteur_2))

    return distance

def matrice_distance_hamming(corpus: List[str]) -> List[List[int]]:
    """ Calcule la matrice de distance de Hamming entre les vecteurs de mots de chaque phrase du corpus
    
    Args:
        corpus (List[str]): corpus de phrases
        
    Returns:
        List[List[int]]: matrice de distance de Hamming
    """
    taille = len(corpus)
    matrice = [[0 for _ in range(taille)] for _ in range(taille)]

    for i in range(taille):
        for j in range(taille):
            matrice[i][j] = distance_hamming(corpus[i], corpus[j])

    return matrice