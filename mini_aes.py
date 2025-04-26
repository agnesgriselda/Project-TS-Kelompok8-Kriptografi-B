import streamlit as st

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
        [w[4], w[5], w[4], w[5]],
        [w[4], w[5], w[4], w[5]]  # Copy last key for final AddRoundKey
    ]

def mini_aes_encrypt(plain_int, key_int):
    logs = []
    state = int_to_nibbles(plain_int)
    round_keys = key_expansion(key_int)

    logs.append(f"Initial State: {state}")

    state = add_round_key(state, round_keys[0])
    logs.append(f"After Round 0 (AddRoundKey): {state}")

    # Round 1
    state = sub_nibbles(state)
    logs.append(f"After SubNibbles R1: {state}")
    state = shift_rows(state)
    logs.append(f"After ShiftRows R1: {state}")
    state = mix_columns(state)
    logs.append(f"After MixColumns R1: {state}")
    state = add_round_key(state, round_keys[1])
    logs.append(f"After AddRoundKey R1: {state}")

    # Round 2
    state = sub_nibbles(state)
    logs.append(f"After SubNibbles R2: {state}")
    state = shift_rows(state)
    logs.append(f"After ShiftRows R2: {state}")
    state = mix_columns(state)
    logs.append(f"After MixColumns R2: {state}")
    state = add_round_key(state, round_keys[2])
    logs.append(f"After AddRoundKey R2: {state}")

    # Round 3 (final round)
    state = sub_nibbles(state)
    logs.append(f"After SubNibbles R3: {state}")
    state = shift_rows(state)
    logs.append(f"After ShiftRows R3: {state}")
    state = add_round_key(state, round_keys[3])
    logs.append(f"After AddRoundKey R3: {state}")

    ciphertext = nibbles_to_int(state)
    logs.append(f"Final Ciphertext (Hex): {hex(ciphertext)}")

    return ciphertext, logs

# STREAMLIT GUI
st.title("Mini-AES 16-bit Encryption")
st.write("This app encrypts a 16-bit plaintext using Mini-AES!")

plaintext_input = st.text_input("Enter Plaintext")
key_input = st.text_input("Enter Key")

if st.button("Encrypt"):
    try:
        if len(plaintext_input) != 16 or len(key_input) != 16:
            st.error("Plaintext and Key must each be exactly 16 bits long!")
        else:
            plaintext = int(plaintext_input, 2)
            key = int(key_input, 2)
            ciphertext, logs = mini_aes_encrypt(plaintext, key)
            st.success(f"Ciphertext (hex): {hex(ciphertext)}")
            st.subheader("Encryption Steps:")
            for log in logs:
                st.text(log)
    except Exception as e:
        st.error(f"Error: {e}")