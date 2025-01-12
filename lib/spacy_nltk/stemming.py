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

def porter_stemmer_phrase(phrase):
    stemmer = PorterStemmer()
    words = word_tokenize(phrase)
    return [stemmer.stem(word) for word in words if word.isalpha()]

def lancaster_stemmer(list_words):
    stemmer = LancasterStemmer()
    return [stemmer.stem(word) for word in list_words]

def lancaster_stemmer_phrase(phrase):
    stemmer = LancasterStemmer()
    words = word_tokenize(phrase)
    return [stemmer.stem(word) for word in words if word.isalpha()]

def snowball_stemmer(text, language='english'):
    stemmer = SnowballStemmer(language)
    return [stemmer.stem(word) for word in text]

def snowball_stemmer_phrase(phrase, language='english'):
    stemmer = SnowballStemmer(language)
    words = word_tokenize(phrase)
    return [stemmer.stem(word) for word in words if word.isalpha()]

def wordnet_lemmatizer(text, pos='n'):
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(text)
    return [lemmatizer.lemmatize(word, pos) for word in words]

def wordnet_lemmatizer_phrase(phrase, pos='n'):
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(phrase)
    return [lemmatizer.lemmatize(word, pos) for word in words]

def lovins_stemmer(text):
    stemmer = nltk.LovinsStemmer()
    words = word_tokenize(text)
    return [stemmer.stem(word) for word in words]

def lovins_stemmer_phrase(phrase):
    stemmer = nltk.LovinsStemmer()
    words = word_tokenize(phrase)
    return [stemmer.stem(word) for word in words]

def porter2_stemmer(text):
    stemmer = nltk.Porter2Stemmer()
    words = word_tokenize(text)
    return [stemmer.stem(word) for word in words]

def porter2_stemmer_phrase(phrase):
    stemmer = nltk.Porter2Stemmer()
    words = word_tokenize(phrase)
    return [stemmer.stem(word) for word in words]

def regexp_stemmer(text, regexp):
    stemmer = nltk.RegexpStemmer(regexp)
    words = word_tokenize(text)
    return [stemmer.stem(word) for word in words]

def isri_stemmer(text):
    stemmer = nltk.ISRIStemmer()
    words = word_tokenize(text)
    return [stemmer.stem(word) for word in words]
    