# KTP OCR NIK extractor with GUI
melakukan ekstraksi data NIK kedalam angka yang disimpan dalam output.txt menggunakan tesseract custom hasil train image sendiri
* scr: KTP hasil scan
* out: data NIK

## Depedency
* python 3.x
* opencv-python
* pytesseract
* wxpython
* imutils

## Setup
* pastikan depedency sudah terinstall [opencv](https://www.scivision.co/install-opencv-python-windows/) | [pytesseract](https://pypi.org/project/pytesseract/) | [wxpython](https://www.wxpython.org/pages/downloads/)
* copy file tesseract train data nik dan nama kedalam tesseract repository /tessdata [train_data](https://github.com/kristiankevin/capture_doc/tree/master/support/tesseract_train_data)
* pastikan kode berada pada drive sama dengan repository tesseract (windows ONLY)
* jalankan: python gui.py
* pilih folder atau file dalam src (KTP SCAN)
* data tersimpan di dalam output.txt
