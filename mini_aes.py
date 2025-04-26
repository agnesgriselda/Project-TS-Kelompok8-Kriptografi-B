import streamlit as st
import io
import secrets

# --- MINI-AES FUNCTION (enkripsi dari kode kamu sebelumnya) ---

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

def inv_sub_nibbles(state):
    return [INV_S_BOX[n] for n in state]

def shift_rows(state):
    return [state[0], state[1], state[3], state[2]]

def inv_shift_rows(state):
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

def inv_mix_columns(state):
    s0, s1, s2, s3 = state
    return [
        mul(9, s0) ^ mul(2, s2),
        mul(9, s1) ^ mul(2, s3),
        mul(2, s0) ^ mul(9, s2),
        mul(2, s1) ^ mul(9, s3)
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

def mini_aes_decrypt_block(cipher_int, key_int):
    state = int_to_nibbles(cipher_int)
    round_keys = key_expansion(key_int)

    state = add_round_key(state, round_keys[3])
    state = inv_shift_rows(state)
    state = inv_sub_nibbles(state)

    state = add_round_key(state, round_keys[2])
    state = inv_mix_columns(state)
    state = inv_shift_rows(state)
    state = inv_sub_nibbles(state)

    state = add_round_key(state, round_keys[1])
    state = inv_mix_columns(state)
    state = inv_shift_rows(state)
    state = inv_sub_nibbles(state)

    state = add_round_key(state, round_keys[0])

    return nibbles_to_int(state)

# --- HELPER ---

def string_to_blocks(s):
    blocks = []
    s_bytes = s.encode('utf-8')
    if len(s_bytes) % 2 != 0:
        s_bytes += b'\x00'  # Padding kalau ganjil
    for i in range(0, len(s_bytes), 2):
        block = (s_bytes[i] << 8) + s_bytes[i+1]
        blocks.append(block)
    return blocks

def blocks_to_string(blocks):
    s = b''
    for block in blocks:
        s += bytes([(block >> 8) & 0xFF, block & 0xFF])
    return s.rstrip(b'\x00').decode('utf-8')

def hex_to_blocks(hex_string):
    hex_string = hex_string.replace(" ", "")
    if len(hex_string) % 4 != 0:
        raise ValueError("Ciphertext hex length must be multiple of 4")
    blocks = []
    for i in range(0, len(hex_string), 4):
        blocks.append(int(hex_string[i:i+4], 16))
    return blocks

def blocks_to_hex(blocks):
    return ''.join(f'{block:04X}' for block in blocks)

def xor_blocks(b1, b2):
    return b1 ^ b2

def generate_iv():
    return secrets.randbelow(0x10000) 

def save_to_txt(content, filename="output.txt"):
    return io.BytesIO(content.encode('utf-8'))

# --- STREAMLIT APP ---

st.title("Mini-AES 16-bit Encryption/Decryption (Text Mode) with ECB/CBC")

mode = st.selectbox("Select Mode:", ["Encrypt", "Decrypt"])
cipher_mode = st.selectbox("Cipher Mode:", ["ECB", "CBC"])
key_input = st.text_input("Key (4 characters):")

# Input untuk IV hanya jika mode CBC
iv_input = None
if cipher_mode == "CBC":
    iv_input = st.text_input("IV (4 hex characters, optional):", "")

input_method = st.radio("Input Method:", ["Manual Input", "Upload from File"])
plaintext_input = ""
ciphertext_input = ""

if input_method == "Manual Input":
    if mode == "Encrypt":
        plaintext_input = st.text_area("Plaintext (text) for Encrypt:")
    else:
        ciphertext_input = st.text_area("Ciphertext (hex) for Decrypt:")
else:
    uploaded_file = st.file_uploader("Upload your TXT file:", type=["txt"])
    if uploaded_file:
        file_content = uploaded_file.read().decode("utf-8")
        if mode == "Encrypt":
            plaintext_input = file_content.strip()
        else:
            ciphertext_input = file_content.strip()

if st.button("Process"):
    try:
        if len(key_input) != 4:
            st.error("Key must be exactly 4 characters!")
        else:
            key_int = (ord(key_input[0]) << 8) + ord(key_input[1])
            output_text = ""

            # Handle IV input or generate it randomly if CBC mode
            iv = None
            if cipher_mode == "CBC":
                if iv_input:
                    try:
                        iv = int(iv_input, 16)
                        if iv < 0 or iv > 0xFFFF:
                            raise ValueError("IV must be a 4-digit hex value.")
                    except ValueError:
                        st.error("Invalid IV format. IV should be a 4-digit hex value.")
                        
                else:
                    iv = generate_iv()

            if mode == "Encrypt":
                if not plaintext_input:
                    st.error("Please input plaintext.")
                else:
                    blocks = string_to_blocks(plaintext_input)
                    cipher_blocks = []
                    
                    if cipher_mode == "ECB":
                        for block in blocks:
                            cipher_blocks.append(mini_aes_encrypt_block(block, key_int))
                    elif cipher_mode == "CBC":
                        prev_block = iv
                        for block in blocks:
                            block = xor_blocks(block, prev_block)
                            enc_block = mini_aes_encrypt_block(block, key_int)
                            cipher_blocks.append(enc_block)
                            prev_block = enc_block
                        cipher_blocks.insert(0, iv)  # prepend IV to ciphertext

                    cipher_hex = blocks_to_hex(cipher_blocks)
                    st.success(f"Ciphertext (hex): {cipher_hex}")

                    output_text = cipher_hex

            elif mode == "Decrypt":
                if not ciphertext_input:
                    st.error("Please input ciphertext.")
                else:
                    blocks = hex_to_blocks(ciphertext_input)

                    if cipher_mode == "CBC":
                        iv = blocks[0]
                        blocks = blocks[1:]

                    plain_blocks = []
                    if cipher_mode == "ECB":
                        for block in blocks:
                            plain_blocks.append(mini_aes_decrypt_block(block, key_int))
                    elif cipher_mode == "CBC":
                        prev_block = iv
                        for block in blocks:
                            dec_block = mini_aes_decrypt_block(block, key_int)
                            plain_block = xor_blocks(dec_block, prev_block)
                            plain_blocks.append(plain_block)
                            prev_block = block

                    plain_text = blocks_to_string(plain_blocks)
                    st.success(f"Plaintext (text): {plain_text}")

                    output_text = plain_text

            # Export Result
            st.download_button(
                label="Download Result as TXT",
                data=save_to_txt(output_text),
                file_name="result.txt",
                mime="text/plain"
            )

    except Exception as e:
        st.error(f"Error: {e}")