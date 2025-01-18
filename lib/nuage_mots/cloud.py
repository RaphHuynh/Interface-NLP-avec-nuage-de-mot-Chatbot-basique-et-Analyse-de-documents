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

def nuage_mots(texte):
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
    
    
def nuage_mots_couleur(texte):
    wc = WordCloud().generate(texte)
    plt.imshow(wc)
    plt.axis('off')
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return f"data:image/png;base64,{img_data}"

def nuage_mots_couleur_stopword(texte):
    wc = WordCloud().generate(texte)
    plt.imshow(wc)
    plt.axis('off')
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return f"data:image/png;base64,{img_data}"

def nuage_mots_couleur_masque(texte, lang):
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

def nuage_mots_stopword_wordcloud(texte):
    wc = WordCloud(colormap = 'Spectral', stopwords = STOPWORDS, background_color = 'white').generate(texte)
    plt.imshow(wc)
    plt.axis('off')
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return f"data:image/png;base64,{img_data}"

def nuage_mots_tfidf(texte, lang):
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