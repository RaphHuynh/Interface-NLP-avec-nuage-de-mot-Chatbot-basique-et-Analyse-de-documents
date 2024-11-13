import spacy
from typing import List

nlp = spacy.load('en_core_web_sm')

def steamming(corpus: List[str]) -> List[str]:
    """ steamming function to steamming the words in the corpus using spacy

    Args:
        corpus (List[str]): list of strings to steamming the words in it

    Returns:
        List[str]: list of strings after steamming the words in the corpus
    """
    return [token.lemma_ for token in nlp(corpus)]