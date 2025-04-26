# Contoh fungsi dekripsi Mini-AES sederhana

# Fungsi untuk proses dekripsi
def decrypt(ciphertext, round_keys):
    """
    ciphertext: list of 4 nibbles (4-bit values)
    round_keys: list of round keys (list of 4 nibbles each)
    """
    state = add_round_key(ciphertext, round_keys[-1])
    state = inverse_shift_rows(state)
    state = inverse_substitute(state)

    for round_key in reversed(round_keys[1:-1]):
        state = add_round_key(state, round_key)
        state = inverse_mix_columns(state)
        state = inverse_shift_rows(state)
        state = inverse_substitute(state)

    state = add_round_key(state, round_keys[0])

    return state

# Fungsi Add Round Key
def add_round_key(state, key):
    return [s ^ k for s, k in zip(state, key)]

# Fungsi Inverse Shift Rows
def inverse_shift_rows(state):
    return [state[0], state[1], state[3], state[2]]

# Fungsi Inverse Substitution (menggunakan Inverse S-Box)
def inverse_substitute(state):
    inverse_s_box = {
        0x0: 0x0, 0x1: 0x5, 0x2: 0xA, 0x3: 0xF,
        0x4: 0x4, 0x5: 0x9, 0x6: 0xE, 0x7: 0x3,
        0x8: 0x8, 0x9: 0xD, 0xA: 0x2, 0xB: 0x7,
        0xC: 0xC, 0xD: 0x1, 0xE: 0x6, 0xF: 0xB
    }
    return [inverse_s_box[nibble] for nibble in state]

# Fungsi Inverse Mix Columns
def inverse_mix_columns(state):
    def multiply(a, b):
        p = 0
        for _ in range(4):
            if b & 1:
                p ^= a
            carry = a & 0x8
            a <<= 1
            if carry:
                a ^= 0x13
            b >>= 1
        return p & 0xF

    new_state = [
        multiply(state[0], 9) ^ multiply(state[2], 2),
        multiply(state[1], 9) ^ multiply(state[3], 2),
        multiply(state[0], 2) ^ multiply(state[2], 9),
        multiply(state[1], 2) ^ multiply(state[3], 9)
    ]
    return new_state
