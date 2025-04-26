# Mini-AES basic functions (tanpa streamlit)

S_BOX = {
    0x0: 0xE, 0x1: 0x4, 0x2: 0xD, 0x3: 0x1,
    0x4: 0x2, 0x5: 0xF, 0x6: 0xB, 0x7: 0x8,
    0x8: 0x3, 0x9: 0xA, 0xA: 0x6, 0xB: 0xC,
    0xC: 0x5, 0xD: 0x9, 0xE: 0x0, 0xF: 0x7
}

def int_to_nibbles(val):
    return [(val >> 12) & 0xF, (val >> 8) & 0xF, (val >> 4) & 0xF, val & 0xF]

def nibbles_to_int(nibs):
    return (nibs[0] << 12) | (nibs[1] << 8) | (nibs[2] << 4) | nibs[3]

def sub_nibbles(state):
    return [S_BOX[n] for n in state]

def shift_rows(state):
    return [state[0], state[1], state[3], state[2]]

def mix_columns(state):
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
    s0, s1, s2, s3 = state
    return [
        mul(1, s0) ^ mul(4, s2),
        mul(1, s1) ^ mul(4, s3),
        mul(4, s0) ^ mul(1, s2),
        mul(4, s1) ^ mul(1, s3)
    ]

def add_round_key(state, round_key):
    return [s ^ k for s, k in zip(state, round_key)]

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
        [w[4], w[5], w[4], w[5]],
        [w[4], w[5], w[4], w[5]]
    ]

def mini_aes_encrypt_block(plain_int, key_int):
    state = int_to_nibbles(plain_int)
    round_keys = key_expansion(key_int)

    state = add_round_key(state, round_keys[0])

    state = sub_nibbles(state)
    state = shift_rows(state)
    state = mix_columns(state)
    state = add_round_key(state, round_keys[1])

    state = sub_nibbles(state)
    state = shift_rows(state)
    state = mix_columns(state)
    state = add_round_key(state, round_keys[2])

    state = sub_nibbles(state)
    state = shift_rows(state)
    state = add_round_key(state, round_keys[3])

    return nibbles_to_int(state)

# Avalanche Test Functions

def flip_bit(data, bit_position):
    return data ^ (1 << bit_position)

def count_different_bits(a, b):
    xor = a ^ b
    return bin(xor).count('1')

def avalanche_test(plaintext, key):
    original_cipher = mini_aes_encrypt_block(plaintext, key)

    print(f"Plaintext Original : {plaintext:04X}")
    print(f"Ciphertext Original: {original_cipher:04X}")

    total_changed_bits = 0

    for bit in range(16):
        modified_plaintext = flip_bit(plaintext, bit)
        modified_cipher = mini_aes_encrypt_block(modified_plaintext, key)

        changed_bits = count_different_bits(original_cipher, modified_cipher)
        percentage_change = (changed_bits / 16) * 100
        total_changed_bits += changed_bits

        print(f"\nFlip bit ke-{bit}:")
        print(f"Plaintext Baru    : {modified_plaintext:04X}")
        print(f"Ciphertext Baru   : {modified_cipher:04X}")
        print(f"Bit yang berubah  : {changed_bits}/16 ({percentage_change:.2f}%)")

    avg_changed_bits = total_changed_bits / 16
    avg_percentage = (avg_changed_bits / 16) * 100

    print("\n=== Rata-rata ===")
    print(f"Rata-rata bit berubah : {avg_changed_bits:.2f}/16")
    print(f"Rata-rata persentase  : {avg_percentage:.2f}%")

if __name__ == "__main__":
    plaintext = 0x1234  # Kamu bisa ganti
    key = 0x5678        # Kamu bisa ganti

    avalanche_test(plaintext, key)
