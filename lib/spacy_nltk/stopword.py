from typing import List
import nltk
from nltk.corpus import stopwords

# Download stopwords if not already downloaded
nltk.download('stopwords')

def retirer_stopwords(corpus: List[str], lang: str) -> List[str]:
    """ Retire les stopwords d'une liste de mots
    
    Args:
        corpus (List[str]): liste de mots
        
    Returns:
        List[str]: liste de mots sans stopwords
    """
    if lang == 'Français':
        stop_words = set(stopwords.words('french'))
    else:
        stop_words = set(stopwords.words('english'))
    corpus_sans_stopwords = [mot for mot in corpus if mot not in stop_words]
    return corpus_sans_stopwords