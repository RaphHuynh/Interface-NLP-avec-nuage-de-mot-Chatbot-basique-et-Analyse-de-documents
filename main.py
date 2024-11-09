from shiny import App, ui, render, reactive
import pandas as pd
from lib import *
from lib import matrice_similarite
from lib.utils import *

app_ui = ui.page_fluid(
    ui.tags.head(
        ui.tags.link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css"),
        ui.tags.script(src="https://code.jquery.com/jquery-3.6.0.min.js"),
        ui.tags.style("""
            html { margin: 0; padding: 0; }
            main { margin: 0; padding: 0; }
            body { margin: 0; padding: 0; background-color: #ffffff; font-family: 'Arial', sans-serif; }
            .main-content { height: 100vh; overflow-y: auto; }
            .table-auto {
                border-collapse: collapse;
                width: 100%;
            }
            .table-auto th, .table-auto td {
                border: 1px solid #ddd;
                padding: 8px;
            }
            .table-auto th {
                background-color: #f2f2f2;
                text-align: left;
            }
            
        """),
        ui.tags.script("""
            $(document).on('click', '#showBackofword', function() {
                $('#backofwordModal').show();
            });
            
            $(document).on('click', '#showDistance', function() {
                $('#distanceModal').show();
            });
            
            $(document).on('click', '.close-modal', function() {
                $(this).closest('.modal').hide();
            });
            
            $(document).on('click', '.modal', function(event) {
                if (event.target === this) {
                    $(this).hide();
                }
            });
        """)
    ),
    ui.div(
        # Sidebar
        ui.div(
            ui.div(
                ui.h2("Menu", class_="text-2xl font-bold mb-4 border-b border-gray-300 pb-3"),
                ui.input_select("lang_select", "", choices={"Français": "🇫🇷 Français", "English": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 English"}, selected="Français"),
                ui.p("Descripteur", class_="mt-4"),
                ui.input_select(
                    "choix1", "", 
                    choices={"1": "Binaire", "2": "Occurence", "3": "Probalite", "4":"Normalise","5":"tf_idf_bin","6":"tf_idf_occ","7":"tf_idf_norm","8":"tf_idf_new"}, 
                    selected="1"  
                ),
                ui.p("Distance", class_="mt-4"),
                ui.input_select(
                    "choix2", "", 
                    choices=descriptor_select_distance("1"),
                    selected="Euclidienne"
                ),
                ui.input_checkbox("use_stopwords", "Utiliser les stopwords", value=True),
                ui.input_file("file_input", "Déposer un fichier ici ou cliquer pour sélectionner un fichier", multiple=False),
                ui.output_ui("phrase_selector"),
                ui.input_slider("k_value", "Nombre de voisins les plus proches (k)", min=1, max=10, value=3, step=1),
                ui.input_action_button("generate", "Generate", class_="mt-4 w-full bg-black text-white py-2 px-4 rounded"),
                class_="p-4 border border-gray-200 shadow-md bg-gray-50 rounded-lg",
            ),
            class_="w-1/5 sidebar mt-4",
        ),
        # Main content
        ui.div(
            ui.output_ui("content"),
            class_="w-4/5 p-8 main-content"
        ),
        class_="flex"
    ),
)

# Mise à jour de la fonction de rendu pour inclure le graphe
def server(input, output, session):
    lang = reactive.Value("Français")
    phrases = reactive.Value([])
    selected_phrase_index = reactive.Value(None)
    selected_phrase_index_str = reactive.Value("0")
    graph_image = reactive.Value("")  # Variable pour l'image du graphe

    @reactive.Effect
    @reactive.event(input.lang_select)
    def update_lang():
        lang.set(input.lang_select())

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
        if input.file_input():
            uploaded_file = input.file_input()[0]
            with open(uploaded_file['datapath'], 'r', encoding='utf-8') as f:
                contenu = f.read()
            corpus = separer_phrase(contenu)
            corpus_sans_poc = supp_poc_corpus(corpus)
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
        if not input.file_input():
            return ui.p("Veuillez sélectionner un fichier." if selected_lang == "Français" else "Please select a file.")

        if not input.generate():
            return ui.p("Cliquez sur Generate pour voir les résultats." if selected_lang == "Français" else "Click Generate to see results.")

        uploaded_file = input.file_input()[0]
        with open(uploaded_file['datapath'], 'r', encoding='utf-8') as f:
            contenu = f.read()

        corpus = separer_phrase(contenu)
        corpus_sans_poc = supp_poc_corpus(corpus)
        phrases.set(corpus_sans_poc)

        liste_mots = retirer_doublons(split_doc_mot(corpus_sans_poc))
        if input.use_stopwords():
            corpus_sans_poc_stopword, liste_mots_stopword = stopwords(corpus_sans_poc, liste_mots, selected_lang)
        else:
            corpus_sans_poc_stopword = corpus_sans_poc
            liste_mots_stopword = liste_mots

        list_backbofwords = get_backbofwords(corpus_sans_poc_stopword, liste_mots_stopword, input.choix1())
        distance = input.choix2()
        distance_matrix = get_distance_matrix(list_backbofwords, distance)

        k = input.k_value()
        k_nearest_phrases = get_k_nearest_phrases(corpus_sans_poc, selected_phrase_index.get(), k, distance_matrix)
        k_max = len(corpus_sans_poc_stopword) - 1

        # Générer le graphe des k plus proches voisins
        graph_image.set(plot_knn_graph(k_max, distance_matrix, corpus_sans_poc, selected_phrase_index.get()))

        # Affiche les matrices de manière permanente
        backofword_df = pd.DataFrame(list_backbofwords)
        distance_df = pd.DataFrame(distance_matrix)
        
        word_frequency = calculate_word_frequency(corpus_sans_poc_stopword)
        word_frequency_df = pd.DataFrame(word_frequency.items(), columns=['Mot', 'Fréquence'])
    
        # Générer le graphe des fréquences des mots
        word_freq_graph = plot_word_frequency(word_frequency_df)
        
        word_freq_graph_pie_chart = plot_word_frequency_pie(word_frequency_df)
         
        #Générer le boxplot des distances
        distance_boxplot = plot_distance_boxplot(distance_matrix)


        return ui.div(
            ui.h3("Résultats de l'analyse", class_="text-2xl font-bold mb-4 text-center"),
            ui.div(
                ui.h4("Phrase sélectionnée :", class_="text-lg font-semibold mb-2"),
                ui.p(corpus_sans_poc[selected_phrase_index.get()] if selected_phrase_index.get() is not None else "Aucune phrase sélectionnée."),
                class_="bg-gray-50 p-4 rounded-lg mb-4 border-2 shadow-md"
            ),
            ui.div(
                ui.h4("Phrases les plus proches", class_="text-lg font-semibold mb-2"),
                ui.HTML("<br>".join(k_nearest_phrases)),
                class_="bg-gray-50 p-4 rounded-lg mb-4 border-2 shadow-md"
            ),
            ui.div(
                ui.div(
                    ui.h4("Matrice Backofword", class_="text-lg font-semibold mb-2 text-center"),
                    ui.div(
                        ui.HTML(style_dataframe(backofword_df).to_html()),
                        class_="overflow-x-auto max-h-96 mb-2"
                    ),
                    class_="w-1/2 bg-gray-50 p-4 rounded-lg border-2 shadow-md"
                ),
                ui.div(
                    ui.h4("Matrice de Distance", class_="text-lg font-semibold mb-2 text-center"),
                    ui.div(
                        ui.HTML(style_dataframe(distance_df).to_html()),
                        class_="overflow-x-auto max-h-96 mb-2"
                    ),
                    class_="w-1/2 bg-gray-50 p-4 rounded-lg border-2 shadow-md"
                ),
                class_="flex gap-2 mb-4"
            ),
            # Afficher le graphique dans l'application
            ui.div(
                ui.h4("Graphique des K plus proches voisins", class_="text-lg font-semibold mb-2 text-center"),
                ui.img(src=graph_image.get(), class_="w-full max-w-3xl mx-auto"),
                class_="bg-gray-50 p-4 rounded-lg mb-4 border-2 shadow-md"
            ),
            ui.div(
                ui.div(
                    ui.h4("Graphique des Fréquences des Mots", class_="text-lg font-semibold mb-2 text-center"),
                    ui.img(src=word_freq_graph, class_="w-full max-w-3xl mx-auto"),
                    class_="bg-gray-50 p-4 rounded-lg mb-4 border-2 shadow-md"
                ),
                ui.div(
                    ui.h4("Répartition des Mots les plus Fréquents", class_="text-lg font-semibold mb-2 text-center"),
                    ui.img(src=word_freq_graph_pie_chart, class_="w-full max-w-3xl mx-auto"),
                    class_="bg-gray-50 p-4 rounded-lg mb-4 border-2 shadow-md"
                ),
                class_="flex gap-2" 
            ),
            ui.div(
                ui.h4("Boxplot des Distances", class_="text-lg font-semibold mb-2 text-center"),
                ui.div(
                    ui.img(src=distance_boxplot, class_="w-full max-w-3xl mx-auto"),
                    ui.p("Le boxplot des distances (entre phrases) représente la distribution des distances entre les différentes paires de phrases dans un espace vectoriel. Il permet de visualiser la similarité entre les phrases en utilisant une mesure de distance spécifique. Cela signifie que plus les phrases sont proches de 0 plus elles sont similaires."),
                    class_="flex gap-2 text-gray-600 text-justify pr-2 items-center",
                ),
                class_="bg-gray-50 p-4 rounded-lg mb-4 border-2 shadow-md"
                ),
            ui.div(
                ui.h4("Boxplot des fréquences des mots par phrase", class_="text-lg font-semibold mb-2 text-center"),
                ui.div(
                    ui.p("Le boxplot des fréquences des mots par phrase représente la distribution des fréquences des mots dans chaque phrase. Il permet de visualiser la variabilité des fréquences des mots dans les phrases du corpus. On peut donc observer si les phrases sont plus ou moins homogènes, courtes ou longues."),
                    ui.img(src=plot_number_of_words_boxplot(corpus_sans_poc), class_="w-full max-w-3xl mx-auto"),
                    class_="flex gap-2 text-gray-600 text-justify pr-2 items-center",
                ),
                class_="bg-gray-50 p-4 rounded-lg mb-4 border-2 shadow-md"
            ),
        )

app = App(app_ui, server)  

if __name__ == "__main__":
    app.run()