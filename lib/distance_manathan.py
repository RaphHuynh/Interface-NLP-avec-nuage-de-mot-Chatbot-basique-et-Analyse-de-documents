def distance_manhattan(list_mot_phrase_1, list_mot_phrase2):
    somme = 0
    for i in range(len(list_mot_phrase_1)):
        somme += abs(list_mot_phrase_1[i] - list_mot_phrase2[i])
    return somme


def matrix_distance_Manhattan(corpus):
    matrix = [[0 for _ in corpus] for _ in corpus]

    for i in range(len(corpus)):
        for j in range(len(corpus)):
            matrix[i][j] = distance_manhattan(corpus[i], corpus[j])
    return matrix