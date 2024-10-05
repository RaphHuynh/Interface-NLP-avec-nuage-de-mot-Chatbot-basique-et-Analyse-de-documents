import math


def distance_euclidienne(list_mot_phrase_1, list_mot_phrase2):
    somme = 0
    for i in range(len(list_mot_phrase_1)):
        somme += (list_mot_phrase_1[i] - list_mot_phrase2[i]) ** 2
    return math.sqrt(somme)


def matrix_distance_Euclidienne(corpus):
    matrix = [[0 for _ in corpus] for _ in corpus]

    for i in range(len(corpus)):
        for j in range(len(corpus)):
            matrix[i][j] = distance_euclidienne(corpus[i], corpus[j])

    return matrix