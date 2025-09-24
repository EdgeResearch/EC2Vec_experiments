import pandas as pd
from transformers import pipeline
import os
import re
from tqdm import tqdm  # Per la barra di progresso
import sys
from Delivery.declarations import echo, non_echo


def classify_emotions(input_csv, output_csv, text_column_name):
    # Carica il file CSV
    df = pd.read_csv(input_csv)

    # Controlla che la colonna "body" esista
    if text_column_name not in df.columns:
        raise ValueError('Il file CSV deve contenere una colonna chiamata '+text_column_name)

    # Carica il modello di Hugging Face
    classifier = pipeline(
        "text-classification",
        model="SamLowe/roberta-base-go_emotions",
        top_k=None,
        truncation=True,
        max_length=512,
        device=0
    )

    # Funzione per classificare il testo e restituire un dizionario con i punteggi
    def get_emotion_scores(text):
        if not isinstance(text, str):
            print(f"Valore non stringa trovato e convertito: {text}")
            text = str(text)
        scores = classifier(text)[0]
        return {score['label']: score['score'] for score in scores}

    # Gestisci i valori NaN o non stringa nella colonna "body"
    df[text_column_name] = df[text_column_name].fillna("").astype(str)

    # Applica il classificatore ai testi nella colonna "body" con la barra di progresso
    print(f"Inizio elaborazione file: {input_csv}")
    emotion_scores = [
        get_emotion_scores(text) for text in tqdm(df[text_column_name], desc="Analizzando il file")
    ]

    # Crea un DataFrame con i punteggi per ogni emozione
    emotion_df = pd.DataFrame(emotion_scores)

    # Aggiungi una colonna numerica progressiva chiamata "row"
    emotion_df.insert(0, "row", range(1, len(emotion_df) + 1))

    # Salva il nuovo DataFrame in un file CSV
    emotion_df.to_csv(output_csv, index=False)
    print(f"File salvato con successo in {output_csv}")


def process_files_emotions(file_list, folder_type):
    # Impostazione delle cartelle di input e output in base alla scelta
    if folder_type == "echo":
        input_folder = "Delivery/2_Filtered_Data_Datetime/echo_filtered_data"
        output_folder = "Delivery/3_Outputs/3.1_Emotions_datetime/echo_fd_emotions"
    elif folder_type == "nonecho":
        input_folder = "Delivery/2_Filtered_Data_Datetime/non_echo_filtered_data"
        output_folder = "Delivery/3_Outputs/3.1_Emotions_datetime/non_echo_fd_emotions"
    else:
        raise ValueError("Il tipo di folder deve essere 'echo' o 'nonecho'")

    updated_file_list = [item.replace("reddit_data", "reddit_filteredData") for item in file_list]

    # Controlla che i file esistano nella cartella
    for file_name in updated_file_list:
        input_file = os.path.join(input_folder, file_name)
        if not os.path.exists(input_file):
            print(f"Errore: il file {file_name} non esiste nella cartella {input_folder}")
            continue

        # Estrai tutto ciò che segue "reddit_filteredData_" e rimuovi l'estensione ".csv"
        base_name = re.sub(r'^reddit_filteredData_', '', file_name).replace(".csv", "")

        # Crea il percorso del file di output
        output_file = os.path.join(output_folder, f"output_{base_name}.csv")

        # Controlla se il file di output esiste già
        if os.path.exists(output_file):
            print(f"Attenzione: il file di output {output_file} esiste già. Skipping...")
            continue

        # Esegui la funzione di classificazione
        classify_emotions(input_file, output_file, "body")



if __name__ == "__main__":
    data_type = "echo" # O "nonecho"

    echo = ['reddit_data_flatearth.csv']

    print("--- Step 1: Filtraggio dei dati ---")
    process_files_emotions(echo, data_type)
