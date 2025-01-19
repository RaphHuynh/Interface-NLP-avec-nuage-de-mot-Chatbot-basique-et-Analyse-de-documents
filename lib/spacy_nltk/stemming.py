import nltk
from nltk.stem import PorterStemmer, LancasterStemmer, SnowballStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
from stemming.lovins import stem as LovinsStemmer
from typing import List

# Ensure you have the necessary NLTK data files
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')

def porter_stemmer(list_words: List[str]) -> List[str]:
    """
    Applique porter stemmer à une liste de mot.
    
    Args:
        list_words (List[str]): List of words to stem.
        
    Returns:
        List[str]: List of stemmed words.
    """
    stemmer = PorterStemmer()
    return [stemmer.stem(word) for word in list_words]

def porter_stemmer_phrase(phrase: str) -> List[str]:
    """
    Applique porter stemmer à une phrase.
    
    Args:
        phrase (str): The phrase to stem.
        
    Returns:
        List[str]: List of stemmed words
    """
    stemmer = PorterStemmer()
    words = word_tokenize(phrase)
    return [stemmer.stem(word) for word in words if word.isalnum()]

def lancaster_stemmer(list_words: List[str]) -> List[str]:
    """
    Applique le Lancaster stemmer à une liste de mots.
    
    Args:
        list_words (List[str]): List of words to stem.
        
    Returns:
        List[str]: List of stemmed words.
    """
    stemmer = LancasterStemmer()
    return [stemmer.stem(word) for word in list_words]

def lancaster_stemmer_phrase(phrase: str) -> List[str]:
    """
    Applique le Lancaster stemmer à une phrase.
    
    Args:
        phrase (str): The phrase to stem.
        
    Returns:
        List[str]: List of stemmed words.
    """
    stemmer = LancasterStemmer()
    words = word_tokenize(phrase)
    return [stemmer.stem(word) for word in words if word.isalpha()]

def snowball_stemmer(text: List[str], language:str='english') -> List[str]: 
    """
    Applique le Snowball stemmer à un texte.
    
    Args:
        text (List[str]): The text to stem.
        language (str): The language to use for stemming.
        
    Returns:
        List[str]: List of stemmed words.
    """
    stemmer = SnowballStemmer(language)
    return [stemmer.stem(word) for word in text]

def snowball_stemmer_phrase(phrase: str, language: str='english') -> List[str]:
    """
    Applique le Snowball stemmer à une phrase.
    
    Args:
        phrase (str): The phrase to stem.
        language (str): The language to use for stemming.
        
    Returns:
        List[str]: List of stemmed words.
    """
    stemmer = SnowballStemmer(language)
    words = word_tokenize(phrase)
    return [stemmer.stem(word) for word in words if word.isalpha()]

def wordnet_lemmatizer(text: str, pos: str='n') -> List[str]:
    """
    Applique le WordNet lemmatizer à un texte.
    
    Args:
        text (str): The text to lemmatize.
        pos (str): The part of speech tag to use for lemmatization.
        
    Returns:
        List[str]: List of lemmatized words.
    """
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(text)
    return [lemmatizer.lemmatize(word, pos) for word in words]

def wordnet_lemmatizer_phrase(phrase: str, pos:str='n') -> List[str]:
    """
    Applique le WordNet lemmatizer à une phrase.
    
    Args:
        phrase (str): The phrase to lemmatize.
        pos (str): The part of speech tag to use for lemmatization.
        
    Returns:
        List[str]: List of lemmatized words.
    """
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(phrase)
    return [lemmatizer.lemmatize(word, pos) for word in words]

def lovins_stemmer(text: str) -> List[str]:
    """
    Applique le Lovins stemmer à un texte.
    
    Args:
        text (str): The text to stem.
        
    Returns:
        List[str]: List of stemmed words
    """
    list_mot = text.split()
    
    stemmed_words = []
    for word in list_mot:
        if word.isalpha():
            try:
                stemmed_word = LovinsStemmer(word)
                stemmed_words.append(stemmed_word)
            except IndexError as e:
                print(f"Error stemming word: {word}, {e}")
        else:
            stemmed_words.append(word)
    
    return stemmed_words