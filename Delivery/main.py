import os

from Delivery.Scripts.filterData import filter_data
from Delivery.Scripts.getBoxPlot import create_boxplot
from Delivery.Scripts.getEmotion import process_files_emotions
from Delivery.Scripts.getMeanVector import process_files_meanvector
from Delivery.Scripts.getCosineSimilarity import calculate_similarity
from Delivery.Scripts.getPCA import process_pca
from Delivery.Scripts.getScatterPlot import plot_pca
from declarations import echo_all, non_echo_all

# Funzione principale
def main():
    data_type = "echo" # O "nonecho"

    print("--- Step 1: Filtraggio dei dati ---")
    #filter_data(echo, data_type)

    print("--- Step 2: Calcolo delle emozioni ---")
    #process_files_emotions(echo, data_type)

    print("--- Step 3: Calcolo dei vettori medi ---")
    process_files_meanvector(echo_all,data_type)
    process_files_meanvector(non_echo_all, "nonecho")

    print("--- Step 4: Calcolo delle matrici di similarità ---")
    #echoXecho = calculate_similarity("echo","echo")
    #echoXnonecho = calculate_similarity("echo","nonecho")
    #nonechoXnonecho = calculate_similarity("nonecho","nonecho")

    print("--- Step 5: Calcolo della PCA ---")
    #process_pca(data_type)

    print("--- Step 6: Salvataggio Grafici ScatterPlot ---")
    #plot_pca("2D")
    #plot_pca("3D")

    print("--- Step 7: Salvataggio Grafici BoxPlot ---")
    #create_boxplot(echoXecho)
    #create_boxplot(echoXnonecho)
    #create_boxplot(nonechoXnonecho)


if __name__ == "__main__":
    main()
