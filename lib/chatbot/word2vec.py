import re
import gensim
import numpy as np
from typing import List

from gensim.models import Word2Vec

formules_politesse = {
    "comment": "Après analyse, ",
    "pourquoi": "Car, ",
    "peux-tu": "Oui, bien sûr! ",
    "quel": "Voici ce que j'ai trouvé : ",
    "pourrais-tu":"Bien sûr, voici ce que j'ai trouvé : ",
    "dis-moi": "Certainement !",
    "raconte-moi": "D'accord, voici ce que j'ai trouvé : ",
    "quel est": "Voici la réponse : ",
}

def modele_word2vec(corpus: List[List[str]]) -> Word2Vec:
    """
    Créer un modèle Word2Vec à partir d'un corpus de documents tokenizés.
    
    Args:
        corpus (List[List[str]]): Une liste de documents tokenizés.
        
    Returns:
        Word2Vec: Un modèle Word2Vec entraîné sur le corpus.
    """
    modele1 = Word2Vec(vector_size=2, window=5, min_count=1)
   
    modele1.build_vocab(corpus)
   
    modele1.train(corpus, total_examples=modele1.corpus_count, epochs=10)
    
    return modele1
   
def mot_significatif(question: str, corpus: List[List[str]], modele: Word2Vec) -> str:
    """
    retourne le mot le plus significatif dans la question en utilisant Word2Vec.
    
    Args:
        question (str): La question posée par l'utilisateur.
        corpus (List[List[str]]): Une liste de documents tokenizés.
        modele (Word2Vec): Un modèle Word2Vec entraîné sur le corpus.
        
    Returns:
        str: Le mot le plus significatif dans la question.
    
    """
    mots_question = question.split()
    significances = {}
    
    for mot in mots_question:
        if mot in modele.wv.key_to_index.keys():  # Vérifier si le mot est dans le vocabulaire
            # Calculer la norme pour estimer la "signification" du mot dans l'espace
            vector_norm = np.linalg.norm(modele.wv[mot])
            significances[mot] = vector_norm
    
    # Retourner le mot avec la plus grande norme
    return max(significances, key=significances.get) if significances else None

def trouver_phrase(document: str, mot: str) -> str:
    """
    Trouver la phrase contenant le mot spécifié dans le document.
    
    Args:
        document (str): Le document contenant des phrases.
        mot (str): Le mot à rechercher dans le document.
        
    Returns:
        str: La phrase contenant le mot spécifié.
    """
    # Fractionner le texte en phrases
    phrases = re.split(r'[.!?]', document)
    
    for phrase in phrases:
        if mot in phrase:
            return phrase.strip()  # Retourner la phrase nettoyée
    return None

def repondre_a_question(question: str, document: str, corpus: List[List[str]], stemmer: str) -> str:
    """
    Répondre à une question en utilisant Word2Vec pour identifier le mot significatif.
    
    Args:
        question (str): La question posée par l'utilisateur.
        document (str): Le document contenant des phrases.
        corpus (List[List[str]]): Une liste de documents tokenizés.
        
    Returns:
        str: La réponse à la question posée.
    """
    # Préparer le corpus pour Word2Vec
    corpus_tokens = [doc.split() for doc in corpus]
    modele = modele_word2vec(corpus_tokens)
    
    # Identifier le mot significatif
    mot_cle = mot_significatif(question, corpus_tokens, modele)
    if not mot_cle:
        return "Je n'ai pas pu identifier un mot significatif dans votre question."
    
    # Trouver la phrase contenant ce mot
    phrase_reponse = trouver_phrase(document, mot_cle)
    if not phrase_reponse:
        return f"Je n'ai trouvé aucune phrase contenant le mot '{mot_cle}'."
    
    # Ajouter la formule de politesse
    for cle, formule in formules_politesse.items():
        if cle in question.lower():
            return formule + phrase_reponse
    
    # Réponse par défaut
    return phrase_reponse