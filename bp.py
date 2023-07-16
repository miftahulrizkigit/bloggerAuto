# importing Flask and other modules
import openai
import sys
import json
from duckduckgo_search import DDGS
from oauth2client import client
from googleapiclient import sample_tools
import time

openai.api_key = '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'




bukuJudul = [
    "Ayat-Ayat Cinta - Habiburrahman El-Shirazy",
    "Dilan 1990 - Pidi Baiq",
    "Bumi Manusia - Pramoedya Ananta Toer",
    "Tenggelamnya Kapal Van Der Wijck - Hamka",
    "Ronggeng Dukuh Paruk - Ahmad Tohari",
    "Sang Pemimpi - Andrea Hirata",
    "Perahu Kertas - Dee Lestari",
    "Pulang - Leila S. Chudori",
    "Sang Alkemis - Paulo Coelho",
    "Harry Potter - J.K. Rowling (Terjemahan)",
    "Ayah - Andrea Hirata",
    "Lelaki Harimau - Eka Kurniawan",
    "Pramoedya Ananta Toer: Antologi Cerpen",
    "Garis Waktu - Fiersa Besari",
    "Cinta di Dalam Gelas - Andrea Hirata",
    "Negeri Para Bedebah - Tere Liye",
    "Si Anak Singkong - Chairul Tanjung",
    "Matilda - Roald Dahl"
]
for buku in bukuJudul:
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
  messages = [{
      "role": "system",
      "content": "kamu adalah penulis resensi/review buku yang sangat hebat."
  }, {
      "role": "user",
      "content": f"Saya ingin Anda menulis sebuah artikel dengan judul 'Review Buku {buku}', yang dibagi menjadi 6 heading yaitu Pendahuluan(1000 kata),Biografi Pengarang(500 kata),sinopsis{buku},rangkuman{buku},Kelebihan dan kekurangan {buku}(1000 kata),Rekomendasi(500 kata)Kesimpulan(500 kata).Jumlah Kata Minimal 2000 Buat dalam format html dimulai dari <h2>,"
  }]

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
              "title": f'review buku {buku}',
              "content": f'<div style="text-align: center;"><img src="{gambar}" alt="{buku}" height="400" width="auto"></div>\n{contentJadi}',
              "labels": {buku}
          }

          posts.insert(blogId='172644980291778343', body=blogContent, isDraft=False).execute()
          print(f"masuk {buku}")
          time.sleep(20)
          
      except:
          print(
              "The credentials have been revoked or expired, please re-run"
              "the application to re-authorize"
          )

if __name__ == "__main__":
    main(sys.argv)
