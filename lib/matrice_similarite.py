from lib import *

def matrice_similarite(corpus, list_mot, distance_func, descripteur_func):
    matrix = [[0 for _ in corpus] for _ in corpus]

    if descripteur_func == "1":
        descripteur_func = backbofwordsBinaire
    elif descripteur_func == "2":
        descripteur_func = backbofwords_occurence
    elif descripteur_func == "3":
        descripteur_func = matrix_backbofwords_normalize_Norme
    elif descripteur_func == "4":
        descripteur_func = matrix_backbofwords_normalize_proba
    elif descripteur_func == "5":
        descripteur_func = tf_idf_bin
    elif descripteur_func == "6":
        descripteur_func = tf_idf_norm
    elif descripteur_func == "7":
        descripteur_func = tf_idf_occ
    else:
        descripteur_func = tf_idf_new
        
    if distance_func == "Euclidienne":
        distance_func = distance_euclidienne
    elif distance_func == "Cosinus":
        distance_func = distance_cosinus
    elif distance_func == "Curtis":
        distance_func = distance_bray_curtis
    elif distance_func == "Kullback":
        distance_func = distance_kullback_leibler
    elif distance_func == "Jacard":
        distance_func = distance_jacard
    elif distance_func == "Hamming":
        distance_func = distance_hamming
    else:
        distance_func = distance_manhattan

    for i in range(len(corpus)):
        for j in range(len(corpus)):
            matrix[i][j] = distance_func(descripteur_func([corpus[i]], list_mot)[0],
                                         descripteur_func([corpus[j]], list_mot)[0])

    return matrix
