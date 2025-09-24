import pandas as pd
import matplotlib.pyplot as plt


# Funzione per creare il boxplot
def create_boxplot(file_name):
    # Percorso del file di input
    input_file = f"Delivery/3_Outputs/3.3_Similarity_Matrix/{file_name}" #aggiungi all'occorrenza .csv

    # Carica il file CSV
    data = pd.read_csv(input_file)

    # Rimuovi la colonna 'file_name' se presente
    data = data.drop(['file_name'], axis=1)

    # Impostazioni predefinite per titolo e etichette asse X/Y
    title = ''
    xlabel = ''

    # Condizione per determinare il tipo di file e modificare il titolo e l'asse X
    if 'echoXecho' in file_name:
        title = 'Echo-Echo'
        xlabel = 'Echo_Chambers'
    elif 'echoXnonecho' in file_name:
        title = 'Echo-Non_Echo'
        xlabel = 'Echo_Chambers'
    elif 'nonechoXnonecho' in file_name:
        title = 'Non_Echo-Non_Echo'
        xlabel = 'Reddit_Channels'

    # Crea il boxplot
    fig1, ax1 = plt.subplots()
    ax1.set_title(title)
    ax1.boxplot(data)
    ax1.set_xticklabels(list(data.columns), rotation=90, fontsize=8)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel('Cosine Similarity Distributions')

    # Salva il grafico
    output_file = f"Delivery/3_Outputs/3.5_Plots/boxplot_{file_name}.png"
    fig1.savefig(output_file, bbox_inches='tight')

    # Mostra il grafico
    plt.show()
    print(f"Grafico salvato in: {output_file}")
