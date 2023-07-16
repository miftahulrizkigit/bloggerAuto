
# importing Flask and other modules
from flask import Flask, request, render_template
import openai
import sys
import json
from duckduckgo_search import DDGS
from oauth2client import client
from googleapiclient import sample_tools
import time

openai.api_key = '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'

bukuJudul = [
    "The Help",
    "The Book Thief",
    "The Secret Life of Bees",
    "The Picture of Dorian Gray",
    "The Giver",
    "A Game of Thrones",
    "The Maze Runner",
    "The Girl with the Dragon Tattoo",
    "Lord of the Flies",
    "The Outsiders",
    "The Diary of a Young Girl",
    "The Hitchhiker's Guide to the Galaxy",
    "Wuthering Heights",
    "The Fault in Our Stars",
    "The Sun Also Rises",
    "One Hundred Years of Solitude",
    "The Adventures of Tom Sawyer",
    "The Picture of Dorian Gray",
    "Moby-Dick",
    "Jane Eyre",
    "The Scarlet Letter",
    "Frankenstein",
    "The Count of Monte Cristo",
    "Crime and Punishment",
    "The Odyssey",
    "Don Quixote",
    "Les Misérables",
    "War and Peace",
    "The Brothers Karamazov",
    "Anna Karenina",
    "A Tale of Two Cities",
    "The Divine Comedy",
    "The Iliad",
    "Sense and Sensibility",
    "The Adventures of Huckleberry Finn",
    "Great Expectations",
    "Little Women",
    "Treasure Island",
    "Dracula",
    "The Call of the Wild",
    "Pride and Prejudice",
    "Sense and Sensibility",
    "Emma",
    "Northanger Abbey",
    "Persuasion",
    "The Phantom of the Opera",
    "The Adventures of Sherlock Holmes",
    "The Hound of the Baskervilles",
    "Alice's Adventures in Wonderland",
    "Through the Looking-Glass",
    "The War of the Worlds",
    "Around the World in Eighty Days",
    "Twenty Thousand Leagues Under the Sea",
    "The Time Machine",
    "The Jungle Book",
    "The Wonderful Wizard of Oz",
    "The Adventures of Pinocchio",
    "Robinson Crusoe",
    "Gulliver's Travels",
    "The Three Musketeers",
    "Swiss Family Robinson",
    "The Legend of Sleepy Hollow",
    "Anne of Green Gables",
    "The Little Prince",
    "Around the World in Eighty Days",
    "The Count of Monte Cristo",
    "The Adventures of Tom Sawyer",
    "The Secret Garden",
    "The War of the Worlds",
    "Winnie-the-Pooh",
    "The Wind in the Willows",
    "The Chronicles of Narnia",
    "Charlie and the Chocolate Factory",
    "Matilda",
    "The BFG",
    "James and the Giant Peach",
    "Alice's Adventures in Wonderland",
    "The Call of the Wild",
    "White Fang",
    "The Secret Life of Bees",
    "The Color Purple",
    "The Help",
    "The Book Thief",
    "The Fault in Our Stars",
    "A Man Called Ove",
    "Educated",
    "The Girl on the Train",
    "Gone Girl",
    "Big Little Lies",
    "Crazy Rich Asians",
    "The Silent Patient",
    "Where the Crawdads Sing",
    "Normal People",
    "The Tattooist of Auschwitz",
    "Becoming"
]



def create_blog_post(buku):
    judul = f'review buku {buku}'

    with DDGS() as ddgs:
        keywords = f'cover buku {buku}'
        ddgs_images_gen = ddgs.images(
            keywords,
            region="id-id",
            safesearch="Off",
            size="Large",
            color=None,
            type_image=None,
            layout=None,
            license_image=None,
        )
        for r in ddgs_images_gen:
            urlGambar = r['image']
            break

    gambar = urlGambar

    # Menginisialisasi daftar pesan
    messages = [
        {
            "role": "system",
            "content": "kamu adalah penulis resensi/review buku yang sangat hebat."
        },
        {
            "role": "user",
            "content": f"Saya ingin Anda menulis sebuah artikel dengan judul {judul}, yang dibagi menjadi 6 heading yaitu Pendahuluan(1000 kata),Biografi Pengarang(500 kata),sinopsis{buku},rangkuman{buku},Kelebihan dan kekurangan {buku}(1000 kata),Rekomendasi(500 kata)Kesimpulan(500 kata).Jumlah Kata Minimal 2000 Buat dalam format html dimulai dari <h2>,"
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        max_tokens=15000,
        temperature=0.8,
        messages=messages,
        stop="STOP"
    )

    # mengubah openaiobj menjadi dictionary
    contentOpenAiObj = list(response.choices)[0]

    # mengambil konten dari open ai
    contentJadi = contentOpenAiObj['message']['content']

    # Fungsi untuk menyisipkan pos baru
    def main(argv):
        # Authenticate and construct service.
        service, flags = sample_tools.init(
            argv,
            "blogger",
            "v3",
            __doc__,
            __file__,
            scope="https://www.googleapis.com/auth/blogger",
        )

        try:
            posts = service.posts()

            blogContent = {
                "title": judul,
                "content": f'<div style="text-align: center;"><img src="{gambar}" alt="{judul}" height="400" width="auto"></div>\n{contentJadi}',
                "labels": judul
            }

            response = posts.insert(blogId='172644980291778343', body=blogContent, isDraft=False).execute()
            url = response['url']
            titleResp = response['title']

            with open('urls.txt', 'a') as file:
                file.write(f"{url}\n")
            with open('judul.txt', 'a') as life:
                life.write(f"{titleResp}\n")            

        except client.AccessTokenRefreshError:
            print(
                "The credentials have been revoked or expired, please re-run"
                "the application to re-authorize"
            )

    print(f"masuk {buku}")

    if __name__ == "__main__":
        main(sys.argv)

    # Mengatur jeda selama 20 detik
    time.sleep(20)

# Loop melalui daftar judul buku
for buku in bukuJudul:
    create_blog_post(buku)