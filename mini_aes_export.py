from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import csv

# Fungsi ECB Mode
def ecb_encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    return ciphertext

# Fungsi CBC Mode
def cbc_encrypt(plaintext, key):
    iv = get_random_bytes(AES.block_size)  # IV acak
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    return iv + ciphertext  # Gabungkan IV dengan ciphertext untuk pengiriman

# Fungsi untuk menyimpan ke file TXT (append)
def save_to_txt(plaintext, ciphertext, filename='encryption_log.txt'):
    with open(filename, 'a') as file:  # Gunakan 'a' untuk append
        file.write(f"Plaintext: {plaintext}\n")
        file.write(f"Ciphertext: {ciphertext}\n\n")  # Menambahkan baris baru sebagai pemisah

# Fungsi untuk menyimpan ke file CSV (append)
def save_to_csv(plaintext, ciphertext, filename='encryption_log.csv'):
    with open(filename, 'a', newline='') as csvfile:  # Gunakan 'a' untuk append
        fieldnames = ['plaintext', 'ciphertext']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Jika file kosong, tulis header terlebih dahulu
        if csvfile.tell() == 0:  # Cek apakah file kosong
            writer.writeheader()

        writer.writerow({'plaintext': plaintext, 'ciphertext': ciphertext})

# Fungsi untuk memuat dari file CSV
def load_from_file(filename='encryption_log.csv'):
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(f"Plaintext: {row['plaintext']}")
            print(f"Ciphertext: {row['ciphertext']}")

# Main Code
def main():
    # Input dari pengguna
    print("Masukkan pesan plaintext yang ingin dienkripsi (max 16 byte):")
    plaintext_input = input()  # Pengguna memasukkan pesan plaintext
    plaintext = plaintext_input.encode()  # Mengubah input menjadi bytes

    # Input kunci AES
    print("Masukkan kunci 16-byte untuk AES:")
    key_input = input()  # Pengguna memasukkan key
    key = key_input.encode()  # Mengubah input menjadi bytes

    if len(key) != 16:
        print("Kunci harus terdiri dari 16 byte!")
        return

    # Menyimpan enkripsi ECB
    print("\nMelakukan enkripsi dengan mode ECB...")
    ciphertext_ecb = ecb_encrypt(plaintext, key)
    print(f"Ciphertext (ECB): {ciphertext_ecb.hex()}")

    # Menyimpan enkripsi CBC
    print("\nMelakukan enkripsi dengan mode CBC...")
    ciphertext_cbc = cbc_encrypt(plaintext, key)
    print(f"Ciphertext (CBC): {ciphertext_cbc.hex()}")

    # Simpan ke kedua file (TXT dan CSV) menggunakan append
    save_to_txt(plaintext_input, ciphertext_ecb.hex(), 'encryption_log.txt')
    save_to_csv(plaintext_input, ciphertext_ecb.hex(), 'encryption_log.csv')
    print("\nHasil enkripsi disimpan ke file encryption_log.txt dan encryption_log.csv")

    # Memuat dan menampilkan data dari file CSV
    print("\nMemuat hasil enkripsi dari file...")
    load_from_file('encryption_log.csv')

if __name__ == "__main__":
    main()
