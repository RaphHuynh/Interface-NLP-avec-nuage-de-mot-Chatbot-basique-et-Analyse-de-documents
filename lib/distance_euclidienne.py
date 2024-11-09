import math
from typing import List

def distance_euclidienne(list_mot_phrase_1: str, list_mot_phrase2: str) -> float:
    """ Calcule la distance euclidienne entre deux vecteurs de mots
    
    Args:
        list_mot_phrase_1 (List[int]): vecteur de mots de la phrase 1
        list_mot_phrase2 (List[int]): vecteur de mots de la phrase 2
        
    Returns:
        float: la distance euclidienne entre les deux vecteurs
    """
    somme = 0
    for i in range(len(list_mot_phrase_1)):
        somme += (list_mot_phrase_1[i] - list_mot_phrase2[i]) ** 2
    return math.sqrt(somme)


def matrix_distance_Euclidienne(corpus: List[str]) -> List[List[float]]:
    """ Calcule la matrice de distance euclidienne entre les vecteurs de mots de chaque phrase du corpus
    
    Args:
        corpus (List[str]): corpus de phrases
        
    Returns:
        List[List[float]]: matrice de distance euclidienne
    """
    matrix = [[0 for _ in corpus] for _ in corpus]

    for i in range(len(corpus)):
        for j in range(len(corpus)):
            matrix[i][j] = distance_euclidienne(corpus[i], corpus[j])

    return matrix