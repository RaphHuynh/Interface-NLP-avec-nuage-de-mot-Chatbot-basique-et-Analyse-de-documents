import string
import spacy
from typing import List

# Charger les modèles SpaCy en français et en anglais
nlp_fr = spacy.load("fr_core_news_sm")
nlp_en = spacy.load("en_core_web_sm")


def detecter_langue(texte: str) -> str:
    """
    Détecte la langue d'un texte en fonction du nombre de tokens reconnus par SpaCy.

    Args:
        texte (str): Texte à analyser.

    Returns:
        str: Langue détectée ('fr' pour français, 'en' pour anglais).
    """
    tokens_fr = len(list(nlp_fr(texte)))
    tokens_en = len(list(nlp_en(texte)))
    return 'fr' if tokens_fr > tokens_en else 'en'


def get_nlp_model(langue: str):
    """
    Retourne le modèle SpaCy correspondant à la langue.

    Args:
        langue (str): Langue ('fr' ou 'en').

    Returns:
        spacy.language.Language: Modèle SpaCy correspondant.
    """
    return nlp_fr if langue == 'fr' else nlp_en


def diviser_texte_phrase_spacy(texte: str) -> List[str]:
    """
    Divise un texte en phrases en utilisant SpaCy.

    Args:
        texte (str): Texte à diviser.

    Returns:
        List[str]: Liste des phrases.
    """
    nlp = get_nlp_model(detecter_langue(texte))
    doc = nlp(texte)
    return [phrase.text for phrase in doc.sents]

def get_tokens(textes: List[str]) -> List[str]:
    """
    Tokenise une liste de textes en utilisant SpaCy.

    Args:
        textes (List[str]): Liste de textes à tokeniser.

    Returns:
        List[str]: Liste des tokens.
    """
    tokens = []
    for texte in textes:
        nlp = get_nlp_model(detecter_langue(texte))
        doc = nlp(texte)
        tokens.extend(
            t.text.lower().strip() for t in doc
            if t.text not in string.punctuation and t.text not in [' ', '...']
        )
    return tokens