from flask import Flask, render_template, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)

# Google Sheets bağlantısı için ayar
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("dokum_kayit").sheet1  # Google Sheet adı

def analiz_et_kalip_matrisi(dizi):
    values = dizi.split(",")
    toplam = 42
    hatalilar = [i for i, val in enumerate(values) if val == "1"]
    basarili_sayisi = toplam - len(hatalilar)
    oran = f"{basarili_sayisi}/{toplam}"

    # Başarısız kalıpların koordinatlarını A1, B2 gibi bul
    koordinatlar = []
    for i in hatalilar:
        satir = i // 7 + 1
        sutun = chr(ord("A") + i % 7)
        koordinatlar.append(f"{satir}{sutun}")

    return oran, ", ".join(koordinatlar)

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        tarih = request.form.get("tarih")
        dokum_no = request.form.get("dokum_no")
        alasim = request.form.get("alasim")
        sicaklik = request.form.get("sicaklik")
        notlar = request.form.get("notlar")
        kalip_dizisi = request.form.get("kalip")

        oran, hatali_kaliplar = analiz_et_kalip_matrisi(kalip_dizisi)

        sheet.append_row([tarih, dokum_no, alasim, sicaklik, oran, hatali_kaliplar, notlar])
        return "Kayıt başarıyla eklendi!"

    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)