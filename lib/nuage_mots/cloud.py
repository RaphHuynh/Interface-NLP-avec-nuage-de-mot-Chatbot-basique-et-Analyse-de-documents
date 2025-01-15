from wordcloud import WordCloud , ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from random import randint
from io import BytesIO
import base64
import os

def nuage_mots(texte):
    wc = WordCloud(colormap = 'binary',background_color = 'white')
    wc.generate(texte)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)  # 'bbox_inches' pour éviter les marges inutiles
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return f"data:image/png;base64,{img_data}"
    
    
def nuage_mots_couleur(texte):
    wc = WordCloud().generate(texte)
    plt.imshow(wc)
    plt.axis('off')
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)  # 'bbox_inches' pour éviter les marges inutiles
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return f"data:image/png;base64,{img_data}"

def nuage_mots_couleur_stopword(texte):
    wc = WordCloud().generate(texte)
    plt.imshow(wc)
    plt.axis('off')
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)  # 'bbox_inches' pour éviter les marges inutiles
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
    plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)  # 'bbox_inches' pour éviter les marges inutiles
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return f"data:image/png;base64,{img_data}"
    