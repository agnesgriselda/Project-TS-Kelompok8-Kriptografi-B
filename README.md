# Project-TS-Kelompok8-Kriptografi-B

## Anggota Kelompok
| Nama  | NRP  |
|----------|----------|
| Aswalia Novitriasari  | 5027231012 |
| Agnes Zenobia Griselda P  | 5027231034 |
| Nayla Raissa Azzahra  | 5027231054 |
| Aisha Ayya Ratiandari  | 5027231056 |
| Aisyah Rahmasari | 5027231072 |

## _Alur Flowchart_
![flowchart](https://github.com/user-attachments/assets/1c8e34bb-5d7f-45bd-b377-1713ae96501b)

### Penjelasan Alur Flowchart Mini-AES
#### 1. Start

- Program mulai.

#### 2. Input Plaintext dan Key

- Masukkan plaintext (data yang ingin dienkripsi) dan key (kunci enkripsi).

##### 3. AddRoundKey (Initial Round)

- Langsung di awal, plaintext di-XOR dengan key awal (initial key).

#### 4. Round 1

- *SubNibbles*
Substitusi setiap 4-bit bagian data menggunakan S-Box 4-bit.

- *ShiftRows*
Menggeser baris kedua dari 2x2 matriks internal data.

- *MixColumns*
Melakukan operasi linear (perkalian matriks sederhana di GF(2⁴)).

- *AddRoundKey*
XOR hasil dengan kunci round 1.

#### 5. Round 2

- Sama persis langkahnya:

*SubNibbles ➔ ShiftRows ➔ MixColumns ➔ AddRoundKey.*

#### 6. Round 3 (Final Round)

- Sedikit beda: tidak ada MixColumns di final round.

Hanya:

*SubNibbles ➔ ShiftRows ➔ AddRoundKey.*

#### 7. Output Ciphertext

- Hasil akhir enkripsi ditampilkan.

#### 8. End

- Program selesai.

## _Implementasi Operasi Dasar AES_

#### SubNibbles

- Menggunakan S-Box 4-bit, yang berarti tiap 4-bit input (nibble) diganti dengan value dari tabel substitusi.

- Ini untuk memberikan efek confusion (membuat hubungan plaintext–ciphertext tidak mudah ditebak).

#### ShiftRows

- Data diatur dalam bentuk matriks 2×2.

- Baris kedua digeser satu ke kiri.

- Ini memberikan efek diffusion (menyebarkan perubahan satu bit input ke banyak bit output).

#### MixColumns

- Setiap kolom di matriks diencode ulang dengan operasi linear di GF(2⁴) (field bilangan biner 4-bit).

- Menggunakan matriks sederhana seperti:

```c
[1 4]
[4 1]
```
- lalu melakukan perkalian dan penjumlahan di GF(2⁴).

- Ini memperkuat diffusion.

#### AddRoundKey

- Tiap ronde, hasil data di-XOR dengan kunci round yang sudah di-generate.

- Ini bagian penting dari keamanan.

#### *Jumlah Rounds*

_Round 1: Full (SubNibbles, ShiftRows, MixColumns, AddRoundKey)_

_Round 2: Full (SubNibbles, ShiftRows, MixColumns, AddRoundKey)_

_R_ound 3: Tidak pakai MixColumns (hanya SubNibbles, ShiftRows, AddRoundKey)._

## _Implementasi Program_
<img width="1428" alt="Screenshot 2025-04-27 at 16 59 01" src="https://github.com/user-attachments/assets/b668abf7-32e3-4d41-a3df-af23fb8288ac" />
Program ini diimplementasikan sebagai aplikasi web menggunakan Streamlit, sehingga pengguna dapat melakukan enkripsi dan dekripsi secara interaktif. Di aplikasi web, pengguna bisa memilih mode operasi: Encrypt atau Decrypt, serta metode cipher: ECB (Electronic Codebook) atau CBC (Cipher Block Chaining).

#### Input Data
- Input plaintext dan key bisa diberikan secara manual atau melalui file .txt.
- Key harus terdiri dari 4 karakter (karena Mini-AES 16-bit menggunakan 16-bit key).
- Untuk mode CBC, pengguna juga bisa memasukkan IV (Initialization Vector) secara manual dalam format heksadesimal atau membiarkannya di-generate secara otomatis.

#### Proses Enkripsi
<img width="1439" alt="Screenshot 2025-04-27 at 17 00 21" src="https://github.com/user-attachments/assets/35f2a134-0f7c-46f3-9066-b7b44758d49c" />

Plaintext diubah menjadi blok-blok 16-bit, kemudian setiap blok diproses:
- ECB Mode: Setiap blok dienkripsi langsung secara independen menggunakan Mini-AES.
- CBC Mode: Blok pertama di-XOR dengan IV, kemudian hasilnya dienkripsi. Blok berikutnya di-XOR dengan ciphertext sebelumnya sebelum dienkripsi. IV ditambahkan sebagai blok pertama ciphertext.
Proses enkripsi setiap blok ditampilkan secara detail dalam log proses, termasuk hasil setelah setiap tahap (AddRoundKey, SubNibbles, ShiftRows, MixColumns).
<img width="1422" alt="Screenshot 2025-04-27 at 17 00 37" src="https://github.com/user-attachments/assets/9f8f2a5f-fefa-47d4-8f8e-3c79eb55bc53" />

#### Proses Dekripsi
<img width="1428" alt="Screenshot 2025-04-27 at 17 01 05" src="https://github.com/user-attachments/assets/5ce5ee93-72d9-4db3-90fd-60fbcbacc9bd" />

- Ciphertext (dalam format heksadesimal) dibagi ke dalam blok-blok 16-bit.
- Setiap blok didekripsi sesuai mode:
  - ECB Mode: Tiap blok didekripsi langsung.
  - CBC Mode: Blok pertama dianggap sebagai IV, lalu dekripsi dilakukan dengan membalik proses CBC (menggunakan XOR dengan blok sebelumnya).
- Output berupa teks plaintext hasil dekripsi.
<img width="693" alt="Screenshot 2025-04-27 at 17 01 27" src="https://github.com/user-attachments/assets/683faec6-06a5-43e2-9162-54bed5e092d8" />

#### Output
- Hasil enkripsi atau dekripsi dapat di-download sebagai file .txt.
- Aplikasi juga menampilkan detail log proses enkripsi agar pengguna dapat memahami setiap tahapan Mini-AES.
<img width="740" alt="Screenshot 2025-04-27 at 17 04 10" src="https://github.com/user-attachments/assets/9e411af2-4d1e-4ec3-aba2-cebda2941545" />



### Analisis Kelebihan dan Keterbatasan Mini-AES

#### Kelebihan Mini-AES

1. **Nilai Edukatif**: Mini-AES menyediakan model pembelajaran yang sangat baik untuk memahami struktur dasar dan operasi fundamental dari algoritma AES standar dengan kompleksitas yang lebih rendah.

2. **Efisiensi Komputasi**: Dengan ukuran blok dan kunci yang hanya 16-bit (dibandingkan 128-bit pada AES standar), Mini-AES membutuhkan sumber daya komputasi yang jauh lebih sedikit, memungkinkan implementasi dan eksekusi yang lebih cepat.

3. **Transparansi Operasi**: Struktur yang sederhana memungkinkan visualisasi dan penelusuran setiap langkah transformasi dengan lebih mudah, ideal untuk keperluan pendidikan dan debugging.

4. **Mempertahankan Konsep Dasar AES**: Meskipun disederhanakan, Mini-AES mempertahankan empat operasi dasar AES (SubBytes/SubNibbles, ShiftRows, MixColumns, AddRoundKey), memberikan pemahaman konseptual yang akurat tentang algoritma asli.

5. **Portabilitas**: Ukuran yang kecil dan persyaratan komputasi yang rendah memungkinkan implementasi pada berbagai platform, termasuk perangkat dengan sumber daya terbatas.
   

#### Keterbatasan Mini-AES

1. **Keamanan Sangat Terbatas**: Dengan hanya menggunakan 16-bit untuk ukuran blok dan kunci, Mini-AES sangat rentan terhadap serangan brute force (hanya 2^16 = 65.536 kemungkinan kunci), membuat algoritma ini sama sekali tidak aman untuk penggunaan praktis.

2. **Pengurangan Difusi dan Konfusi**: MixColumns dan ShiftRows yang disederhanakan pada Mini-AES menghasilkan difusi yang lebih lemah dibandingkan AES standar, mengurangi efektivitas scrambling data.

3. **S-Box Sederhana**: S-Box 4-bit pada Mini-AES tidak memiliki sifat matematika yang sama kuatnya seperti S-Box 8-bit pada AES standar, yang mengurangi resistansi terhadap analisis kriptanalitik.

4. **Jumlah Ronde Terbatas**: Dengan hanya 3 ronde (dibandingkan 10-14 ronde pada AES standar), Mini-AES memberikan margin keamanan yang sangat kecil, membuatnya sangat rentan terhadap serangan diferensial dan linear.

5. **Ruang Status Kecil**: Ruang status 16-bit sangat terbatas, memungkinkan pemetaan lengkap dari semua kemungkinan plaintext ke ciphertext, yang bisa digunakan untuk serangan berbasis tabel lookup.

6. **Tidak Cocok untuk Data Nyata**: Ukuran blok 16-bit terlalu kecil untuk mayoritas aplikasi data praktis, membuat algoritma ini murni untuk tujuan pendidikan.

7. **Ketahanan Avalanche Lebih Lemah**: Perubahan satu bit pada input mungkin tidak menyebar secara efektif ke seluruh ciphertext seperti pada AES standar karena jumlah operasi yang lebih sedikit dan ukuran data yang lebih kecil.
