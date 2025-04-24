# mini_aes_interactive.py

S_BOX = {
    0x0: 0xE, 0x1: 0x4, 0x2: 0xD, 0x3: 0x1,
    0x4: 0x2, 0x5: 0xF, 0x6: 0xB, 0x7: 0x8,
    0x8: 0x3, 0x9: 0xA, 0xA: 0x6, 0xB: 0xC,
    0xC: 0x5, 0xD: 0x9, 0xE: 0x0, 0xF: 0x7
}

INV_S_BOX = {v: k for k, v in S_BOX.items()}

def int_to_nibbles(val):
    return [(val >> 12) & 0xF, (val >> 8) & 0xF, (val >> 4) & 0xF, val & 0xF]

def nibbles_to_int(nibs):
    return (nibs[0] << 12) | (nibs[1] << 8) | (nibs[2] << 4) | nibs[3]

def sub_nibbles(state):
    return [S_BOX[n] for n in state]

def shift_rows(state):
    return [state[0], state[1], state[3], state[2]]

def add_round_key(state, round_key):
    return [s ^ k for s, k in zip(state, round_key)]

def mul(a, b):
    p = 0
    for _ in range(4):
        if b & 1:
            p ^= a
        carry = a & 0x8
        a <<= 1
        if carry:
            a ^= 0x13
        a &= 0xF
        b >>= 1
    return p

def mix_columns(state):
    s0, s1, s2, s3 = state
    return [
        mul(1, s0) ^ mul(4, s2),
        mul(1, s1) ^ mul(4, s3),
        mul(4, s0) ^ mul(1, s2),
        mul(4, s1) ^ mul(1, s3)
    ]

def key_expansion(key):
    k = int_to_nibbles(key)
    w = [0]*6
    w[0], w[1] = k[0:2]
    w[2] = w[0] ^ S_BOX[w[1]]
    w[3] = w[2] ^ w[1]
    w[4] = w[2] ^ S_BOX[w[3]]
    w[5] = w[4] ^ w[3]
    return [
        [w[0], w[1], w[0], w[1]],
        [w[2], w[3], w[2], w[3]],
        [w[4], w[5], w[4], w[5]]
    ]

def mini_aes_encrypt(plain_int, key_int):
    print(f"\n[ENKRIPSI] Plaintext: {bin(plain_int)[2:].zfill(16)}, Key: {bin(key_int)[2:].zfill(16)}")

    state = int_to_nibbles(plain_int)
    round_keys = key_expansion(key_int)

    print(f"Initial State: {state}")

    state = add_round_key(state, round_keys[0])
    print(f"After Round 0 (AddRoundKey): {state}")

    state = sub_nibbles(state)
    print(f"After SubNibbles R1: {state}")
    state = shift_rows(state)
    print(f"After ShiftRows R1: {state}")
    state = mix_columns(state)
    print(f"After MixColumns R1: {state}")
    state = add_round_key(state, round_keys[1])
    print(f"After AddRoundKey R1: {state}")

    state = sub_nibbles(state)
    print(f"After SubNibbles R2: {state}")
    state = shift_rows(state)
    print(f"After ShiftRows R2: {state}")
    state = add_round_key(state, round_keys[2])
    print(f"After AddRoundKey R2: {state}")

    ciphertext = nibbles_to_int(state)
    print(f"\nFinal Ciphertext (16-bit): {bin(ciphertext)[2:].zfill(16)}")
    print(f"Final Ciphertext (Hex)    : {hex(ciphertext)}")
    return ciphertext

if __name__ == "__main__":
    print("=== MINI AES 16-BIT ENKRIPSI ===")
    try:
        pt_input = input("Masukkan Plaintext (16-bit dalam format biner, contoh: 1101011100101000): ")
        key_input = input("Masukkan Key (16-bit dalam format biner, contoh: 0100101011110101): ")
        
        # Ubah ke integer
        plaintext = int(pt_input, 2)
        key = int(key_input, 2)
        
        mini_aes_encrypt(plaintext, key)

    except Exception as e:
        print("Terjadi kesalahan input. Pastikan format biner 16-bit benar.")
        print("Error:", e)
