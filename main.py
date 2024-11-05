from shiny import App, ui, render, reactive, session
import pandas as pd
from lib import *

backofword_styled = None
distance_df_styled = None

def descriptor_select_distance(choix):
    if choix == "1":
        return ["Euclidienne", "Manhattan", "Cosinus", "Curtis", "Kullback", "Jacard", "Hamming"]
    else:
        return ["Euclidienne", "Manhattan", "Cosinus", "Curtis", "Kullback"]
    
def update_constant(new_value, new_value2):
            global backofword_styled
            backofword_styled = new_value
            global distance_df_styled
            distance_df_styled = new_value2

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
            .container {
                margin-left: 0 !important;
                margin-right: 0 !important;
                padding-left: 0 !important;
                padding-right: 0 !important;
            }
            .modal {
                display: none;
                position: fixed;
                z-index: 1000;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0,0,0,0.4);
            }
            .modal-content {
                background-color: white;
                margin: 5% auto;
                padding: 20px;
                border-radius: 8px;
                width: 90%;
                max-height: 90vh;
                overflow-y: auto;
            }
            .close-modal {
                float: right;
                font-size: 28px;
                font-weight: bold;
                cursor: pointer;
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
            # Modal pour la matrice backofword
            ui.div(
                {"class": "modal", "id": "backofwordModal"},
                ui.div(
                    {"class": "modal-content"},
                    ui.span({"class": "close-modal"}, "×"),
                    ui.h4("Matrice backofword", class_="text-lg font-semibold mb-2"),
                    ui.HTML(backofword_styled),
                    ui.output_ui("backofword_matrix"),
                )
            ),
            # Modal pour la matrice de distance
            ui.div(
                {"class": "modal", "id": "distanceModal"},
                ui.div(
                    {"class": "modal-content"},
                    ui.span({"class": "close-modal"}, "×"),
                    ui.h4("Matrice de distance", class_="text-lg font-semibold mb-2"),
                    ui.output_ui("distance_matrix"),
                )
            ),
            class_="w-4/5 p-8 main-content"
        ),
        class_="flex"
    ),
)

def style_dataframe(df):
    return df.style.set_table_attributes('class="table-auto w-full border-collapse border border-gray-200"') \
           .set_properties(**{'border': '1px solid black'}) \
           .background_gradient(cmap='viridis', low=0, high=1)

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

def server(input, output, session):
    lang = reactive.Value("Français")
    phrases = reactive.Value([])
    selected_phrase_index = reactive.Value(None)
    selected_phrase_index_str = reactive.Value("0")
    matrices = reactive.Value({"backofword": None, "distance": None})

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
    @reactive.event(input.choix1)
    def update_distance_choices():
        new_choices = descriptor_select_distance(input.choix1())
        ui.update_select("choix2", choices=new_choices)

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

    @output
    @render.ui
    def backofword_matrix():
        if matrices.get()["backofword"] is not None:
            return ui.div(
                ui.HTML(matrices.get()["backofword"]),
                class_="overflow-auto"
            )
        return ui.p("Aucune matrice disponible")

    @output
    @render.ui
    def distance_matrix():
        if matrices.get()["distance"] is not None:
            return ui.div(
                ui.HTML(matrices.get()["distance"]),
                class_="overflow-auto"
            )
        return ui.p("Aucune matrice disponible")

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

        # Convert matrices to DataFrames
        backofword = pd.DataFrame(list_backbofwords)
        distance_df = pd.DataFrame(distance_matrix)
        
        update_constant(backofword, distance_df)

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
                ui.input_action_button(id="showBackofword", label="Voir matrice backofword", class_="bg-blue-500 text-white px-4 py-2 rounded mr-2 shadow-md"),
                ui.input_action_button(id="showDistance", label="Voir matrice distance", class_="bg-green-500 text-white px-4 py-2 rounded shadow-md"),
                class_="mb-4"
            )
        )
        
def style_dataframe(df):
    return df.style\
        .set_table_attributes('class="table-auto w-full border-collapse border border-gray-200"')\
        .format("{:.3f}")\
        .background_gradient(cmap='viridis', low=0, high=1)\
        .set_properties(**{
            'white-space': 'nowrap',
            'font-size': '14px',
            'text-align': 'center'
        })

app = App(app_ui, server)

if __name__ == "__main__":
    app.run()