# Project-TS-Kelompok8-Kriptografi-B

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

## _Implementasi Program_
