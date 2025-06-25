from flask import Flask, render_template, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Google Sheets bağlantısı
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("dokum_kayit").sheet1  # sayfa adı

# Başarı oranı ve hatalı kalıpları hesaplayan fonksiyon
def analiz_et_kalip_matrisi(matrix_str):
    values = matrix_str.split(",")
    rows, cols = 6, 7
    basarisiz = []
    basarili_sayisi = 0

    for i in range(rows):
        for j in range(cols):
            idx = i * cols + j
            if values[idx] == "1":
                basarili_sayisi += 1
            else:
                harf = chr(ord("A") + j)
                basarisiz.append(f"{i+1}-{harf}")
    
    toplam = rows * cols
    oran = f"{basarili_sayisi}/{toplam}"
    return oran, ", ".join(basarisiz)

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        dokum_no = request.form.get("dokum_no")
        alasim = request.form.get("alasim")
        sicaklik = request.form.get("sicaklik")
        notlar = request.form.get("notlar")
        kalip_dizisi = request.form.get("kalip")

        oran, hatali_kaliplar = analiz_et_kalip_matrisi(kalip_dizisi)

        sheet.append_row([
            dokum_no,
            alasim,
            sicaklik,
            notlar,
            oran,
            hatali_kaliplar
        ])

        return "Kayıt başarıyla alındı!"

    return render_template("form.html")