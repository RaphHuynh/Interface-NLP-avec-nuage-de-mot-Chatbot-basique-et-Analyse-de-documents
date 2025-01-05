from typing import List
import spacy
import re


def retirer_ponctuation(doc: str) -> str:
    """ Retire la ponctuation d'un document
    
    Args:
        doc (str): document à traiter
        
    Returns:
        str: document sans ponctuation
    """
    ponctuations = ['.', ',', '!', '?', ':', ';', '(', ')', '-', '_', '"', "'", '...', '—', '/',"'", '’', '‘', '“', '”', '«', '»', '–','…']
    for ponctuation in ponctuations:
        doc = doc.replace(ponctuation, ' ')
    return doc


def supp_poc_corpus(corpus: List[str]) -> List[str]:
    """ Supprime la ponctuation d'un corpus de documents et retourne le corpus sans ponctuation
    
    Args:
        corpus (List[str]): corpus de documents
    
    Returns:
        List[str]: corpus de documents sans ponctuation
    """
    corpus_sans_poc = []
    for doc in corpus:
        doc_sans_poc = retirer_ponctuation(doc)
        corpus_sans_poc.append(doc_sans_poc)
    return corpus_sans_poc


def split_phrase_mot(corpus: str) -> List[str]:
    """ Sépare un corpus en phrases et les phrases en mots
    
    Args:
        corpus (str): corpus à traiter
        
    Returns:
        List[str]: liste de mots
    """
    phrases = corpus.split('.')
    liste_mots = []

    for phrase in phrases:
        phrase = phrase.strip()
        if phrase:
            mots = phrase.split()
            liste_mots.extend(mots)

    return liste_mots


def split_doc_mot(corpus: List[str]) -> List[str]:
    """ Créer la liste de mots d'un corpus
    
    Args:
        corpus (List[str]): corpus à traiter
        
    Returns:
        List[str]: liste de mots 
    """
    liste_mots_totale = []

    for doc in corpus:
        mots = split_phrase_mot(doc)
        liste_mots_totale.extend(mots)

    return liste_mots_totale


def retirer_doublons(corpus: List[str]) -> List[str]:
    """ Retire les doublons d'une liste de mots
    
    Args:
        corpus (List[str]): liste de mots
        
    Returns:
        List[str]: liste de mots sans doublons
    """
    vus = set()
    liste_sans_doublons = []
    for mot in corpus:
        mot_lower = mot.lower()
        if mot_lower not in vus:
            liste_sans_doublons.append(mot_lower)
            vus.add(mot_lower)

    return liste_sans_doublons

def separer_phrase(contenu: str) -> List[str]:
    """Sépare un contenu en phrases sans séparer les abréviations courantes,
    tout en reconnaissant des sous-phrases introduites par un motif spécifique
    comme 'bla: Yes, we can.'.
    
    Args:
        contenu (str): contenu à traiter
        
    Returns:
        List[str]: liste de phrases 
    """
    # Liste des abréviations courantes à préserver
    abrev = ['Mr.', 'Mme.', 'Dr.', 'Prof.', 'Sr.', 'Jr.', 'Sen.', 'Pres.', 
             'Gen.', 'Rep.', 'St.', 'Mlle.', 'Gov.']
    
    # Protéger temporairement les abréviations
    for ab in abrev:
        contenu = contenu.replace(ab, ab.replace('.', '###'))
    
    # Gérer le cas spécifique: "mot: Mot, mot mot."
    # On remplace ce motif par deux phrases séparées
    contenu = re.sub(
        r'(\b\w+\b):\s([A-Z][a-z]+,\s[a-z]+\s[a-z]+)\.',  # Motif regex
        r'\1. \2.',  # Remplacement : sépare les deux phrases
        contenu
    )
    
    # Découper par les principaux délimiteurs de fin de phrase
    phrases = re.split(r'[.!?]', contenu)
    
    # Nettoyer les sous-phrases et gérer les espaces
    phrases = [phrase.strip() for phrase in phrases if phrase.strip()]
    
    # Rétablir les abréviations
    for i in range(len(phrases)):
        for ab in abrev:
            phrases[i] = phrases[i].replace(ab.replace('.', '###'), ab)
    
    return phrases

def separer_phrase_spacy(contenu: str, lang: str) -> List[str]:
    """ Sépare un contenu en phrases sans séparer les abréviations courantes
    
    Args:
        contenu (str): contenu à traiter
        
    Returns:
        List[str]: liste de phrases 
    """
    if lang == 'Français':
        nlp = spacy.load("fr_core_news_sm")
    else:
        nlp = spacy.load("en_core_web_sm")
    doc = nlp(contenu)
    phrases = [sent.text for sent in doc.sents]
    return phrases  