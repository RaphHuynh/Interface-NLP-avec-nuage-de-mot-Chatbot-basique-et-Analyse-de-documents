import os
from lib import *
import networkx as nx
import numpy as np
from io import BytesIO
import base64
import matplotlib.pyplot as plt
from aquarel import load_theme
import seaborn as sns
from typing import List, Tuple, Dict
import pandas as pd

def plot_knn_graph(k: int, distance_matrix: List[List[float]], corpus_sans_poc: List[str], selected_index: int) -> base64:
    """génère un graphique de réseau pour les k plus proches voisins d'un document sélectionné.

    Args:
        k (int): nombre de voisins les plus proches à afficher
        distance_matrix (List[List[float]]): matrice de distance entre les documents
        corpus_sans_poc (List[str]): corpus de documents sans ponctuation
        selected_index (int): index du document sélectionné

    Returns:
        base64: image encodée en base64
    """
    G = nx.Graph()
    
    # Ajouter les nœuds avec les indices comme labels
    for i in range(len(corpus_sans_poc)):
        # Utilise l'index comme libellé du nœud
        G.add_node(i, label=str(i))
    
    # Ajouter les arêtes pour le nœud sélectionné et ses k plus proches voisins
    nearest_neighbors = sorted(enumerate(distance_matrix[selected_index]), key=lambda x: x[1])[:k+1]
    edges = []
    max_dist = max([dist for _, dist in nearest_neighbors])
    
    for neighbor, dist in nearest_neighbors[1:]:  # Exclure le nœud lui-même
        # Ajouter une arête avec un poids inversé pour la distance (plus proche = plus lourd)
        G.add_edge(selected_index, neighbor, weight=(max_dist+1)-dist)
        edges.append((selected_index, neighbor, dist))
    
    # Utiliser une disposition fixe en ancrant le nœud sélectionné au centre
    fixed_pos = {selected_index: (0, 0)}
    
    # Ajuster les paramètres du spring_layout pour une meilleure disposition
    pos = nx.spring_layout(G, pos=fixed_pos, fixed=[selected_index], k=0.5, iterations=50)
    
    plt.figure(figsize=(10, 8))
    plt.axis('off')  # Retire le cadre noir et les axes

    # Définir les couleurs des nœuds (rouge pour le nœud sélectionné, bleu pour les autres)
    node_colors = ['red' if i == selected_index else 'skyblue' for i in range(len(corpus_sans_poc))]
    
    node_sizes = 1000
    
    # Définir les couleurs des arêtes avec un gradient de couleur pour la distance
    norm = plt.Normalize(vmin=min([dist for _, _, dist in edges]), vmax=max([dist for _, _, dist in edges]))
    edge_colors = [plt.cm.viridis(norm(dist)) for _, _, dist in edges]  # Utilise le colormap Viridis pour le gradient
    
    # Tracer les nœuds et les arêtes du nœud sélectionné
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes)
    nx.draw_networkx_edges(G, pos, edgelist=[(selected_index, neighbor) for _, neighbor, _ in edges], edge_color=edge_colors, width=2)
    nx.draw_networkx_labels(G, pos, labels={i: i for i in range(len(corpus_sans_poc))}, font_size=10, font_weight="bold")

    # Conversion en image PNG pour l'application
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')  # 'bbox_inches' pour éviter les marges inutiles
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return f"data:image/png;base64,{img_data}"

def stopwords(corpus: List[str], list_mot: List[str], nom_stop_words: List[str]) -> Tuple[List[str], List[str]]:
    """Fonction pour supprimer les mots vides d'un corpus et d'une liste de mots.

    Args:
        corpus (List[str]): liste des documents
        list_mot (_type_): liste des mots
        nom_stop_words (_type_): nom du fichier de mots vides

    Returns:
        Tuple(List[str][str]): corpus sans mots vides, liste de mots sans mots vides
    """
    base_dir = os.path.dirname(__file__)
    if nom_stop_words == "en_short":
        path = os.path.join(base_dir, "stopwords/en_short.txt")
    elif nom_stop_words == "English":
        path = os.path.join(base_dir, "stopwords/en.txt")
    else:   
        path = os.path.join(base_dir, "stopwords/fr.txt")
        
    with open(path, "r") as fichier:
        mots_vides = fichier.read().split("\n")
            
    mots_vides = [mot.lower() for mot in mots_vides]
    
    list_mot_stopwords = [mot.lower() for mot in list_mot if mot.lower() not in mots_vides]
    corpus_lower = [doc.lower() for doc in corpus]
    corpus_stopwords = [" ".join([mot for mot in doc.split() if mot not in mots_vides]) for doc in corpus_lower]
    
    return corpus_stopwords, list_mot_stopwords

def get_backbofwords(corpus_sans_poc: List[str], liste_mots: List[str], choix1: str) -> List[List[float]]:
    """ Fonction pour obtenir la matrice de backbofwords selon le choix de l'utilisateur.

    Args:
        corpus_sans_poc (List[str]): corpus de documents sans ponctuation
        list_mot (List[str]): liste des mots
        choix1 (str): choix de l'utilisateur

    Returns:
        List[List[float]]: matrice du descripteur (backbofwords)
    """
    if choix1 == "1":
        return backbofwordsBinaire(corpus_sans_poc, liste_mots)
    elif choix1 == "2":
        return backbofwords_occurence(corpus_sans_poc, liste_mots)
    elif choix1 == "3":
        return matrix_backbofwords_normalize_Norme(corpus_sans_poc, liste_mots)
    elif choix1 == "4":
        return matrix_backbofwords_normalize_proba(corpus_sans_poc, liste_mots)
    elif choix1 == "5":
        return tf_idf_bin(corpus_sans_poc, liste_mots)
    elif choix1 == "6":
        return tf_idf_norm(corpus_sans_poc, liste_mots)
    elif choix1 == "7":
        return tf_idf_occ(corpus_sans_poc, liste_mots)
    else:
        return tf_idf_new(corpus_sans_poc, liste_mots)

def get_distance_matrix(list_backbofwords: List[List[float]], distance: str) -> List[List[float]]:
    """ Fonction pour obtenir la matrice de distance selon le choix de l'utilisateur.

    Args:
        list_backbofwords (List[List[float]]): matrice du descripteur (backbofwords)
        distance (str): nom de la distance

    Returns:
        List[List[float]]: matrice de distance
    """
    if distance == "Euclidienne":
        return matrix_distance_Euclidienne(list_backbofwords)
    elif distance == "Cosinus":
        return matrice_distance_cosinus(list_backbofwords)
    elif distance == "Curtis":
        return matrice_distance_bray_curtis(list_backbofwords)
    elif distance == "Kullback":
        return matrice_kullback_leibler(list_backbofwords)
    elif distance == "Jacard":
        return matrice_distance_jacard(list_backbofwords)
    elif distance == "Hamming":
        return matrice_distance_hamming(list_backbofwords)
    else:
        return matrix_distance_Manhattan(list_backbofwords)

def get_k_nearest_phrases(corpus_sans_poc: List[str], selected_phrase_index: int, k: int, distance_matrix: List[List[float]]) -> List[str]:
    """ Fonction pour obtenir les k plus proches voisins d'un document sélectionné.

    Args:
        corpus_sans_poc (List[str]): corpus de documents sans ponctuation
        selected_phrase_index (int): index du document sélectionné
        k (int): nombre de voisins les plus proches à afficher
        distance_matrix (List[List[float]]): matrice de distance entre les documents

    Returns:
        List[str]: liste des k plus proches voisins
    """
    if selected_phrase_index is not None:
        selected_phrase = corpus_sans_poc[selected_phrase_index]
        k_nearest = K_plus_proches_documents(selected_phrase, k, corpus_sans_poc, distance_matrix)
        return [f"• {phrase}: {distance}" for phrase, distance in k_nearest]
    else:
        return []
    
def style_dataframe(df: pd.DataFrame) -> pd.io.formats.style.Styler:
    """ Fonction pour styliser un DataFrame avec des couleurs et des propriétés CSS.

    Args:
        df (pd.DataFrame): DataFrame à styliser

    Returns:
        pd.io.formats.style.Styler: DataFrame stylisé
    """
    return df.style.set_table_attributes('class="table-auto w-full border-collapse border border-gray-200"').format("{:.3f}").background_gradient(cmap='viridis', low=0, high=1).set_properties(**{
            'white-space': 'nowrap',
            'font-size': '14px',
            'text-align': 'center',
        })
        
def descriptor_select_distance(choix: str) -> List[str]:
    """ Fonction pour sélectionner les distances en fonction du choix de l'utilisateur.

    Args:
        choix (str): choix de l'utilisateur

    Returns:
        List[str]: liste des distances disponibles
    """
    if choix == "1":
        return ["Euclidienne", "Manhattan", "Cosinus", "Curtis", "Kullback", "Jacard", "Hamming"]
    else:
        return ["Euclidienne", "Manhattan", "Cosinus", "Curtis", "Kullback"]
    
def calculate_word_frequency(corpus: List[str]) -> Dict[str, int]:
    """
    Calcule la fréquence des mots dans le corpus sans utiliser de librairie.
    
    Args:
        corpus (List[str]): Liste des phrases du corpus.
    
    Returns:
        Dict[str, int]: Dictionnaire avec les mots comme clés et leur fréquence comme valeur.
    """
    frequency = {}
    for phrase in corpus:
        for word in phrase.split():
            if word in frequency:
                frequency[word] += 1
            else:
                frequency[word] = 1
    return frequency

def plot_word_frequency(word_frequency_df: Dict[str, int]) -> base64:
    """ Fonction pour générer un graphique de fréquence de mots à partir d'un DataFrame.

    Args:
        word_frequency_df (Dict[str, int]): DataFrame de fréquence de mots

    Returns:
        base64: image encodée en base64
    """
    # Limiter aux 20 mots les plus fréquents pour la lisibilité
    word_frequency_df = word_frequency_df.sort_values(by='Fréquence', ascending=False).head(20)
    
    # Création de la palette de couleurs personnalisée
    color_palette = sns.color_palette("viridis", len(word_frequency_df))  # Utilisation de la palette "viridis"
    
    with load_theme("minimal_light"):
        # Création du graphique avec des barres horizontales
        plt.figure(figsize=(8, 8))
        bars = plt.barh(word_frequency_df['Mot'], word_frequency_df['Fréquence'], color=color_palette)
        plt.gca().invert_yaxis()  # Inverser l'ordre des mots pour que le plus fréquent soit en haut
        plt.xlabel("Fréquence")
        plt.ylabel("Mots")
        plt.title("Fréquence des mots les plus courants")
        plt.tight_layout()
        
        # Sauvegarde l'image dans un buffer
        buf = BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        image_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        plt.close()
        return f"data:image/png;base64,{image_base64}"
    
    
def plot_word_frequency_pie(word_frequency_df: Dict[str, int]) -> base64:
    """ Fonction pour générer un graphique camembert de fréquence de mots à partir d'un DataFrame.

    Args:
        word_frequency_df (Dict[str, int]): DataFrame de fréquence de mots

    Returns:
        base64: image encodée en base64
    """
    # Limiter aux 10 mots les plus fréquents pour la lisibilité d'un camembert
    word_frequency_df = word_frequency_df.sort_values(by='Fréquence', ascending=False).head(10)
    
    # Création de la palette de couleurs personnalisée
    color_palette = sns.color_palette("viridis", len(word_frequency_df))  # Utilisation de la palette "viridis"
    
    # Création du graphique avec le thème "minimal_light"
    with load_theme("minimal_light"):
        plt.figure(figsize=(8, 8))
        plt.pie(
            word_frequency_df['Fréquence'],
            labels=word_frequency_df['Mot'],
            autopct='%1.1f%%',  # Afficher les pourcentages
            startangle=140,  # Angle de démarrage pour l'alignement
            colors=color_palette  # Application de la palette de couleurs
        )
        plt.title("Répartition des mots les plus fréquents")
        
        # Sauvegarde l'image dans un buffer
        buf = BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        image_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        plt.close()
        return f"data:image/png;base64,{image_base64}"
