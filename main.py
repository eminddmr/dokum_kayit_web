from flask import Flask, render_template, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Google Sheets bağlantısı
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("dokum_kayit").sheet1  # sayfa adı

def analiz_et_kalip_matrisi(dizi):
    values = dizi.split(",")
    toplam = 42
    aktifler = []
    for idx in range(toplam):
        try:
            if values[idx] == "1":
                aktifler.append(idx)
        except IndexError:
            break  # Veri eksik gelirse döngüyü bitir
    basarisizlar = [i for i in range(toplam) if i not in aktifler]
    oran = f"{len(aktifler)}/{toplam}"
    koordinatlar = []
    for i in basarisizlar:
        satir = i // 7 + 1
        sutun = chr(ord("A") + i % 7)
        koordinatlar.append(f"{satir}{sutun}")
    return oran, ", ".join(koordinatlar)

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