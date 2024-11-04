import os

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