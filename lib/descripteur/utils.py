# Fonction de stemming en fonction de l'option
from typing import List
from lib.spacy_nltk.stemming import *
import os
import nltk
from nltk.corpus import stopwords as nltk_stopwords

nltk.download('stopwords')


def appliquer_stemming(phrase: str, stemming: str) -> List[str]:
    """
    Appliquer le stemming à une phrase en fonction de l'option choisie.
    
    Args:
        phrase (str): La phrase à traiter.
        stemming (str): L'option pour choisir le stemming.
        
    Returns:
        List[str]: La liste des mots après application du stemming.
    
    """
    phrase = phrase.lower()

    if stemming == "1":
        return porter_stemmer_phrase(phrase)
    elif stemming == "2":
        return snowball_stemmer_phrase(phrase)
    elif stemming == "3":
        return lancaster_stemmer_phrase(phrase)
    elif stemming == "4":
        return wordnet_lemmatizer_phrase(phrase)
    elif stemming == "5":
        return lovins_stemmer(phrase)
    else:
        # Pas de stemming appliqué, on garde les mots d'origine
        return phrase.split()