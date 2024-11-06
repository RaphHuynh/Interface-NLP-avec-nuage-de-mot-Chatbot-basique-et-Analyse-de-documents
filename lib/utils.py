import os
from lib import *
import networkx as nx
import numpy as np
from io import BytesIO
import base64
import matplotlib.pyplot as plt

def plot_knn_graph(k, distance_matrix, corpus_sans_poc, selected_index):
    G = nx.Graph()
    
    # Ajouter les nœuds avec les indices comme labels
    for i in range(len(corpus_sans_poc)):
        G.add_node(i, label=str(i))  # Utilise l'index comme libellé du nœud
    
    # Ajouter les arêtes pour le nœud sélectionné et ses k plus proches voisins
    nearest_neighbors = sorted(enumerate(distance_matrix[selected_index]), key=lambda x: x[1])[:k+1]
    edges = []
    max_dist = max([dist for _, dist in nearest_neighbors])
    
    for neighbor, dist in nearest_neighbors[1:]:  # Exclure le nœud lui-même
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

def stopwords(corpus, list_mot, nom_stop_words):
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

def get_backbofwords(corpus_sans_poc, liste_mots, choix1):
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

def get_distance_matrix(list_backbofwords, distance):
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

def get_k_nearest_phrases(corpus_sans_poc, selected_phrase_index, k, distance_matrix):
    if selected_phrase_index is not None:
        selected_phrase = corpus_sans_poc[selected_phrase_index]
        k_nearest = K_plus_proches_documents(selected_phrase, k, corpus_sans_poc, distance_matrix)
        return [f"• {phrase}: {distance}" for phrase, distance in k_nearest]
    else:
        return []
    
def style_dataframe(df):
    return df.style.set_table_attributes('class="table-auto w-full border-collapse border border-gray-200"').format("{:.3f}").background_gradient(cmap='viridis', low=0, high=1).set_properties(**{
            'white-space': 'nowrap',
            'font-size': '14px',
            'text-align': 'center',
        })
        
def descriptor_select_distance(choix):
    if choix == "1":
        return ["Euclidienne", "Manhattan", "Cosinus", "Curtis", "Kullback", "Jacard", "Hamming"]
    else:
        return ["Euclidienne", "Manhattan", "Cosinus", "Curtis", "Kullback"]