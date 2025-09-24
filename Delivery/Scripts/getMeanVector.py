import pandas as pd
import os
import sys

# Funzione per generare il nome del file di output (senza timestamp)
def generate_output_filename(base_path, folder_type):
    if folder_type == "echo":
        return f"{base_path}_echo.csv"
    elif folder_type == "nonecho":
        return f"{base_path}_non_echo.csv"
    else:
        raise ValueError("Il tipo di folder deve essere 'echo' o 'nonecho'")

# Funzione principale per processare i file
def process_files_meanvector(file_list, folder_type):
    # Cartelle di input e output
    if folder_type == "echo":
        input_folder = "Delivery/3_Outputs/3.1_Emotions/echo_fd_emotions"
    elif folder_type == "nonecho":
        input_folder = "Delivery/3_Outputs/3.1_Emotions/non_echo_fd_emotions"
    else:
        raise ValueError("Il tipo di folder deve essere 'echo' o 'nonecho'")

    output_folder = "Delivery/3_Outputs/3.2_Mean_Vector/"  # Cartella dei file di output

    # Genera il nome del file di output in base al tipo di "echo" o "nonecho"
    output_file = generate_output_filename(output_folder + "meanVector", folder_type)

    # Elimina il file di output esistente (se presente)
    if os.path.exists(output_file):
        os.remove(output_file)

    # Aggiorna i nomi dei file per riflettere la struttura corretta
    updated_file_list = [item.replace("reddit_data", "output") for item in file_list]

    # Processa i file nella lista
    for file in updated_file_list:
        file_path = os.path.join(input_folder, file)  # Percorso del file di input
        if os.path.exists(file_path):
            print(f"Elaborando il file: {file}")
            data = pd.read_csv(file_path)

            # Calcola le medie per ciascuna colonna numerica
            mean_values = data.mean(numeric_only=True)

            # Crea un nuovo DataFrame con una sola riga
            mean_row = mean_values.to_frame().T

            # Rinomina la colonna `row` in `file_name` se esiste, altrimenti aggiungi la colonna
            if 'row' in data.columns:
                mean_row = mean_row.rename(columns={'row': 'file_name'})

            # Se la colonna `file_name` non esiste già, aggiungila al DataFrame
            if 'file_name' not in mean_row.columns:
                mean_row.insert(0, 'file_name', file)
            else:
                mean_row['file_name'] = file

            # Scrive nel file di output, aggiungendo i dati in modalità append
            if not os.path.exists(output_file):
                # Se il file non esiste, crea un nuovo file CSV con l'header
                mean_row.to_csv(output_file, index=False)
            else:
                # Aggiunge i dati in modalità append senza duplicare l'header
                mean_row.to_csv(output_file, mode='a', index=False, header=False)
        else:
            print(f"Errore: il file {file} non esiste nella cartella {input_folder}")
