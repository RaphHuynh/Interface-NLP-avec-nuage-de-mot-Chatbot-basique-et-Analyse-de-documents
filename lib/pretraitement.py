from typing import List

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
    """ Sépare un contenu en phrases
    
    Args:
        contenu (str): contenu à traiter
        
    Returns:
        List[str]: liste de phrases 
    """
    phrases = contenu.split('.')
    phrases_temp = []
    for phrase in phrases:
        phrases_temp.extend(phrase.split('!'))
    phrases_finales = []
    for phrase in phrases_temp:
        phrases_finales.extend(phrase.split('?'))
    return [phrase.strip() for phrase in phrases_finales if len(phrase.strip().split()) > 1]