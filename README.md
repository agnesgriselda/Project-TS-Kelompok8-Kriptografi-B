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
