def affichage_matrix_with_list_words(matrix, list_mot):
    print("Mots:", "\t".join(list_mot))
    for i, row in enumerate(matrix):
        print(f"Phrase {i+1}: ", "\t".join(map(str, row)))


def affichage_matrix_distance(matrix):
    for i, row in enumerate(matrix):
        print(f"Phrase {i+1}: ", "\t".join(map(str, row)))