from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from io import BytesIO
import base64
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize

def nuage_mots(texte: str) -> str:
    """
    Génère un nuage de mots à partir d'un texte.
    
    Args:
        texte (str): Le texte à analyser.
        
    Returns:
        str: L'image du nuage de mots encodée en base64.
    """
    wc = WordCloud(colormap = 'binary',background_color = 'white')
    wc.generate(texte)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return f"data:image/png;base64,{img_data}"
    
    
def nuage_mots_couleur(texte: str) -> str:
    """
    Génère un nuage de mots coloré à partir d'un texte.
    
    Args:
        texte (str): Le texte à analyser.
        
    Returns:
        str: L'image du nuage de mots encodée en base64.
    """
    wc = WordCloud().generate(texte)
    plt.imshow(wc)
    plt.axis('off')
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return f"data:image/png;base64,{img_data}"

def nuage_mots_couleur_stopword(texte: str) -> str:
    """
    Génère un nuage de mots coloré à partir d'un texte en excluant les stopwords sélectionnés dans le menu.
    
    Args:
        texte (str): Le texte à analyser.
        
    Returns:
        str: L'image du nuage de mots encodée en base64.
    """
    wc = WordCloud().generate(texte)
    plt.imshow(wc)
    plt.axis('off')
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return f"data:image/png;base64,{img_data}"

def nuage_mots_couleur_masque(texte: str, lang: str) -> str:
    """
    Génère un nuage de mots coloré à partir d'un texte avec un masque de forme spécifique.
    
    Args:
        texte (str): Le texte à analyser.
        lang (str): La langue du texte.
        
    Returns:
        str: L'image du nuage de mots encodée en base64.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if lang == 'Français':
        masque = os.path.join(current_dir, "france-map.jpg")
    else:
        masque = os.path.join(current_dir, "usa-map.jpg")
    wc = WordCloud(mask = np.array(Image.open(masque)),contour_width=2, contour_color='firebrick',background_color="white",colormap = 'Spectral').generate(texte)
    plt.imshow(wc)
    plt.axis('off')
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return f"data:image/png;base64,{img_data}"

def nuage_mots_stopword_wordcloud(texte: str) -> str:
    """
    Génère un nuage de mots en excluant les stopwords de la librairie WordCloud.
    
    Args:
        texte (str): Le texte à analyser.
        
    Returns:
        str: L'image du nuage de mots encodée en base64.
    """
    wc = WordCloud(colormap = 'Spectral', stopwords = STOPWORDS, background_color = 'white').generate(texte)
    plt.imshow(wc)
    plt.axis('off')
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return f"data:image/png;base64,{img_data}"

def nuage_mots_tfidf(texte: str, lang: str) -> str:
    """
    Génère un nuage de mots en utilisant la méthode TF-IDF.
    
    Args:
        texte (str): Le texte à analyser.
        lang (str): La langue du texte.
        
    Returns:
        str: L'image du nuage de mots encodée en base64.
    """
    if lang == 'Français':
        nltk.download('stopwords')
        vector = TfidfVectorizer(stop_words=stopwords.words('french'))
    else:
        vector = TfidfVectorizer(stop_words="english")
    
    matrice = vector.fit_transform(sent_tokenize(texte))
    tokens = vector.get_feature_names_out()
    
    score = matrice.toarray()
    
    score = dict(zip(tokens, score.sum(axis=0)))
    
    wc = WordCloud(background_color="white").generate_from_frequencies(score)
    
    plt.imshow(wc)
    plt.axis('off')
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return f"data:image/png;base64,{img_data}"