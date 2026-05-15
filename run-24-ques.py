# https://docs.google.com/forms/u/0/d/e/1FAIpQLSddTDvp8CRhl3cWNHyaAA3Tx54yxNg-5UiKG4caqtL2kYbhTQ/formResponse

import requests
import random
import time

form_url = "https://docs.google.com/forms/u/0/d/e/1FAIpQLSeMpoSGNS-w54rq98iRN1WLAVv6YEPyF-V113dQ9A-wcihfJQ/formResponse"

names = [
    "Irfan Diansyahputra",
    "Lingqe Raja Dianda",
    "Satria Perdana",
    "Fajar Arafi",
    "Sajid Ibrahim",
    "Ilham Umam Saifullah",
    "Fajri Lucaz Jakoswa",
    "Hasnan Alfan Shuri",
    "Hendrata Putra Pratama",
    "Ridho Jayadi Saputra",
    "M Khairuman Hidayat",
    "Rifki Mahendra",
    "Al Imron",
    "Pandu Lutfiansyah",
    "Muhammad Setiawan",
    "Pippo Ariyandra",
    "Irwan Syaputra",
    "Muhammad Fauzan",
    "M. Dhio Ananda Kesuma",
    "Wanda Lestian",
    "Fajar Setiono",
    "Surya Wijaya Lie Sahar",
    "Rendy Ruzfizal",
    "Muhammad Said Ilham",
    "Rizky Wahyudi",
    "Al Fayad",
    "Ade Dimas Pribadi",
    "Ridho Anggara",
    "Yuri Heriyaldo",
    "Wawan Ananda Putra"
]

pilihan_skala = ["Ya", "Mungkin", "Cukup"]

weights_skala = [0.9, 0.04, 0]

time_gaps = [2200, 423, 3652, 60, 1232, 1643]

entry_id = {
    "nama": "entry.430814187",
    "pekerjaan": "entry.1003510170",
    "pertanyaan3": "entry.1400135330",
    "pertanyaan4": "entry.1238295085",
    "pertanyaan5": "entry.129585321",
    "pertanyaan6": "entry.2115041641",
    "pertanyaan7": "entry.1667872225",
}

form_data = {}

for nama in names:
    form_data = {
        entry_id['nama']: nama,
        entry_id['pekerjaan']: "Mahasiswa"
    }

    # Isi pertanyaan 3–23
    for q_num in range(3, 8):
        key = f"pertanyaan{q_num}"
        form_data[entry_id[key]] = random.choices(pilihan_skala, weights=weights_skala, k=1)[0]

    # Kirim POST request
    response = requests.post(form_url, data=form_data)

    time_break = random.choice(time_gaps)

    if response.status_code == 200:
        print(f"Nama diisi {nama}. ✅ Form berhasil diisi. Jeda waktu {time_break}")
    else:
        print(f"Responden {nama}. ❌ Gagal mengisi form. Status code: {response.status_code}")
        print("   Data yang dikirim:", form_data)

    # Delay biar aman
    time.sleep(time_break)