# EC2Vec_experiments

This project analyzes **Reddit subreddit content through emotion features** to (1) **discover clusters** of related discussions and (2) **classify** subreddit as **conspiracy vs. non-conspiracy** using **Logistic Regression (LR)** and a **Multi-Layer Perceptron (MLP)**.  
The notebook is cleaned for presentation.

---

## ✨ What this project does

- **Data prep**: load subreddit posts/comments, clean text (tokenize, lowercase, remove stopwords).
- **Emotion features**: map each text to an **emotion vector** (e.g., joy, anger, fear, sadness, trust, anticipation, surprise, disgust) via lexicon or classifier.
- **Unsupervised**: reduce dimensionality with **PCA**, cluster with **K-Means / DBSCAN / Hierarchical**; evaluate with **Silhouette**, **Davies–Bouldin**, **Calinski–Harabasz**.
- **Supervised**: train **LR** and **MLP** on emotion features; report **accuracy, precision, recall, F1**.
- **Visualization**: plot clusters and class separation; inspect emotion profiles of conspiratorial communities.

---

## 📁 Files

- `research_results.ipynb` — main, presentation-ready notebook.

> Bring your own dataset of subreddit texts (CSV/JSON). The notebook expects columns like `text` (content) and, for supervised tasks, a binary label such as `is_conspiracy` (0/1).

---

## 📦 Installation (pipenv)

Install **pipenv** if you don’t have it:

```bash
pip install pipenv

