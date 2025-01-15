from lib.pretraitement import retirer_doublons, split_doc_mot
from lib.spacy_nltk.stemming import *
from itertools import chain

def give_liste_mot(corpus_sans_poc, selected_stemming):
    if selected_stemming == "1":
        liste_mots = porter_stemmer(retirer_doublons(split_doc_mot(corpus_sans_poc)))
    elif selected_stemming == "2":
        liste_mots = snowball_stemmer(retirer_doublons(split_doc_mot(corpus_sans_poc)))
    elif selected_stemming == "3":
        liste_mots = lancaster_stemmer(retirer_doublons(split_doc_mot(corpus_sans_poc)))
    elif selected_stemming == "4":
        liste_mots = [wordnet_lemmatizer(phrase.lower()) for phrase in corpus_sans_poc]
        flat_list = list(chain.from_iterable(liste_mots))
        liste_mots = retirer_doublons(flat_list)
    elif selected_stemming == "5":
        liste_mots = [lovins_stemmer(phrase.lower()) for phrase in corpus_sans_poc]
        flat_list = list(chain.from_iterable(liste_mots))
        liste_mots = retirer_doublons(flat_list)
    else:
        liste_mots = retirer_doublons(split_doc_mot(corpus_sans_poc))
    return liste_mots