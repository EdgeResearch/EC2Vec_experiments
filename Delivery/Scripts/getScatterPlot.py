import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from sklearn.decomposition import PCA
from datetime import datetime

# Funzione per applicare la PCA
def perform_pca(input_file, n_components=None):
    """
    Applica la PCA a un dataset CSV e restituisce i risultati,
    escludendo righe specifiche.

    Args:
        input_file (str): Percorso del file CSV di input.
        n_components (int, opzionale): Numero di componenti principali da mantenere.
                                       Se None, usa tutte le componenti.

    Returns:
        pca_results (array): I risultati della PCA (vettori proiettati).
        explained_variance (array): La varianza spiegata da ciascuna componente principale.
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

    # Stampa informazioni sulla varianza spiegata
    explained_variance = pca.explained_variance_ratio_
    #print(f"File: {input_file}")
    #print("Varianza spiegata per componente principale:", explained_variance)
    #print("Varianza cumulativa spiegata:", explained_variance.cumsum())

    return pca_results, explained_variance

# Funzione per eseguire il plot in 2D o 3D
def plot_pca(plot_type):

    input_file_1 = "Delivery/3_Outputs/3.2_Mean_Vector/meanVector_echo.csv"
    input_file_2 = "Delivery/3_Outputs/3.2_Mean_Vector/meanVector_non_echo.csv"

    pca_results_1, explained_variance_1 = perform_pca(input_file_1)
    pca_results_2, explained_variance_2 = perform_pca(input_file_2)

    # Genera il timestamp
    timestamp = datetime.now().strftime("%d%m%y_%H%M")

    if plot_type == "2D":
        # Plot 2D
        plt.figure(figsize=(10, 8))
        plt.scatter(pca_results_1[:, 0], pca_results_1[:, 1], c='red', marker='o', label='Echo')
        plt.scatter(pca_results_2[:, 0], pca_results_2[:, 1], c='blue', marker='o', label='Non Echo')

        plt.xlabel(f'PC1')
        plt.ylabel(f'PC2')
        plt.title('Visualizzazione dei dati nelle prime due componenti principali')
        plt.legend()
        plt.grid(True)

        # Salva il grafico con il timestamp
        output_file = f"Delivery/3_Outputs/3.5_Plots/pca_scatter_plot_2D_combined_{timestamp}.png"
        plt.savefig(output_file, dpi=300)
        print(f"Grafico salvato in: {output_file}")
        plt.show()

    elif plot_type == "3D":
        # Plot 3D
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        ax.scatter(pca_results_1[:, 0], pca_results_1[:, 1], pca_results_1[:, 2], c='red', marker='o', label='Echo')
        ax.scatter(pca_results_2[:, 0], pca_results_2[:, 1], pca_results_2[:, 2], c='blue', marker='o', label='Non Echo')

        ax.set_xlabel('PC1')
        ax.set_ylabel('PC2')
        ax.set_zlabel('PC3')
        ax.set_title('Visualizzazione dei dati nelle prime tre componenti principali')
        ax.legend()
        ax.grid(True)

        # Salva il grafico con il timestamp
        output_file = f"Delivery/3_Outputs/3.5_Plots/pca_scatter_plot_3D_combined_{timestamp}.png"
        plt.savefig(output_file, dpi=300)
        print(f"Grafico salvato in: {output_file}")
        plt.show()

    else:
        raise ValueError("Il tipo di plot deve essere '2D' o '3D'.")

