import math
from .descripteur.backofword_occurence import backbofwords_occurence
from typing import List

def matrix_backbofwords_normalize_proba(corpus_sans_poc: List[str], liste_mots: List[str]) -> List[List[float]]:
    """ Calcule la matrice de backbofwords normalisée par probabilité
    
    Args:
        corpus_sans_poc (List[str]): corpus de phrases sans les mots de peu d'importance
        liste_mots (List[str]): liste de mots
        
    Returns:
        List[List[float]]: matrice de backbofwords normalisée par probabilité
    """
    matrix = backbofwords_occurence(corpus_sans_poc, liste_mots)
    matrix_normalize = [[0 for _ in matrix[0]] for _ in matrix]

    for i in range(len(matrix)):
        somme = sum(matrix[i])
        for j in range(len(matrix[i])):
            if somme == 0:
                matrix_normalize[i][j] = 0
            else:
                matrix_normalize[i][j] = matrix[i][j] / somme

    return matrix_normalize


def matrix_backbofwords_normalize_Norme(corpus_sans_poc: List[str], liste_mots: List[str]) -> List[List[float]]:
    """ Calcule la matrice de backbofwords normalisée par norme
    
    Args:
        corpus_sans_poc (List[str]): corpus de phrases sans les mots de peu d'importance
        liste_mots (List[str]): liste de mots
        
    Returns:
        List[List[float]]: matrice de backbofwords normalisée par norme
    """
    matrix = backbofwords_occurence(corpus_sans_poc, liste_mots)
    matrix_normalize = [[0 for _ in matrix[0]] for _ in matrix]

    for i in range(len(matrix)):
        somme = math.sqrt(sum([x ** 2 for x in matrix[i]]))
        for j in range(len(matrix[i])):
            if somme == 0:
                matrix_normalize[i][j] = 0
            else:
                matrix_normalize[i][j] = matrix[i][j] / somme

    return matrix_normalize