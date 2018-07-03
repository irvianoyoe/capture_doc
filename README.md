# KTP OCR NIK extractor with GUI
melakukan ekstraksi data NIK kedalam angka yang disimpan dalam output.txt

## depedency
* python 3.x
* opencv-python
* pytesseract
* wxpython

## Setup
* pastikan depedency sudah terinstall [opencv](https://www.scivision.co/install-opencv-python-windows/) [pytesseract](https://pypi.org/project/pytesseract/) [wxpython](https://www.wxpython.org/pages/downloads/)
* copy file tesseract train data kedalam tesseract repository anda [link disini](https://github.com/kristiankevin/capture_doc/tree/master/support/tesseract_train_data)
* pastikan kode berada pada drive sama dengan repository tesseract (windows ONLY)
* jalankan: python gui.py
* pilih file dalam src (NIK yang sudah di crop)
* data tersimpan di output.txt (version 0.1: data masih simpan satu satu)
