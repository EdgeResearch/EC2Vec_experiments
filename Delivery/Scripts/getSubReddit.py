import praw
import csv
import os
import time
from datetime import datetime
from prawcore.exceptions import TooManyRequests
from tqdm import tqdm

# Configurazione API
reddit = praw.Reddit(
    client_id="",
    client_secret="",
    user_agent="script"
)

# Lista di subreddit
#subreddit_names = ["COVID19_5G", "AskConservatives", "vegan", "conspiracy", "atheism", "AskThe_donald", "UFOs", "flatearth"]
#subreddit_names = ["shakespeare", "AskReddit.csv", "changemyview", "CulinaryPlating", "Bible", "skeptic"]
subreddit_names = ["AskReddit"]

# Directory di output
#output_dir = "Delivery/1_Non_Filtered_Data_Datetime/echo_data/"
output_dir = "Delivery/1_Non_Filtered_Data_Datetime/non_echo_data/"
os.makedirs(output_dir, exist_ok=True)

for subreddit_name in subreddit_names:
    try:
        subreddit = reddit.subreddit(subreddit_name)
        data = []
        posts = list(subreddit.hot(limit=1000))  # Limita a 1000 post per test

        print(f"Estrazione dei post 'hot' dal subreddit r/{subreddit_name}...")
        total_posts = len(posts)

        # Contatore commenti
        comment_counter = 0

        for post in tqdm(posts, desc=f"Estrazione post da r/{subreddit_name}", unit="post", ncols=100):
            try:
                # Dettagli del post
                post_data = {
                    "type": "post",
                    "post_id": post.id,
                    "title": post.title,
                    "author": str(post.author),
                    "score": post.score,
                    "flair": post.link_flair_text or "N/A",
                    "body": post.selftext or "N/A",
                    "created_utc": datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                }
                data.append(post_data)

                # Recupera i commenti, sostituendo fino a 10 MoreComments
                post.comments.replace_more(limit=10)  # Carica fino a 10 blocchi di MoreComments
                for comment in post.comments.list():
                    if isinstance(comment, praw.models.Comment):  # Filtra solo i commenti validi
                        comment_data = {
                            "type": "comment",
                            "post_id": post.id,
                            "title": f"Commento su: {post.title}",
                            "author": str(comment.author),
                            "score": comment.score,
                            "flair": "N/A",
                            "body": comment.body,
                            "created_utc": datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                        }
                        data.append(comment_data)

                        # Incrementa il contatore
                        comment_counter += 1

                        # Pausa ogni 50 commenti
                        if comment_counter % 50 == 0:
                            time.sleep(1)

                # Pausa per evitare limiti (tra i post)
                time.sleep(1)

            except TooManyRequests:
                print("Superato il limite di richieste! Attendo 60 secondi...")
                time.sleep(60)  # Pausa più lunga in caso di errore 429
            except Exception as e:
                print(f"Errore durante l'elaborazione di un post: {e}")

        # Salvataggio in CSV
        output_file = os.path.join(output_dir, f"reddit_data_{subreddit_name}.csv")
        fields = ["type", "post_id", "title", "author", "score", "flair", "body", "created_utc"]

        with open(output_file, mode="w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fields, quoting=csv.QUOTE_MINIMAL, escapechar='\\')
            writer.writeheader()
            writer.writerows(data)

        print(f"Dati salvati in {output_file}!")

    except Exception as e:
        print(f"Errore durante l'elaborazione del subreddit r/{subreddit_name}: {e}")
