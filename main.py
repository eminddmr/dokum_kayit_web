from flask import Flask, render_template, request, redirect
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)

# Google Sheets bağlantısı
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("dokum_kayit").sheet1  # Sheet adını gerektiğinde değiştir

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dokum_no = request.form["dokum_no"]
        alasim = request.form["alasim"]
        sicaklik = request.form["sicaklik"]
        kalip = request.form["kalip"]
        notlar = request.form["notlar"]

        sheet.append_row([tarih, dokum_no, alasim, sicaklik, kalip, notlar])
        return redirect("/")
    return render_template("form.html")
