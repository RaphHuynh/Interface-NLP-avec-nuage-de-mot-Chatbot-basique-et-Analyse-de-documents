import nltk
from nltk.stem import PorterStemmer, LancasterStemmer, SnowballStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Ensure you have the necessary NLTK data files
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')

def porter_stemmer(list_words):
    stemmer = PorterStemmer()
    return [stemmer.stem(word) for word in list_words]

def lancaster_stemmer(list_words):
    stemmer = LancasterStemmer()
    
    return [stemmer.stem(word) for word in list_words]

def snowball_stemmer(text, language='english'):
    stemmer = SnowballStemmer(language)
    words = word_tokenize(text)
    return [stemmer.stem(word) for word in words]

def wordnet_lemmatizer(text, pos='n'):
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(text)
    return [lemmatizer.lemmatize(word, pos) for word in words]

def lovins_stemmer(text):
    stemmer = nltk.LovinsStemmer()
    words = word_tokenize(text)
    return [stemmer.stem(word) for word in words]