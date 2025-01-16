from shiny import App, ui, render, reactive
import pandas as pd
from lib import *
from lib.utils import *

app_ui = ui.page_fluid(
    ui.div(
        # Sidebar
        ui.div(
            ui.div(
                ui.h2("Menu", class_="h3 text-center font-weight-bold mb-4 border-bottom pb-3"),
                ui.input_select("lang_select", "", choices={"Français": "🇫🇷 Français", "English": "🏴 English"}, selected="Français"),
                ui.p("Descripteur", class_="mt-2"),
                ui.input_select(
                    "choix1", "", 
                    choices={"1": "Binaire", "2": "Occurence", "3": "Probalite", "4":"Normalise","5":"tf_idf_bin","6":"tf_idf_occ","7":"tf_idf_norm","8":"tf_idf_new"}, 
                    selected="1"  
                ),
                ui.p("Distance", class_="mt-2"),
                ui.input_select(
                    "choix2", "", 
                    choices=descriptor_select_distance("1"),
                    selected="Euclidienne"
                ),
                ui.p("Stopwords", class_="mt-2"),
                ui.input_select("stopwords", "", choices={"1": "Stopword Français", "2": "Stopwords English", "3":"Stopwords nltk français", "4":"Stopwords nltk english", "5":"english short", "6": "Aucun"}, selected="6"),
                ui.p("Stemming & Lemmatisation", class_="mt-2"),
                ui.input_select("stemming", "", choices={"1": "Porter Stemmer", "2": "Snowball Stemmer", "3":"Lancaster Stemmer", "4":"wordNet Lemmatiser", "5":"Lovins Stemmer", "6":"Aucun"}, selected="6"),
                ui.input_file("file_input", "Déposer un fichier ici ou cliquer pour sélectionner un fichier", multiple=True),
                ui.output_ui("phrase_selector"),
                ui.input_slider("k_value", "Nombre de voisins les plus proches (k)", min=1, max=10, value=3, step=1),
                ui.input_action_button("generate", "Generate", class_="mt-4 w-100 btn btn-dark"),
                class_="p-4 shadow-sm bg-light rounded",
            ),
            class_="mt-2 position-fixed",
        ),
        # Main content
        ui.div(
            ui.navset_card_tab(
                ui.nav_panel("Analyse de texte", ui.output_ui("content")),
                ui.nav_panel("Nuage de point", ui.output_ui("embedding_call")),
                ui.nav_panel("Chatbot", ui.output_ui("chatbot")),
                id="selected_navset_card_tab",
            ),
            class_="col-md-9 p-4 main-content position-absolute end-0 top-0",
        ),
        class_="d-flex"
    ),
)

# Mise à jour de la fonction de rendu pour inclure le graphe
def server(input, output, session):
    lang = reactive.Value("Français")
    stopword = reactive.Value("Aucun")
    stemming = reactive.Value("Aucun")
    phrases = reactive.Value([])
    corpus_ponc = reactive.Value([])
    selected_phrase_index = reactive.Value(None)
    selected_phrase_index_str = reactive.Value("0")
    graph_image = reactive.Value("")
       
    @output 
    @render.ui
    def embedding_call():
        corpus = input.file_input()
        if not corpus:
            return ui.p("Veuillez sélectionner un fichier." if lang.get() == "Français" else "Please select a file.")
        
        if len(corpus) > 1:
            object_corpus = Corpus()
            for file in corpus:
                with open(file['datapath'], 'r', encoding='utf-8') as f:
                    text = f.read()
                    object_corpus.add_document(text)
            corpus = object_corpus.list_documents
            corpus_sans_poc = [retirer_ponctuation(c) for c in object_corpus.list_documents if c]
            phrases.set(corpus_sans_poc)
        else:
            corpus = corpus[0]
            with open(corpus['datapath'], 'r', encoding='utf-8') as f:
                contenu = f.read()

            corpus = separer_phrase(contenu)
            corpus_sans_poc = supp_poc_corpus(corpus)
            phrases.set(corpus_sans_poc)
            
        liste_mots = give_liste_mot(corpus_sans_poc, stemming.get())
        
        if stopword.get() != "6":
            corpus_stopword, liste_mots_stopword = stopwords(corpus_sans_poc, liste_mots, stopword.get())
            corpus_sans_poc_stopword = corpus_sans_poc
        else:
            corpus_stopword = corpus_sans_poc
            corpus_sans_poc_stopword = corpus_sans_poc
            
        wc_color = nuage_mots_couleur(" ".join(corpus_sans_poc_stopword))
        wc = nuage_mots(" ".join(corpus_sans_poc_stopword),)
        wc_color_stopword = nuage_mots_couleur_stopword(" ".join(corpus_stopword))
        wc_mask = nuage_mots_couleur_masque(" ".join(corpus_stopword), lang.get())
        
        return ui.div(
    ui.div(
        ui.div(
            ui.h3('Nuages de mots'),
            class_='text-center mb-4 font-weight-bold'
        ),
        ui.div(
            ui.div(
                ui.div(ui.p('Nuage de mot avec couleur et sans stopword', class_='text-center'), class_='mb-2'),
                ui.div(ui.img(src=wc_color, class_='img-fluid'), class_='text-center'),
                class_='col-md-6'
            ),
            ui.div(
                ui.div(ui.p('Nuage de mot sans couleur et sans stopword', class_='text-center'), class_='mb-2'),
                ui.div(ui.img(src=wc, class_='img-fluid'), class_='text-center'),
                class_='col-md-6'
            ),
            class_='row mb-4'
        ),
        ui.div(
            ui.div(
                ui.div(ui.p('Nuage de mot avec couleur et avec stopword', class_='text-center'), class_='mb-2'),
                ui.div(ui.img(src=wc_color_stopword, class_='img-fluid'), class_='text-center'),
                class_='col-md-6'
            ),
            ui.div(
                ui.div(ui.p('Nuage de mot avec couleur, stopword et mask du pays', class_='text-center'), class_='mb-2'),
                ui.div(ui.img(src=wc_mask, class_='img-fluid'), class_='text-center'),
                class_='col-md-6'
            ),
            class_='row'
        ),
        class_='container'
    )
)

    @reactive.Effect
    @reactive.event(input.lang_select)
    def update_lang():
        lang.set(input.lang_select())
        
    @reactive.Effect
    @reactive.event(input.stopwords)
    def update_stopwords():
        stopword.set(input.stopwords())
        
    @reactive.Effect
    @reactive.event(input.stemming)
    def update_stemming():
        stemming.set(input.stemming())

    @reactive.Effect
    @reactive.event(input.phrase_select)
    def update_selected_phrase():
        new_value = input.phrase_select()
        selected_phrase_index.set(int(new_value) if new_value else None)
        selected_phrase_index_str.set(new_value if new_value else "0")

    @output
    @render.ui
    def phrase_selector():
        if not phrases.get():
            return None
        return ui.input_select("phrase_select", "Choisissez une phrase", choices={str(i): p for i, p in enumerate(phrases.get())}, selected=selected_phrase_index_str.get())  

    @reactive.Effect
    @reactive.event(input.file_input)
    def update_k_value_max():
        if input.file_input() and len(input.file_input()) == 1:
            uploaded_file = input.file_input()[0]
            with open(uploaded_file['datapath'], 'r', encoding='utf-8') as f:
                contenu = f.read()
            corpus = separer_phrase(contenu)
            corpus_sans_poc = supp_poc_corpus(corpus)
            phrases.set(corpus_sans_poc)
            ui.update_slider("k_value", max=len(corpus_sans_poc)-1)
        elif input.file_input() and len(input.file_input()) > 1:
            object_corpus = Corpus()
            for file in input.file_input():
                with open(file['datapath'], 'r', encoding='utf-8') as f:
                    text = f.read()
                    object_corpus.add_document(text)
            corpus = object_corpus.list_documents
            corpus_sans_poc = [retirer_ponctuation(c) for c in object_corpus.list_documents if c]
            phrases.set(corpus_sans_poc)
            ui.update_slider("k_value", max=len(corpus_sans_poc)-1)
        else:
            ui.update_slider("k_value", max=10)
            
    @reactive.Effect
    @reactive.event(input.choix1)
    def update_distance_choices():
        new_choices = descriptor_select_distance(input.choix1())
        ui.update_select("choix2", choices=new_choices)
        
    @output
    @render.ui
    def content():
        selected_lang = lang.get()
        selected_stopwords = stopword.get()
        selected_stemming = stemming.get()
        
        if not input.file_input():
            return ui.p("Veuillez sélectionner un fichier." if selected_lang == "Français" else "Please select a file.")

        if not input.generate():
            return ui.p("Cliquez sur Generate pour voir les résultats." if selected_lang == "Français" else "Click Generate to see results.")
        
        uploaded_file = input.file_input()
        
        if len(uploaded_file) > 1:
            object_corpus = Corpus()
            for file in uploaded_file:
                with open(file['datapath'], 'r', encoding='utf-8') as f:
                    text = f.read()
                    object_corpus.add_document(text)
            corpus = object_corpus.list_documents
            corpus_sans_poc = [retirer_ponctuation(c) for c in object_corpus.list_documents if c]
            phrases.set(corpus_sans_poc)
        else:
            uploaded_file = input.file_input()[0]
            with open(uploaded_file['datapath'], 'r', encoding='utf-8') as f:
                contenu = f.read()

            corpus = separer_phrase(contenu)
            corpus_sans_poc = supp_poc_corpus(corpus)
            phrases.set(corpus_sans_poc)
            
        liste_mots = give_liste_mot(corpus_sans_poc, selected_stemming)
            
        if selected_stopwords != "6":
            corpus_sans_poc_stopword, liste_mots_stopword = stopwords(corpus_sans_poc, liste_mots, selected_stopwords)
        else:
            corpus_sans_poc_stopword = corpus_sans_poc
            liste_mots_stopword = liste_mots

        list_backbofwords = get_backbofwords(corpus_sans_poc_stopword, liste_mots_stopword, input.choix1(), selected_stemming)
        distance = input.choix2()
        distance_matrix = get_distance_matrix(list_backbofwords, distance)

        k = input.k_value()
        k_nearest_phrases = get_k_nearest_phrases(corpus, selected_phrase_index.get(), k, distance_matrix)
        k_max = len(corpus_sans_poc_stopword) - 1

        # Générer le graphe des k plus proches voisins
        graph_image.set(plot_knn_graph(k_max, distance_matrix, corpus_sans_poc, selected_phrase_index.get()))
        
        word_frequency = calculate_word_frequency(corpus_sans_poc_stopword)
        word_frequency_df = pd.DataFrame(word_frequency.items(), columns=['Mot', 'Fréquence'])
    
        # Générer le graphe des fréquences des mots
        word_freq_graph = plot_word_frequency(word_frequency_df)
        
        word_freq_graph_pie_chart = plot_word_frequency_pie(word_frequency_df)
         
        #Générer le boxplot des distances
        distance_boxplot = plot_distance_boxplot(distance_matrix)
        
        words_boxplot = plot_number_of_words_boxplot(corpus_sans_poc)        

        return ui.div(
            ui.h3("Résultats de l'analyse", class_="h3 font-weight-bold mb-4 text-center"),
            ui.div(
                ui.p("Phrase sélectionnée :", class_="font-weight-semibold mb-2"),
                ui.p(corpus[selected_phrase_index.get()] if selected_phrase_index.get() is not None else "Aucune phrase sélectionnée."),
                class_="bg-light p-4 rounded mb-4 border-2 shadow-sm"
            ),
            ui.div(
                ui.p("Phrases les plus proches", class_="font-weight-semibold mb-2"),
                ui.HTML("<br>".join(k_nearest_phrases)),
                class_="bg-light p-4 rounded mb-4 border-2 shadow-sm"
            ),
            # Afficher le graphique dans l'application
            ui.div(
                ui.h4("Graphique des K plus proches voisins", class_="h4 font-weight-semibold mb-2 text-center"),
                ui.div(
                    ui.p("Le graphe des k plus proches voisins représente les distances entre les différentes phrases du corpus. Il permet de visualiser les relations entre les phrases en utilisant une mesure de distance spécifique choisie dans le menu. Cela signifie que plus les phrases sont proches du point central plus elles sont similaires à cette phrase. Chaque phrase est représentée par un point dans l'espace vectoriel. Le nombre représente l'index de la phrase dans le corpus.", class_="text-secondary text-justify fs-6"),
                    ui.img(src=graph_image.get(), class_="img-fluid col-md-6 mx-auto"),
                    class_="d-flex gap-2 text-secondary text-justify pr-2 align-items-center",
                ),
                class_="bg-light p-4 rounded mb-4 border-2 shadow-sm",
            ),
            ui.div(
                ui.div(
                    ui.h4("Graphique des Fréquences des Mots", class_="h4 font-weight-semibold mb-2 text-center"),
                    ui.img(src=word_freq_graph, class_="img-fluid mx-auto"),
                    class_="bg-light p-4 rounded mb-4 border-2 shadow-sm"
                ),
                ui.div(
                    ui.h4("Répartition des Mots les plus Fréquents", class_="h4 font-weight-semibold mb-2 text-center"),
                    ui.img(src=word_freq_graph_pie_chart, class_="img-fluid mx-auto"),
                    class_="bg-light p-4 rounded mb-4 border-2 shadow-sm"
                ),
                class_="d-flex gap-2"
            ),
            ui.div(
                ui.h4("Boxplot des Distances", class_="h4 font-weight-semibold mb-2 text-center"),
                ui.div(
                    ui.img(src=distance_boxplot, class_="img-fluid col-md-6 mx-auto"),
                    ui.p("Le boxplot des distances (entre phrases) représente la distribution des distances entre les différentes paires de phrases dans un espace vectoriel. Il permet de visualiser la similarité entre les phrases en utilisant une mesure de distance spécifique. Cela signifie que plus les phrases sont proches de 0 plus elles sont similaires."),
                    class_="d-flex gap-2 text-secondary text-justify pr-2 align-items-center",
                ),
                class_="bg-light p-4 rounded mb-4 border-2 shadow-sm"
            ),
            ui.div(
                ui.h4("Boxplot des fréquences des mots par phrase", class_="h4 font-weight-semibold mb-2 text-center"),
                ui.div(
                    ui.p("Le boxplot des fréquences des mots par phrase représente la distribution des fréquences des mots dans chaque phrase. Il permet de visualiser la variabilité des fréquences des mots dans les phrases du corpus. On peut donc observer si les phrases sont plus ou moins homogènes, courtes ou longues. Dans le cadre où il y a plusieurs documents, le boxplot représente la distribution des fréquences des mots dans chaque document."),
                    ui.img(src=words_boxplot, class_="img-fluid col-md-6 mx-auto"),
                    class_="d-flex gap-2 text-secondary text-justify pr-2 align-items-center",
                ),
                class_="bg-light p-4 rounded mb-4 border-2 shadow-sm"
            ),
        )
        
    @output
    @render.ui
    def chatbot():
        selected_lang = lang.get()
        selected_stopwords = stopword.get()
        selected_stemming = stemming.get()
        
        if not input.file_input():
            return ui.p("Veuillez sélectionner un fichier." if selected_lang == "Français" else "Please select a file.")

        if not input.generate():
            return ui.p("Cliquez sur Generate pour voir les résultats." if selected_lang == "Français" else "Click Generate to see results.")
        
        uploaded_file = input.file_input()
        
        if len(uploaded_file) > 1:
            object_corpus = Corpus()
            for file in uploaded_file:
                with open(file['datapath'], 'r', encoding='utf-8') as f:
                    text = f.read()
                    object_corpus.add_document(text)
            corpus = object_corpus.list_documents
            corpus_sans_poc = [retirer_ponctuation(c) for c in object_corpus.list_documents if c]
            phrases.set(corpus_sans_poc)
            corpus_ponc.set(corpus)
        else:
            uploaded_file = input.file_input()[0]
            with open(uploaded_file['datapath'], 'r', encoding='utf-8') as f:
                contenu = f.read()

            corpus = separer_phrase(contenu)
            corpus_sans_poc = supp_poc_corpus(corpus)
            phrases.set(corpus_sans_poc)
            
        liste_mots = give_liste_mot(corpus_sans_poc, selected_stemming)
            
        if selected_stopwords != "6":
            corpus_sans_poc_stopword, liste_mots_stopword = stopwords(corpus_sans_poc, liste_mots, selected_stopwords)
        else:
            corpus_sans_poc_stopword = corpus_sans_poc
            liste_mots_stopword = liste_mots

        list_backbofwords = get_backbofwords(corpus_sans_poc_stopword, liste_mots_stopword, input.choix1(), selected_stemming)
        distance = input.choix2()
        distance_matrix = get_distance_matrix(list_backbofwords, distance)

        k = input.k_value()
        k_nearest_phrases = get_k_nearest_phrases(corpus, selected_phrase_index.get(), k, distance_matrix)
        k_max = len(corpus_sans_poc_stopword) - 1
        
        return ui.div(
            ui.h3("Chatbot", class_="h3 font-weight-bold mb-4 text-center"),
            ui.div(
                ui.output_text("reponse"),
                class_="bg-success p-3 text-white rounded",
                style="--bs-bg-opacity: .7;"
            ),
            ui.div(
                ui.input_text("question", "Posez une question...",),
                class_="w-full"
            )
        )
        
    @output
    @render.text
    def reponse():
        question = input.question()
        if not question:
            return "Veuillez poser une question." if lang.get() == "Français" else "Please ask a question."
        
        if input.file_input() and len(input.file_input()) > 1:
            corpus = phrases.get()
            corpus_p = corpus_ponc.get()
            corpus_p = " ".join(corpus_p)
        else:
            corpus = phrases.get()
            corpus_p = phrases.get()
            corpus_p = ".".join(corpus_p)

        reponse_text = repondre_a_question(question, corpus_p, corpus)
        return reponse_text

app = App(app_ui, server)  

if __name__ == "__main__":
    app.run()