import math

def matrix_backbofwords_normalize_proba(matrix):
    matrix_normalize = [[0 for _ in matrix[0]] for _ in matrix]

    for i in range(len(matrix)):
        somme = sum(matrix[i])
        for j in range(len(matrix[i])):
            matrix_normalize[i][j] = matrix[i][j] / somme

    return matrix_normalize


def matrix_backbofwords_normalize_Norme(matrix):
    matrix_normalize = [[0 for _ in matrix[0]] for _ in matrix]

    for i in range(len(matrix)):
        somme = math.sqrt(sum([x ** 2 for x in matrix[i]]))
        for j in range(len(matrix[i])):
            matrix_normalize[i][j] = matrix[i][j] / somme

    return matrix_normalize