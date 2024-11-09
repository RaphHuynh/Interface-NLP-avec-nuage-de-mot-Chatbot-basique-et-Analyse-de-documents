from typing import List

def distance_manhattan(list_mot_phrase_1: str, list_mot_phrase2: str) -> int:
    """ Calcule la distance de Manhattan entre deux vecteurs de mots
    
    Args:
        list_mot_phrase_1 (str): vecteur de mots de la phrase 1
        list_mot_phrase2 (str): vecteur de mots de la phrase 2
        
    Returns:
        int: la distance de Manhattan entre les deux vecteurs
    """
    somme = 0
    for i in range(len(list_mot_phrase_1)):
        somme += abs(list_mot_phrase_1[i] - list_mot_phrase2[i])
    return somme


def matrix_distance_Manhattan(corpus: List[str]) -> List[List[int]]:
    """ Calcule la matrice de distance de Manhattan entre les vecteurs de mots de chaque phrase du corpus
    
    Args:
        corpus (List[str]): corpus de phrases
        
    Returns:
        List[List[int]]: matrice de distance de Manhattan
    """
    matrix = [[0 for _ in corpus] for _ in corpus]

    for i in range(len(corpus)):
        for j in range(len(corpus)):
            matrix[i][j] = distance_manhattan(corpus[i], corpus[j])
    return matrix