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


def retirer_ponctuation_spacy(doc: str) -> str:
    """
    Retire la ponctuation d'un document en utilisant SpaCy.

    Args:
        doc (str): Document à traiter.

    Returns:
        str: Document sans ponctuation.
    """
    langue = detecter_langue(doc)
    nlp = get_nlp_model(langue)
    doc_spacy = nlp(doc)
    return " ".join([token.text for token in doc_spacy if not token.is_punct])


def supp_poc_corpus_spacy(corpus: List[str]) -> List[str]:
    """
    Supprime la ponctuation d'un corpus de documents et retourne le corpus sans ponctuation.

    Args:
        corpus (List[str]): Corpus de documents.

    Returns:
        List[str]: Corpus de documents sans ponctuation.
    """
    return [retirer_ponctuation_spacy(doc) for doc in corpus]


def split_phrase_mot_spacy(corpus: str) -> List[str]:
    """
    Sépare un document en phrases et les phrases en mots.

    Args:
        corpus (str): Document à traiter.

    Returns:
        List[str]: Liste des mots.
    """
    langue = detecter_langue(corpus)
    nlp = get_nlp_model(langue)
    doc_spacy = nlp(corpus)
    return [token.text for token in doc_spacy if not token.is_punct and not token.is_space]


def split_doc_mot_spacy(corpus: List[str]) -> List[str]:
    """
    Crée une liste de mots à partir d'un corpus.

    Args:
        corpus (List[str]): Corpus de documents.

    Returns:
        List[str]: Liste de mots.
    """
    liste_mots_totale = []
    for doc in corpus:
        mots = split_phrase_mot_spacy(doc)
        liste_mots_totale.extend(mots)
    return liste_mots_totale


def retirer_doublons_spacy(corpus: List[str]) -> List[str]:
    """
    Retire les doublons d'une liste de mots en ignorant la casse.

    Args:
        corpus (List[str]): Liste de mots.

    Returns:
        List[str]: Liste de mots sans doublons.
    """
    vus = set()
    liste_sans_doublons = []
    for mot in corpus:
        mot_lower = mot.lower()
        if mot_lower not in vus:
            liste_sans_doublons.append(mot_lower)
            vus.add(mot_lower)
    return liste_sans_doublons


def separer_phrase_spacy(contenu: str) -> List[str]:
    """
    Sépare un contenu en phrases en utilisant SpaCy.

    Args:
        contenu (str): Contenu à traiter.

    Returns:
        List[str]: Liste de phrases.
    """
    langue = detecter_langue(contenu)
    nlp = get_nlp_model(langue)
    doc_spacy = nlp(contenu)
    return [sent.text.strip() for sent in doc_spacy.sents if len(sent.text.split()) > 1]