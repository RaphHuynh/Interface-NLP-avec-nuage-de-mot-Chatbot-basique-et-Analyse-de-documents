from typing import List

from lib.spacy_nltk.stemming import *

def backbofwordsBinaire(list_phrase: List[str], list_mot: List[str], stemming: str) -> List[List[int]]:
    """ bag of words binaire

    Args:
        list_phrase (List[str]): liste des phrases
        list_mot (List[str]): liste des mots

    Returns:
        List[List[int]]: liste des vecteurs de back of words
    """
    if stemming == "6":
        list_backbofwords = [[0 for _ in list_mot] for _ in list_phrase]
        list_phrases = []
        for phrase in list_phrase:
            list_phrases.append(phrase.lower())
        list_mots = [mot.lower() for mot in list_mot]

        for indice in range(len(list_phrases)):
            for mot in list_phrases[indice].split():
                if mot in list_mots:
                    list_backbofwords[indice][list_mots.index(mot)] = 1
                else:
                    list_backbofwords[indice][list_mots.index(mot)] = 0

        return list_backbofwords
    else:
        if stemming == "1":
            list_backbofwords = [[0 for _ in list_mot] for _ in list_phrase]
            list_phrases = []
            for phrase in list_phrase:
                list_phrases.append(phrase.lower())

            for indice in range(len(list_phrases)):
                list_mot_phrase = porter_stemmer_phrase(list_phrases[indice])
                for mot in list_mot_phrase:
                    if mot in list_mot:
                        list_backbofwords[indice][list_mot.index(mot)] = 1
                    else:
                        list_backbofwords[indice][list_mot.index(mot)] = 0

            return list_backbofwords
        elif stemming == "2":
            list_backbofwords = [[0 for _ in list_mot] for _ in list_phrase]
            list_phrases = []
            for phrase in list_phrase:
                list_phrases.append(phrase.lower())

            for indice in range(len(list_phrases)):
                list_mot_phrase = snowball_stemmer_phrase(list_phrases[indice])
                for mot in list_mot_phrase:
                    if mot in list_mot:
                        list_backbofwords[indice][list_mot.index(mot)] = 1
                    else:
                        list_backbofwords[indice][list_mot.index(mot)] = 0

            return list_backbofwords
        elif stemming == "3":
            list_backbofwords = [[0 for _ in list_mot] for _ in list_phrase]
            list_phrases = []
            for phrase in list_phrase:
                list_phrases.append(phrase.lower())

            for indice in range(len(list_phrases)):
                list_mot_phrase = lancaster_stemmer_phrase(list_phrases[indice])
                for mot in list_mot_phrase:
                    if mot in list_mot:
                        list_backbofwords[indice][list_mot.index(mot)] = 1
                    else:
                        list_backbofwords[indice][list_mot.index(mot)] = 0

            return list_backbofwords
        elif stemming == "4":
            list_backbofwords = [[0 for _ in list_mot] for _ in list_phrase]
            list_phrases = []
            for phrase in list_phrase:
                list_phrases.append(phrase.lower())

            for indice in range(len(list_phrases)):
                list_mot_phrase = wordnet_lemmatizer_phrase(list_phrases[indice])
                for mot in list_mot_phrase:
                    if mot in list_mot:
                        list_backbofwords[indice][list_mot.index(mot)] = 1
                    else:
                        list_backbofwords[indice][list_mot.index(mot)] = 0

            return list_backbofwords
        elif stemming == "5":
            list_backbofwords = [[0 for _ in list_mot] for _ in list_phrase]
            list_phrases = []
            for phrase in list_phrase:
                list_phrases.append(phrase.lower())

            for indice in range(len(list_phrases)):
                list_mot_phrase = lovins_stemmer(list_phrases[indice])
                print(list_mot_phrase)
                for mot in list_mot_phrase:
                    if mot in list_mot:
                        list_backbofwords[indice][list_mot.index(mot)] = 1
                    else:
                        list_backbofwords[indice][list_mot.index(mot)] = 0

            return list_backbofwords