from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
import pandas as pd
from datetime import datetime
import os
import sys

# Funzione principale per calcolare la cosine similarity
def calculate_similarity(file_type1, file_type2):
    # Definire i percorsi dei file in base al tipo di input
    if file_type1 == "echo":
        file1 = "Delivery/3_Outputs/3.2_Mean_Vector/meanVector_echo.csv"
    elif file_type1 == "nonecho":
        file1 = "Delivery/3_Outputs/3.2_Mean_Vector/meanVector_non_echo.csv"
    else:
        raise ValueError("file_type1 deve essere 'echo' o 'nonecho'")

    if file_type2 == "echo":
        file2 = "Delivery/3_Outputs/3.2_Mean_Vector/meanVector_echo.csv"
    elif file_type2 == "nonecho":
        file2 = "Delivery/3_Outputs/3.2_Mean_Vector/meanVector_non_echo.csv"
    else:
        raise ValueError("file_type2 deve essere 'echo' o 'nonecho'")

    # Controllare se i file esistono
    if not os.path.exists(file1):
        raise FileNotFoundError(f"Il file {file1} non esiste.")
    if not os.path.exists(file2):
        raise FileNotFoundError(f"Il file {file2} non esiste.")

    # Lettura dei file
    echo_data = pd.read_csv(file1)
    non_echo_data = pd.read_csv(file2)

    # Filtrare le righe da escludere (se necessario)
    filtered_echo_data = echo_data
    filtered_non_echo_data = non_echo_data

    # Estrarre i nomi dei file
    echo_names = filtered_echo_data['file_name']
    non_echo_names = filtered_non_echo_data['file_name']

    # Estrarre solo i vettori emozionali (escludendo 'file_name')
    echo_vectors = filtered_echo_data.drop(columns=['file_name']).values
    non_echo_vectors = filtered_non_echo_data.drop(columns=['file_name']).values

    # Normalizzare i vettori
    echo_vectors = normalize(echo_vectors, axis=1)  # Normalizzazione per ogni vettore (asse 1 = righe)
    non_echo_vectors = normalize(non_echo_vectors, axis=1)

    # Calcolare la matrice di cosine similarity
    similarity_matrix = cosine_similarity(echo_vectors, non_echo_vectors)

    # Creare un DataFrame per aggiungere i nomi dei file
    similarity_df = pd.DataFrame(similarity_matrix, index=echo_names, columns=non_echo_names)

    # Generare il timestamp
    timestamp = datetime.now().strftime("%d%m%y_%H%M")  # Formato DDMMYY_HHMM

    # Definire il nome del file di output in base al tipo di file (echo o nonecho) e aggiungere il timestamp
    output_file_name = f'Delivery/3_Outputs/3.3_Similarity_Matrix/similarity_matrix_{file_type1}X{file_type2}_{timestamp}.csv'

    # Salvataggio del risultato
    similarity_df.to_csv(output_file_name)

    # Mostrare il risultato
    #print("Matrice di cosine similarity calcolata:")
    #print(similarity_df)
    print(f"La matrice è stata salvata in: {output_file_name}")

    file_name_only = os.path.basename(output_file_name)
    return file_name_only