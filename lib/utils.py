import os
from lib import *

def stopwords(corpus, list_mot, nom_stop_words):
    base_dir = os.path.dirname(__file__)  # Obtient le répertoire du fichier utils.py
    if nom_stop_words == "en_short":
        path = os.path.join(base_dir, "stopwords/en_short.txt")
    elif nom_stop_words == "English":
        path = os.path.join(base_dir, "stopwords/en.txt")
    else:   
        path = os.path.join(base_dir, "stopwords/fr.txt")
        
    with open(path, "r") as fichier:
        mots_vides = fichier.read().split("\n")
            
    mots_vides = [mot.lower() for mot in mots_vides]
    
    list_mot_stopwords = [mot.lower() for mot in list_mot if mot.lower() not in mots_vides]
    corpus_lower = [doc.lower() for doc in corpus]
    corpus_stopwords = [" ".join([mot for mot in doc.split() if mot not in mots_vides]) for doc in corpus_lower]
    
    return corpus_stopwords, list_mot_stopwords

def get_backbofwords(corpus_sans_poc, liste_mots, choix1):
    if choix1 == "1":
        return backbofwordsBinaire(corpus_sans_poc, liste_mots)
    elif choix1 == "2":
        return backbofwords_occurence(corpus_sans_poc, liste_mots)
    elif choix1 == "3":
        return matrix_backbofwords_normalize_Norme(corpus_sans_poc, liste_mots)
    elif choix1 == "4":
        return matrix_backbofwords_normalize_proba(corpus_sans_poc, liste_mots)
    elif choix1 == "5":
        return tf_idf_bin(corpus_sans_poc, liste_mots)
    elif choix1 == "6":
        return tf_idf_norm(corpus_sans_poc, liste_mots)
    elif choix1 == "7":
        return tf_idf_occ(corpus_sans_poc, liste_mots)
    else:
        return tf_idf_new(corpus_sans_poc, liste_mots)

def get_distance_matrix(list_backbofwords, distance):
    if distance == "Euclidienne":
        return matrix_distance_Euclidienne(list_backbofwords)
    elif distance == "Cosinus":
        return matrice_distance_cosinus(list_backbofwords)
    elif distance == "Curtis":
        return matrice_distance_bray_curtis(list_backbofwords)
    elif distance == "Kullback":
        return matrice_kullback_leibler(list_backbofwords)
    elif distance == "Jacard":
        return matrice_distance_jacard(list_backbofwords)
    elif distance == "Hamming":
        return matrice_distance_hamming(list_backbofwords)
    else:
        return matrix_distance_Manhattan(list_backbofwords)

def get_k_nearest_phrases(corpus_sans_poc, selected_phrase_index, k, distance_matrix):
    if selected_phrase_index is not None:
        selected_phrase = corpus_sans_poc[selected_phrase_index]
        k_nearest = K_plus_proches_documents(selected_phrase, k, corpus_sans_poc, distance_matrix)
        return [f"• {phrase}: {distance}" for phrase, distance in k_nearest]
    else:
        return []
    
def style_dataframe(df):
    return df.style.set_table_attributes('class="table-auto w-full border-collapse border border-gray-200"').format("{:.3f}").background_gradient(cmap='viridis', low=0, high=1).set_properties(**{
            'white-space': 'nowrap',
            'font-size': '14px',
            'text-align': 'center',
        })
        
def descriptor_select_distance(choix):
    if choix == "1":
        return ["Euclidienne", "Manhattan", "Cosinus", "Curtis", "Kullback", "Jacard", "Hamming"]
    else:
        return ["Euclidienne", "Manhattan", "Cosinus", "Curtis", "Kullback"]