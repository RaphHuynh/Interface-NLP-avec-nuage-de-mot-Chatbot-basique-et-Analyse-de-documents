import math
from .backofword_occurence import backbofwords_occurence

def matrix_backbofwords_normalize_proba(corpus_sans_poc, liste_mots):
    matrix = backbofwords_occurence(corpus_sans_poc, liste_mots)
    matrix_normalize = [[0 for _ in matrix[0]] for _ in matrix]

    for i in range(len(matrix)):
        somme = sum(matrix[i])
        if somme == 0:
            somme = 1e-10
        for j in range(len(matrix[i])):
            matrix_normalize[i][j] = matrix[i][j] / somme

    return matrix_normalize


def matrix_backbofwords_normalize_Norme(corpus_sans_poc, liste_mots):
    matrix = backbofwords_occurence(corpus_sans_poc, liste_mots)
    matrix_normalize = [[0 for _ in matrix[0]] for _ in matrix]

    for i in range(len(matrix)):
        somme = math.sqrt(sum([x ** 2 for x in matrix[i]]))
        if somme == 0:
            somme = 0e-10
        for j in range(len(matrix[i])):
            matrix_normalize[i][j] = matrix[i][j] / somme

    return matrix_normalize