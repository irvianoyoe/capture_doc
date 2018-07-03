# KTP OCR NIK extractor with GUI
melakukan ekstraksi data NIK kedalam angka yang disimpan dalam output.txt

## depedency
* python 3.x
* opencv-python
* pytesseract
* wxpython

## Setup
* copy file tesseract train data kedalam tesseract repository anda
* pastikan kode berada pada drive sama dengan repository tesseract (windows ONLY)
* jalankan: python gui.py
* pilih file dalam src (NIK yang sudah di crop)
* data tersimpan di output.txt (version 0.1: data masih simpan satu satu)