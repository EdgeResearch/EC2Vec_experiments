import pandas as pd
import re
import os
from Delivery.declarations import echo, non_echo


# Funzione per verificare se la riga deve essere rimossa
def is_removable(text):
    """
    Determina se una riga deve essere rimossa in base a determinati criteri.
    - Rimuove spazi e punteggiatura dal testo.
    - Esclude testi con meno di 3 parole o che corrispondono a determinati termini.

    Args:
        text (str): Il testo da valutare.

    Returns:
        bool: True se la riga deve essere rimossa, False altrimenti.
    """
    clean_text = re.sub(r'[^\w\s]', '', str(text)).strip()
    return (clean_text in ["removed", "deleted"] or
            len(clean_text.split()) <= 2)

# Funzione per determinare i percorsi di input e output in base al tipo ('echo' o 'nonecho')
def determine_paths(data_type):
    """
    Determina i percorsi di input e output in base al tipo di dati ('echo' o 'nonecho').

    Args:
        data_type (str): Tipo di dati, può essere 'echo' o 'nonecho'.

    Returns:
        tuple: (input_path, output_path)
    """
    if data_type == "echo":
        input_folder = "Delivery/1_Non_Filtered_Data_Datetime/echo_data"
        output_folder = "Delivery/2_Filtered_Data_Datetime/echo_filtered_data"
    elif data_type == "nonecho":
        input_folder = "Delivery/1_Non_Filtered_Data_Datetime/non_echo_data"
        output_folder = "Delivery/2_Filtered_Data_Datetime/non_echo_filtered_data"
    else:
        raise ValueError(f"Tipo di dati non valido: {data_type}. Deve essere 'echo' o 'nonecho'.")

    return input_folder, output_folder

# Funzione principale per filtrare i dati
def filter_data(file_list, data_type):
    """
    Filtra i file CSV specificati e salva i risultati filtrati nelle cartelle corrette.
    Prima verifica se il file di output esiste già.

    Args:
        file_list (list of str): Elenco dei nomi dei file CSV da processare.
        data_type (str): Tipo di dati, può essere 'echo' o 'nonecho'.
    """
    # Determina i percorsi di input e output in base al tipo
    input_folder, output_folder = determine_paths(data_type)

    # Assicura che la cartella di output esista
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in file_list:
        input_file = os.path.join(input_folder, file_name)

        # Estrai tutto ciò che segue "reddit_data_" e rimuovi l'estensione ".csv"
        base_name = re.sub(r'^reddit_data_', '', file_name).replace(".csv", "")

        # Crea il percorso del file di output
        output_file = os.path.join(output_folder, f"reddit_filteredData_{base_name}.csv")

        # Controlla se il file di input esiste
        if not os.path.exists(input_file):
            print(f"Errore: il file {file_name} non esiste nel percorso {input_file}")
            continue

        # Verifica se il file di output esiste già
        if os.path.exists(output_file):
            print(f"Attenzione: il file di output {output_file} esiste già. Skipping...")
            continue

        # Carica il file CSV
        try:
            df = pd.read_csv(input_file)
        except Exception as e:
            print(f"Errore nel caricamento del file {file_name}: {e}")
            continue

        # Verifica la presenza della colonna 'body'
        if 'body' not in df.columns:
            print(f"Errore: la colonna 'body' non è presente nel file {file_name}.")
            continue

        # Filtra il dataframe
        filtered_df = df[~df['body'].apply(is_removable)]

        # Assicurati che la cartella di output esista
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Salva il file filtrato
        try:
            filtered_df.to_csv(output_file, index=False)
            print(f"File filtrato salvato in: {output_file}")
        except Exception as e:
            print(f"Errore nel salvataggio del file filtrato {output_file}: {e}")


if __name__ == "__main__":
    data_type = "nonecho" # O "nonecho"

    print("--- Step 1: Filtraggio dei dati ---")
    filter_data(non_echo, data_type)