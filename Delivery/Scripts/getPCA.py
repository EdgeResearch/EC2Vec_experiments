import pandas as pd
from sklearn.decomposition import PCA
from datetime import datetime

# Funzione per applicare la PCA
def perform_pca(input_file, output_file, n_components=None):
    """
    Applica la PCA a un dataset CSV e salva i risultati.

    Args:
        input_file (str): Percorso del file CSV di input.
        output_file (str): Percorso del file CSV di output.
        n_components (int, opzionale): Numero di componenti principali da mantenere.
                                       Se None, usa tutte le componenti.
    """
    # Carica i dati
    data = pd.read_csv(input_file)

    # Rimuove la colonna di identificazione
    if "file_name" in data.columns:
        file_names = data["file_name"]
        data = data.drop(columns=["file_name"])
    else:
        file_names = None

    # Verifica che tutti i dati rimanenti siano numerici
    if not all(data.dtypes.apply(lambda dtype: pd.api.types.is_numeric_dtype(dtype))):
        raise ValueError("Il dataset contiene colonne non numeriche dopo aver rimosso 'file_name'. Verifica i dati.")

    # Applica la PCA
    pca = PCA(n_components=n_components)
    pca_results = pca.fit_transform(data)

    # Crea un DataFrame con i risultati
    pca_df = pd.DataFrame(
        pca_results,
        columns=[f"PC{i + 1}" for i in range(pca_results.shape[1])]
    )

    # Reinserisce i file_name, se presenti
    if file_names is not None:
        pca_df.insert(0, "file_name", file_names)

    # Salva i risultati in un file CSV
    pca_df.to_csv(output_file, index=False)
    print(f"File salvato in: {output_file}")

    # Stampa informazioni sulla varianza spiegata
    explained_variance = pca.explained_variance_ratio_
    #print("Varianza spiegata per componente principale:", explained_variance)
    #print("Varianza cumulativa spiegata:", explained_variance.cumsum())


def process_pca(file_type, n_components=None):
    """
    Determina il file di input e applica la PCA in base al tipo di dato.

    Args:
        file_type (str): Tipo di file ('echo' o 'nonecho').
        n_components (int, opzionale): Numero di componenti principali da mantenere.
                                       Se None, usa tutte le componenti.
    """
    # Determina il file di input in base alla stringa "echo" o "nonecho"
    if file_type == "echo":
        input_file = "Delivery/3_Outputs/3.2_Mean_Vector/meanVector_echo.csv"
        output_base = "Delivery/3_Outputs/3.4_PCA/pca_echo_results"
    elif file_type == "nonecho":
        input_file = "Delivery/3_Outputs/3.2_Mean_Vector/meanVector_non_echo.csv"
        output_base = "Delivery/3_Outputs/3.4_PCA/pca_nonecho_results"
    else:
        raise ValueError("file_type deve essere 'echo' o 'nonecho'")

    # Genera il timestamp
    timestamp = datetime.now().strftime("%d%m%y_%H%M")  # Formato DDMMYY_HHMM

    # Crea il nome del file di output con timestamp
    output_file = f"{output_base}_{timestamp}.csv"

    # Esegui la PCA
    perform_pca(input_file, output_file, n_components)
