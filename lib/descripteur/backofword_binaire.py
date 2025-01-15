from typing import List

from lib.descripteur.utils import appliquer_stemming
from lib.spacy_nltk.stemming import *

def backbofwordsBinaire(list_phrase: List[str], list_mot: List[str], stemming: str, stopword:str) -> List[List[int]]:
    """ bag of words binaire

    Args:
        list_phrase (List[str]): liste des phrases
        list_mot (List[str]): liste des mots

    Returns:
        List[List[int]]: liste des vecteurs de back of words
    """
    list_backbofwords = [[0 for _ in list_mot] for _ in list_phrase]
    list_phrases = []
    list_mots = [mot.lower() for mot in list_mot]

    for i in range(len(list_phrases)):
        list_mot_phrase = appliquer_stemming(list_phrases[i], stemming)
        print(list_mot_phrase)
        for j,mot in enumerate(list_mot_phrase):
            if mot in list_mots:
                list_backbofwords[i][j] = 1
            else:
                list_backbofwords[i][j] = 0

    return list_backbofwords