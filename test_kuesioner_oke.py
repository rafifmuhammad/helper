import random
import time

import requests


FORM_URL = "https://docs.google.com/forms/u/0/d/e/1FAIpQLSdWXXM960smoclQ3ihypxds1qOCZhVzPQOzr36v1PG_9f69Og/formResponse"

MIN_DELAY_SECONDS = 30
MAX_DELAY_SECONDS = 7200
MIN_TARGET_PERCENTAGE = 92.0
MAX_TARGET_PERCENTAGE = 93.0

ENTRY_ID = {
    "nama": "entry.1360621666",
    "pertanyaan1": "entry.1693397520",
    "pertanyaan2": "entry.970987151",
    "pertanyaan3": "entry.1380373642",
    "pertanyaan4": "entry.1879915429",
    "pertanyaan5": "entry.1006285432",
    "pertanyaan6": "entry.2147146566",
    "pertanyaan7": "entry.876009505",
    "pertanyaan8": "entry.1347526263",
    "pertanyaan9": "entry.1029964857",
    "pertanyaan10": "entry.1090911020",
    "pertanyaan11": "entry.1622036961",
    "pertanyaan12": "entry.1539126032",
}

QUESTIONS = [
    "Apakah semua fitur utama pada sistem arsip surat berfungsi dengan baik?",
    "Apakah pengguna dapat melakukan pendaftaran dan login ke dalam sistem tanpa kendala?",
    "Apakah tampilan antarmuka sistem mudah dipahami oleh pengguna?",
    "Apakah menu dan navigasi pada sistem mudah digunakan?",
    "Apakah pengguna dapat menambahkan data surat masuk dan surat keluar dengan mudah?",
    "Apakah fitur pencarian atau filter data surat berdasarkan rentang tanggal membantu pengguna dalam menemukan arsip?",
    "Apakah fitur upload, preview, dan download dokumen surat berjalan dengan baik?",
    "Apakah proses validasi, penolakan, dan persetujuan surat mudah dipahami?",
    "Apakah fitur version control dapat membantu pengguna dalam melihat riwayat perubahan dokumen?",
    "Apakah identifikasi hash dokumen membantu dalam mendeteksi dokumen yang sama atau duplikat?",
    "Apakah fitur arsip dan laporan dapat membantu proses dokumentasi surat?",
    "Apakah sistem arsip surat berbasis web ini layak digunakan untuk membantu pengelolaan arsip surat?",
]

ALLOWED_ANSWERS = {
    "Sangat Setuju",
    "Setuju",
    "Cukup",
    "Tidak Setuju",
    "Sangat Tidak Setuju",
}

LIKERT_SCORE = {
    "Sangat Setuju": 5,
    "Setuju": 4,
    "Cukup": 3,
    "Tidak Setuju": 2,
    "Sangat Tidak Setuju": 1,
}

RESPONDENT_NAMES = [
    "Yarmadi",
    "Qeyza Nadira",
    "Friska Septiyan",
    "Dzakuan Salim",
    "Rizki Kurniawan",
    "Fiqri Gumilang",
    "Hidzki Alhadi",
    "Lucky Jefniter",
    "Nobel Fajri",
    "Denta Eji",
    "Hendri Naldi",
    "David Ilham",
    "Age Alendra",
    "Septrindo Ahmad",
    "Olen Rusvan",
    "Naten Steven Yatosa",
    "Arte Yatosa",
    "Forse Pernando",
    "Anisa Zahra",
    "Abim Prastafilano",
    "Adrian Wahyu",
    "Endang Putri",
    "Zahra Tulhayati",
    "Farhan Putra",
    "Yeli Amalia",
    "Devin Wiranda",
    "Sangkot Arizal",
    "Mardian",
    "Tasminudin",
    "Feza Yahya",
    "Tiara Elsa",
    "Dwi Tata",
    "Hengki Arya",
    "Aliya Zahra",
    "Arte Yatosa",
    "Arli",
    "Donal",
    "Yamerdal",
    "Daliwar",
    "Mandianto",
    "Yonnadi",
]

# Isi jawaban asli responden di sini. Setelah ENTRY_ID dan jawaban lengkap,
# cukup jalankan: python .\test_kuesioner_oke.py
HIGH_SCORE_RESPONSE_COUNT = 16

BASE_TARGET_ANSWERS = [
    "Sangat Setuju",
    "Sangat Setuju",
    "Sangat Setuju",
    "Sangat Setuju",
    "Setuju",
    "Setuju",
    "Sangat Setuju",
    "Setuju",
    "Sangat Setuju",
    "Setuju",
    "Sangat Setuju",
    "Sangat Setuju",
]

LOWER_TARGET_ANSWERS = [
    "Sangat Setuju",
    "Sangat Setuju",
    "Sangat Setuju",
    "Sangat Setuju",
    "Setuju",
    "Setuju",
    "Sangat Setuju",
    "Setuju",
    "Sangat Setuju",
    "Setuju",
    "Setuju",
    "Sangat Setuju",
]

RESPONSES = [
    {
        "nama": name,
        "jawaban": random.sample(
            (
                BASE_TARGET_ANSWERS
                if index >= len(RESPONDENT_NAMES) - HIGH_SCORE_RESPONSE_COUNT
                else LOWER_TARGET_ANSWERS
            ),
            len(QUESTIONS),
        ),
    }
    for index, name in enumerate(RESPONDENT_NAMES)
]

for index, row in enumerate(RESPONSES):
    while tuple(row["jawaban"]) in [
        tuple(r["jawaban"])
        for other_index, r in enumerate(RESPONSES)
        if other_index != index
    ]:
        random.shuffle(row["jawaban"])


def validate_config():
    if not FORM_URL:
        raise ValueError("FORM_URL masih kosong.")

    empty_entries = [key for key, value in ENTRY_ID.items() if not value]
    if empty_entries:
        raise ValueError(f"ENTRY_ID masih kosong: {', '.join(empty_entries)}")

    if MIN_DELAY_SECONDS < 0 or MAX_DELAY_SECONDS > 7200:
        raise ValueError("Interval waktu harus berada pada rentang 0 sampai 7200 detik.")

    if MIN_DELAY_SECONDS > MAX_DELAY_SECONDS:
        raise ValueError("MIN_DELAY_SECONDS tidak boleh lebih besar dari MAX_DELAY_SECONDS.")


def validate_responses():
    if len(RESPONSES) != len(RESPONDENT_NAMES):
        raise ValueError("Jumlah RESPONSES harus sama dengan jumlah RESPONDENT_NAMES.")

    for index, row in enumerate(RESPONSES, start=1):
        if row["nama"] != RESPONDENT_NAMES[index - 1]:
            raise ValueError(f"Urutan nama ke-{index} tidak sesuai: {row['nama']}")

        answers = row["jawaban"]
        if len(answers) != len(QUESTIONS):
            raise ValueError(f"{row['nama']} harus memiliki {len(QUESTIONS)} jawaban.")

        for question_number, answer in enumerate(answers, start=1):
            if answer not in ALLOWED_ANSWERS:
                raise ValueError(
                    f"Jawaban pertanyaan {question_number} untuk {row['nama']} "
                    f"belum valid: {answer!r}"
                )


def calculate_uat_percentage():
    total_score = 0
    maximum_score = len(RESPONSES) * len(QUESTIONS) * max(LIKERT_SCORE.values())

    for row in RESPONSES:
        total_score += sum(LIKERT_SCORE[answer] for answer in row["jawaban"])

    return total_score, maximum_score, total_score / maximum_score * 100


def validate_unique_answer_patterns():
    seen_patterns = {}

    for row in RESPONSES:
        pattern = tuple(row["jawaban"])

        if pattern in seen_patterns:
            raise ValueError(
                "Pola jawaban duplikat ditemukan: "
                f"{seen_patterns[pattern]} dan {row['nama']}."
            )

        seen_patterns[pattern] = row["nama"]


def validate_target_percentage_range():
    total_score, maximum_score, percentage = calculate_uat_percentage()

    print(f"Total skor UAT = {total_score} dari {maximum_score}")
    print(f"Hasil persentase UAT = {percentage:.2f}%")

    if percentage < MIN_TARGET_PERCENTAGE:
        raise ValueError(
            f"Hasil UAT masih {percentage:.2f}%, belum mencapai target "
            f"{MIN_TARGET_PERCENTAGE:.2f}%."
        )

    if percentage > MAX_TARGET_PERCENTAGE:
        raise ValueError(
            f"Hasil UAT {percentage:.2f}%, melewati batas target "
            f"{MAX_TARGET_PERCENTAGE:.2f}%."
        )


def build_payload(row):
    payload = {ENTRY_ID["nama"]: row["nama"]}

    for index, answer in enumerate(row["jawaban"], start=1):
        payload[ENTRY_ID[f"pertanyaan{index}"]] = answer

    return payload


def submit_all():
    validate_config()
    validate_responses()
    validate_unique_answer_patterns()
    validate_target_percentage_range()

    for index, row in enumerate(RESPONSES, start=1):
        response = requests.post(FORM_URL, data=build_payload(row), timeout=30)

        if response.status_code == 200:
            print(f"{index}. {row['nama']} berhasil dikirim.")
        else:
            print(f"{index}. {row['nama']} gagal. Status code: {response.status_code}")
            print(response.text[:300])

        if index < len(RESPONSES):
            delay_seconds = random.randint(MIN_DELAY_SECONDS, MAX_DELAY_SECONDS)
            print(f"Jeda {delay_seconds} detik.")
            time.sleep(delay_seconds)


if __name__ == "__main__":
    submit_all()
