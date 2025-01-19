# Interface NLP avec nuage de mot / Chatbot basique et Analyse de documents

## Comment faire fonctionner l'application ?
- Installer les librairies avec la commande :
  
```
    pip install -r requirements.txt -v
```

- Pour allumer l'application :
  
    Reste dans le document de l'application est lancé la commande ci-dessous

```
    python main.py
```

## Comment utiliser l'application ?

### Pour un seul fichier
- Pour utiliser l'application pour un seul fichier, il suffit de cliquer sur le bouton "Choisir un fichier" et de sélectionner le fichier à analyser.

### Pour un corpus de fichier / plusieurs fichiers
- Pour utiliser l'application pour un corpus, il suffit de cliquer sur le bouton "Choisir un dossier" et de sélectionner tout les fichiers du dossier contenant les fichiers à analyser.

### Pour utiliser le chatbot
- Pour utiliser le chatbot, il suffit de cliquer sur le bouton "Chatbot" et de poser une question à l'IA quand vous avez généré le ou les fichiers à analyser en cliquant sur le bouton "Generate".

### Pour générer les nuages de points
- Pour générer les nuages de points, il suffit de cliquer sur le bouton "Generate" après avoir sélectionné le fichier ou le dossier à analyser.

> **Note :** Pour utiliser le chatbot et le nuage, il faut d'abord générer les fichiers à analyser en cliquant sur le bouton "Generate". Il faut aussi faire attention a l'encodage des fichiers .txt, il faut qu'ils soient en UTF-8.

## Comment fonctionne l'application ?

### Pour l'analyse de texte ( k plus proches voisins )

#### 1. Prétraitement des données

- Descripteur liste:
  - Bag of words Binaire
  - Bag of words Occurence
  - Bag of words normalisé
  - Bag of words Probabilité
  - Bag of words TF-IDF Binaire
  - Bag of words TF-IDF Normalisé
  - Bag of words TF-IDF Occurence
  - Bag of words TF-IDF New (vu en cours)
  - Embedding Word2Vec
  - Embedding FastText
  - Embedding Doc2Vec

- Distance liste:
  - Distance Euclidienne
  - Distance Cosinus
  - Distance Jaccard
  - Distance Manhattan
  - Distance Hamming
  - Distance Kullback-Leibler
  - Distance Bray-Curtis

- Stopwords liste:
    - Stopword Français -> Ceux du site
    - Stopword English -> Ceux du site version longue
    - english sort -> Ceux du site version courte
    - Stopword nltk français
    - Stopword nltk english
    - Stopword spacy français
    - Stopword spacy english
    - Stopword sklearn english
  
- Lemmatisation et stemmer liste:
  - Porter stemmer
  - Snowball stemmer
  - Lancaster stemmer
  - WordNet Lemmatizer
  - Lovins stemmer

#### 2. Graphiques

- Graphique des k plus proches voisins en fonction de la distance
- Graphique en histogramme des fréquences des mots
- Graphique en camembert des fréquences des mots
- Graphique boxplot des distances moyennes
- Graphique boxplot du nombre de mots moyens par texte ou phrase.

#### 3. K plus proches documents

- Voir le fichier k_plus_proches_documents.py situé dans lib

### Nuage de mots

Il y a 6 nuages de mots générés différents

- Nuage de mots des mots les plus fréquents dans le texte avec WordCloud en couleur sans retirer les stopwords

- Nuage de mots des mots les plus fréquents dans le texte avec WordCloud en noir et blanc sans retirer les stopwords

- Nuage de mots des mots les plus fréquents dans le texte avec WordCloud en couleur en retirant les stopwords avec le stopwords sélectionnés dans le menu (sidebar)

- Nuage de mots des mots les plus fréquents dans le texte avec WordCloud en retirant les stopwords avec le stopwords sélectionnés dans le menu (sidebar) et en ajoutant un mask du pays sélectionné dans le menu (sidebar) (Il faut selectionner la langue donc soit france soit english si english carte des etats unis sinon france)

- Nuage de mots avec les stopwords du WordCloud

- Nuage de mots calculé avec la méthode TF-IDF avec WordCloud avec stopwords nltk

### Chatbot

#### 1. Explication du fonctionnement

- Le chatbot utilise Word2Vec

- La fonction **modele_word2vec** génère un modèle Word2Vec à partir d'un corpus de documents tokenizés. Le vocabulaire du modèle est construit à partir du corpus.

- La fonction mot_significatif détermine quel mot de la question posée est le plus pertinent en fonction du modèle Word2Vec.
  - La question est découpée en mots (split()).
  Pour chaque mot, la fonction vérifie s’il est présent dans le vocabulaire du modèle (modele.wv.key_to_index).
  - Si le mot est dans le vocabulaire : La norme de son vecteur dans l’espace Word2Vec est calculée (np.linalg.norm(modele.wv[mot])). Cette norme est utilisée pour estimer l'importance du mot.
  - Le mot avec la plus grande norme est retourné comme mot significatif.
  - Si aucun mot significatif n'est trouvé, la fonction retourne None.

- La fonction **trouver_phrase** localise la phrase contenant un mot spécifique dans un document.
  - Le document est découpé en phrases en utilisant les délimiteurs ., !, et ? grâce à l’expression régulière re.split(r'[.!?]', document).
  - Chaque phrase est vérifiée pour voir si elle contient le mot recherché.
  - La première phrase contenant le mot est retournée. Si aucune phrase ne correspond, la fonction retourne None.

- La fonction repondre_a_question combine toutes les autres pour répondre à une question basée sur le document.

#### 2. Pourquoi ce choix ?

J'ai suivi cette logique pour réaliser le chatbot:
- Détecter le mot de la question qui est le plus significatif
- Repérer la première occurrence de ce mot dans le document pertinent et retourner comme réponse la phrase qui le contient. Une phrase est définie ici comme étant le texte entouré par deux ponctuations. 

Word2Vec représente chaque mot comme un vecteur dans un espace où la distance entre vecteurs représente les similarités entre les mots.
La norme d'un vecteur peut être utilisé comme une mesure de son importane dans l'espace.
Les mots avec une forte norme vectorielle sont souvent ceux qui apparaissent fréquemment dans le corpus et qui ont une signification sémantique bien définie dans le modèle.
