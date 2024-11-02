from shiny import App, ui, render, reactive
import pandas as pd
from lib import *

app_ui = ui.page_fluid(
    ui.tags.head(
        ui.tags.link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css"),
        ui.tags.link(rel="stylesheet", href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"),
        ui.tags.style("""
            html { margin: 0; padding: 0; }
            main { margin: 0; padding: 0; }
            body { margin: 0; padding: 0; }
            .sidebar { height: 100vh; overflow-y: auto; }
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
        """)
    ),
    ui.div(
        # Sidebar
        ui.div(
            ui.h2("Menu", class_="text-2xl font-bold mb-4 border-b border-gray-300 pb-3"),
            ui.input_select("lang_select", "", choices={"Français": "Français", "English": "English"}, selected="Français"),
            ui.p("Descripteur", class_="mt-4"),
            ui.input_select("choix1", "", choices={"1": "Binaire", "2": "Occurrence", "3": "Normalisé", "4":"Probabilité","5":"TF-IDF Binaire","6":"TF-IDF Normalisé", "7":"TF-IDF Occurence","8":"TF-IDF new"}, selected="1"),
            ui.p("Distance", class_="mt-4"),
            ui.input_select("choix2", "", choices={"Euclidienne": "Euclidienne", "Manhattan": "Manhattan", "Cosinus": "Cosinus","Hamming":"Hamming","Curtis":"Curtis","Jacard":"Jacard","Kullback":"Kullback"}, selected="Euclidienne"),
            ui.input_file("file_input", "Déposer un fichier ici ou cliquer pour sélectionner un fichier", multiple=False),
            ui.input_action_button("generate", "Generate", class_="mt-4 w-full bg-black text-white py-2 px-4 rounded"),
            class_="w-1/5 bg-gray-50 p-4 sidebar"
        ),
        # Main content
        ui.div(
            ui.output_ui("content"),
            class_="w-4/5 p-8 main-content"
        ),
        class_="flex"
    )
)

def style_dataframe(df):
    return df.style.set_table_attributes('class="table-auto w-full border-collapse border border-gray-200"') \
                   .set_properties(**{'border': '1px solid black'}) \
                   .background_gradient(cmap='viridis', low=0, high=1)

def server(input, output, session):
    lang = reactive.Value("Français")

    @reactive.Effect
    @reactive.event(input.lang_select)
    def update_lang():
        lang.set(input.lang_select())

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
        phrases = split_doc_mot(corpus_sans_poc)
        liste_mots = retirer_doublons(split_doc_mot(phrases))

        descripteur = "binaire" if input.choix1() == "1" else "occurrence"
        list_mot = split_doc_mot(phrases)
        if input.choix1() == "1":
            list_backbofwords = backbofwordsBinaire(corpus_sans_poc, liste_mots)
        elif input.choix1() == "2":
            list_backbofwords = backbofwords_occurence(corpus_sans_poc, liste_mots)
        elif input.choix1() == "3":
            list_backbofwords = matrix_backbofwords_normalize_Norme(corpus_sans_poc, liste_mots)
        elif input.choix1() == "4":
            list_backbofwords = matrix_backbofwords_normalize_proba(corpus_sans_poc, liste_mots)
        elif input.choix1() == "5":
            list_backbofwords = tf_idf_bin(corpus_sans_poc, liste_mots)
        elif input.choix1() == "6":
            list_backbofwords = tf_idf_norm(corpus_sans_poc, liste_mots)
        elif input.choix1() == "7":
            list_backbofwords = tf_idf_occ(corpus_sans_poc, liste_mots)
        else:
            list_backbofwords = tf_idf_new(corpus_sans_poc, liste_mots)

        distance = input.choix2()

        if distance == "Euclidienne":
            distance_matrix = matrix_distance_Euclidienne(list_backbofwords)
        elif distance == "Cosinus":
            distance_matrix = matrice_distance_cosinus(list_backbofwords)
        elif distance == "Hamming":
            distance_matrix = matrice_distance_hamming(list_backbofwords)
        elif distance == "Jacard":
            distance_matrix = matrice_distance_jacard(list_backbofwords)
        elif distance == "Curtis":
            distance_matrix = matrice_distance_bray_curtis(list_backbofwords)
        elif distance == "Kullback":
            distance_matrix = matrice_kullback_leibler(list_backbofwords)
        else:
            distance_matrix = matrix_distance_Manhattan(list_backbofwords)

        # Convertir les matrices en DataFrames pandas
        backofword = pd.DataFrame(list_backbofwords)
        distance_df = pd.DataFrame(distance_matrix)

        # Styliser les DataFrames
        backofword_styled = style_dataframe(backofword).to_html()
        distance_df_styled = style_dataframe(distance_df).to_html()

        return ui.div(
            ui.h3("Résultats de l'analyse", class_="text-2xl font-bold mb-4"),
            ui.div(
                ui.p(ui.strong("Fichier analysé : "), uploaded_file['name']),
                ui.p(ui.strong("Descripteur : "), descripteur),
                ui.p(ui.strong("Distance : "), distance),
                class_="mb-4"
            ),
            ui.div(
                ui.h4("Matrice backofword", class_="text-lg font-semibold mb-2"),
                ui.HTML(backofword_styled),
                class_="mb-4 overflow-x-auto"
            ),
            ui.div(
                ui.h4("Matrice de distance", class_="text-lg font-semibold mb-2"),
                ui.HTML(distance_df_styled),
                class_="mb-4 overflow-x-auto"
            )
        )

app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
