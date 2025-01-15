from typing import List

from lib.descripteur.utils import appliquer_stemming
from lib.spacy_nltk.stemming import *

def backbofwordsBinaire(list_phrase: List[str], list_mot: List[str], stemming: str, stopword: str) -> List[List[int]]:
    """ bag of words binaire

    Args:
        list_phrase (List[str]): liste des phrases
        list_mot (List[str]): liste des mots

    Returns:
        List[List[int]]: liste des vecteurs de back of words
    """
    list_backbofwords = [[0 for _ in list_mot] for _ in list_phrase]
    list_mots = [mot.lower() for mot in list_mot]
    list_phrases = [phrase.lower() for phrase in list_phrase]
    list_mot_phrase = []

    for i in range(len(list_phrase)):
        list_mot_phrase = appliquer_stemming(list_phrases[i], stemming)
        for j, mot in enumerate(list_mots):
            list_backbofwords[i][j] = 0
            for mot_phrase in list_mot_phrase:
                if mot_phrase == mot:
                    list_backbofwords[i][j] = 1
                    
    return list_backbofwords